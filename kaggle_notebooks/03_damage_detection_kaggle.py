#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
傷検出AIアプリ開発 - Kaggle Notebook版
Gradioを使った実用的なWebアプリケーション
"""

import os
import numpy as np
import pandas as pd
from PIL import Image
import tensorflow as tf
from tensorflow import keras
import gradio as gr
from datetime import datetime
import json
import matplotlib.pyplot as plt
import seaborn as sns

print("🔍 傷検出AIアプリ開発 - Kaggle Notebook版")
print("=" * 50)

# Kaggleディレクトリ設定
KAGGLE_INPUT_DIR = '/kaggle/input'
KAGGLE_WORKING_DIR = '/kaggle/working'

# グローバル変数
model = None
labels = []
inspection_history = []

def find_and_load_model():
    """モデルを自動検索して読み込む"""
    global model, labels
    
    print("📁 モデルファイルを検索中...")
    
    model_path = None
    labels_path = None
    
    for root, dirs, files in os.walk(KAGGLE_INPUT_DIR):
        for file in files:
            if file.endswith('.h5') and model_path is None:
                model_path = os.path.join(root, file)
            elif file == 'labels.txt' and labels_path is None:
                labels_path = os.path.join(root, file)
    
    if model_path and labels_path:
        try:
            print(f"📦 モデルを読み込み: {model_path}")
            model = keras.models.load_model(model_path, compile=False)
            model.compile(
                optimizer='adam',
                loss='categorical_crossentropy',
                metrics=['accuracy']
            )
            
            with open(labels_path, 'r', encoding='utf-8') as f:
                labels = [line.strip() for line in f.readlines()]
            
            print(f"✅ モデル読み込み完了（クラス: {', '.join(labels)}）")
            return True
            
        except Exception as e:
            print(f"❌ モデル読み込みエラー: {e}")
            return False
    else:
        print("⚠️ モデルファイルが見つかりません")
        return False

def predict_image(image):
    """画像を予測"""
    global model, labels, inspection_history
    
    if model is None:
        return None, "❌ モデルが読み込まれていません", None, None
    
    if image is None:
        return None, "❌ 画像をアップロードしてください", None, None
    
    try:
        # 画像を前処理
        img = Image.fromarray(image)
        img = img.resize((224, 224))
        img_array = np.array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)
        
        # 予測
        predictions = model.predict(img_array)
        predicted_class = np.argmax(predictions[0])
        confidence = predictions[0][predicted_class] * 100
        
        # 結果を記録
        result = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'result': labels[predicted_class],
            'confidence': confidence,
            'all_predictions': {labels[i]: float(predictions[0][i] * 100) for i in range(len(labels))}
        }
        
        inspection_history.append(result)
        
        # 結果テキスト
        result_text = f"判定: {labels[predicted_class]}\n信頼度: {confidence:.1f}%"
        
        # 詳細情報
        details = "\n詳細:\n"
        for label, prob in result['all_predictions'].items():
            details += f"  {label}: {prob:.1f}%\n"
        
        # 判定結果に応じた表示
        if labels[predicted_class] == "良品" or "good" in labels[predicted_class].lower():
            result_html = f'<div style="background-color: #d4edda; color: #155724; padding: 20px; border-radius: 5px; font-size: 24px; font-weight: bold;">✅ {result_text}</div>'
        else:
            result_html = f'<div style="background-color: #f8d7da; color: #721c24; padding: 20px; border-radius: 5px; font-size: 24px; font-weight: bold;">❌ {result_text}</div>'
        
        # 信頼度チャートを作成
        confidence_chart = create_confidence_chart(predictions[0])
        
        # 統計情報を更新
        stats = create_statistics()
        
        return image, result_html + details, confidence_chart, stats
        
    except Exception as e:
        return None, f"❌ エラー: {str(e)}", None, None

def create_confidence_chart(predictions):
    """信頼度のチャートを作成"""
    plt.figure(figsize=(8, 4))
    
    y_pos = np.arange(len(labels))
    plt.barh(y_pos, predictions * 100, color=['green' if i == np.argmax(predictions) else 'skyblue' for i in range(len(labels))])
    plt.yticks(y_pos, labels)
    plt.xlabel('確率 (%)')
    plt.title('予測結果の詳細')
    plt.xlim(0, 100)
    
    # 値を表示
    for i, v in enumerate(predictions * 100):
        plt.text(v + 1, i, f'{v:.1f}%', va='center')
    
    plt.tight_layout()
    return plt.gcf()

def create_statistics():
    """検査履歴の統計を作成"""
    if not inspection_history:
        return "まだ検査履歴がありません"
    
    # データフレームに変換
    df = pd.DataFrame([{
        'timestamp': h['timestamp'],
        'result': h['result'],
        'confidence': h['confidence']
    } for h in inspection_history])
    
    # 統計情報
    stats_text = f"📊 検査統計\n"
    stats_text += f"総検査数: {len(df)}件\n\n"
    
    # 結果の分布
    result_counts = df['result'].value_counts()
    stats_text += "結果の内訳:\n"
    for result, count in result_counts.items():
        percentage = (count / len(df)) * 100
        stats_text += f"  {result}: {count}件 ({percentage:.1f}%)\n"
    
    # 平均信頼度
    avg_confidence = df['confidence'].mean()
    stats_text += f"\n平均信頼度: {avg_confidence:.1f}%"
    
    # 最近の5件
    stats_text += "\n\n最近の検査結果:\n"
    recent = df.tail(5)
    for _, row in recent.iterrows():
        stats_text += f"  {row['timestamp']}: {row['result']} ({row['confidence']:.1f}%)\n"
    
    return stats_text

def batch_process(files):
    """複数ファイルを一括処理"""
    if model is None:
        return "❌ モデルが読み込まれていません", None
    
    if not files:
        return "❌ ファイルをアップロードしてください", None
    
    results = []
    
    for file in files:
        try:
            # 画像を読み込む
            img = Image.open(file.name)
            img_array = np.array(img)
            
            # 予測
            _, result_text, _, _ = predict_image(img_array)
            
            results.append({
                'file': os.path.basename(file.name),
                'result': result_text
            })
        except Exception as e:
            results.append({
                'file': os.path.basename(file.name),
                'result': f"エラー: {str(e)}"
            })
    
    # 結果を整形
    output = "📦 バッチ処理結果:\n\n"
    for r in results:
        output += f"📄 {r['file']}\n{r['result']}\n\n"
    
    # バッチ結果の可視化
    batch_viz = create_batch_visualization(results)
    
    return output, batch_viz

def create_batch_visualization(results):
    """バッチ処理結果の可視化"""
    # 結果から統計を抽出（簡易版）
    good_count = sum(1 for r in results if "良品" in str(r['result']) or "good" in str(r['result']).lower())
    bad_count = len(results) - good_count
    
    plt.figure(figsize=(8, 6))
    
    # 円グラフ
    sizes = [good_count, bad_count]
    labels_pie = ['良品', '不良品']
    colors = ['#28a745', '#dc3545']
    
    plt.pie(sizes, labels=labels_pie, colors=colors, autopct='%1.1f%%', startangle=90)
    plt.title('バッチ処理結果の分布')
    plt.axis('equal')
    
    return plt.gcf()

def export_history():
    """履歴をエクスポート"""
    if not inspection_history:
        return None, "履歴がありません"
    
    # CSVファイルを作成
    filename = f"inspection_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    filepath = os.path.join(KAGGLE_WORKING_DIR, filename)
    
    # データフレームに変換
    df = pd.DataFrame([{
        'timestamp': h['timestamp'],
        'result': h['result'],
        'confidence': h['confidence']
    } for h in inspection_history])
    
    df.to_csv(filepath, index=False, encoding='utf-8')
    
    # JSONでも保存（詳細情報付き）
    json_filename = filename.replace('.csv', '.json')
    json_filepath = os.path.join(KAGGLE_WORKING_DIR, json_filename)
    
    with open(json_filepath, 'w', encoding='utf-8') as f:
        json.dump(inspection_history, f, ensure_ascii=False, indent=2)
    
    return filepath, f"✅ 履歴をエクスポートしました:\n- CSV: {filename}\n- JSON: {json_filename}"

def create_app():
    """Gradioアプリを作成"""
    with gr.Blocks(title="傷検出AIアプリ", theme=gr.themes.Soft()) as app:
        gr.Markdown("""
        # 🔍 傷検出AIアプリ - Kaggle版
        
        部品の画像をアップロードすると、AIが良品/不良品を判定します。
        
        **使い方:**
        1. Teachable Machineのモデル（keras_model.h5, labels.txt）をアップロード
        2. 検査したい画像をアップロード
        3. 「検査開始」をクリック
        """)
        
        # モデル状態
        model_status = gr.Textbox(
            label="モデル状態", 
            value="モデルを読み込み中...",
            interactive=False
        )
        
        with gr.Tab("🔍 単一画像検査"):
            with gr.Row():
                with gr.Column():
                    input_image = gr.Image(label="検査画像")
                    check_btn = gr.Button("🔍 検査開始", variant="primary")
                
                with gr.Column():
                    output_image = gr.Image(label="検査済み画像")
                    result_text = gr.HTML(label="判定結果")
                    confidence_chart = gr.Plot(label="信頼度チャート")
            
            check_btn.click(
                predict_image,
                inputs=[input_image],
                outputs=[output_image, result_text, confidence_chart, model_status]
            )
        
        with gr.Tab("📦 バッチ処理"):
            batch_files = gr.File(
                label="画像ファイル（複数選択可）",
                file_count="multiple"
            )
            batch_btn = gr.Button("📦 一括処理開始", variant="primary")
            batch_result = gr.Textbox(label="処理結果", lines=10)
            batch_viz = gr.Plot(label="バッチ処理統計")
            
            batch_btn.click(
                batch_process,
                inputs=[batch_files],
                outputs=[batch_result, batch_viz]
            )
        
        with gr.Tab("📊 統計・履歴"):
            gr.Markdown("### 検査統計")
            stats_display = gr.Textbox(label="統計情報", lines=15)
            refresh_btn = gr.Button("🔄 統計を更新")
            
            gr.Markdown("### 履歴エクスポート")
            export_btn = gr.Button("📥 履歴をエクスポート")
            export_result = gr.Textbox(label="エクスポート結果")
            export_file = gr.File(label="ダウンロード")
            
            refresh_btn.click(
                create_statistics,
                outputs=[stats_display]
            )
            
            export_btn.click(
                export_history,
                outputs=[export_file, export_result]
            )
        
        # 初期化時にモデルを読み込む
        def update_model_status():
            if find_and_load_model():
                return "✅ モデル読み込み完了", create_statistics()
            else:
                return "⚠️ モデルファイルをアップロードしてください", "統計情報なし"
        
        # アプリ起動時に実行
        app.load(update_model_status, outputs=[model_status, stats_display])
    
    return app

def main():
    """メイン処理"""
    print("\n🚀 傷検出AIアプリを起動します")
    
    # アプリを作成
    app = create_app()
    
    # Kaggleでの注意事項
    print("\n📝 Kaggleでの実行について:")
    print("1. セッションは9時間で終了します")
    print("2. 結果は定期的に保存してください")
    print("3. 公開URLは Share → Public で取得できます")
    
    # アプリを起動
    app.launch(share=True)  # Kaggleでは share=True で公開URL生成

# スクリプトとして実行
if __name__ == "__main__":
    main()

# 使用方法
print("\n💡 使用方法:")
print("1. このセルを実行してアプリを起動")
print("2. 表示されるURLをクリック")
print("3. モデルファイルと画像をアップロードして検査")