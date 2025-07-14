#!/usr/bin/env python3
"""
Gradio傷検出アプリ開発スクリプト
授業テキスト「05_アプリ開発.md」の実践
"""

import os
import sys
import gradio as gr
import numpy as np
from PIL import Image
import tensorflow as tf
from tensorflow import keras
import json
from datetime import datetime
import csv

# グローバル変数
model = None
labels = []
history = []

def load_model(model_path="keras_model.h5", labels_path="labels.txt"):
    """モデルを読み込む"""
    global model, labels
    
    try:
        # モデルを読み込む
        model = keras.models.load_model(model_path, compile=False)
        model.compile(
            optimizer='adam',
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        # ラベルを読み込む
        with open(labels_path, 'r', encoding='utf-8') as f:
            labels = [line.strip() for line in f.readlines()]
        
        return f"✅ モデルを読み込みました（クラス: {', '.join(labels)}）"
    except Exception as e:
        return f"❌ エラー: {str(e)}"

def predict_image(image):
    """画像を予測"""
    global model, labels, history
    
    if model is None:
        return None, "❌ モデルが読み込まれていません", None
    
    if image is None:
        return None, "❌ 画像をアップロードしてください", None
    
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
        
        # 結果を生成
        result_text = f"判定: {labels[predicted_class]}\n信頼度: {confidence:.1f}%"
        
        # 詳細な確率
        details = "\n詳細:\n"
        for i, (label, prob) in enumerate(zip(labels, predictions[0])):
            details += f"  {label}: {prob*100:.1f}%\n"
        
        # 履歴に追加
        history.append({
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'result': labels[predicted_class],
            'confidence': confidence
        })
        
        # 判定結果に応じた色付け
        if labels[predicted_class] == "良品":
            result_html = f'<div style="color: green; font-size: 24px; font-weight: bold;">✅ {result_text}</div>'
        else:
            result_html = f'<div style="color: red; font-size: 24px; font-weight: bold;">❌ {result_text}</div>'
        
        return image, result_html + details, create_confidence_chart(predictions[0])
        
    except Exception as e:
        return None, f"❌ エラー: {str(e)}", None

def create_confidence_chart(predictions):
    """信頼度のチャートを作成"""
    import matplotlib.pyplot as plt
    import matplotlib
    matplotlib.use('Agg')
    
    fig, ax = plt.subplots(figsize=(8, 4))
    
    y_pos = np.arange(len(labels))
    ax.barh(y_pos, predictions * 100)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels)
    ax.set_xlabel('確率 (%)')
    ax.set_title('予測結果の詳細')
    ax.set_xlim(0, 100)
    
    # 最大値をハイライト
    max_idx = np.argmax(predictions)
    ax.barh(max_idx, predictions[max_idx] * 100, color='red')
    
    plt.tight_layout()
    return fig

def batch_process(files):
    """複数ファイルを一括処理"""
    if model is None:
        return "❌ モデルが読み込まれていません"
    
    if not files:
        return "❌ ファイルをアップロードしてください"
    
    results = []
    for file in files:
        try:
            # 画像を読み込む
            img = Image.open(file.name)
            img_array = np.array(img)
            
            # 予測
            _, result_text, _ = predict_image(img_array)
            
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
    output = "バッチ処理結果:\n\n"
    for r in results:
        output += f"📄 {r['file']}\n{r['result']}\n\n"
    
    return output

def export_history():
    """履歴をCSVでエクスポート"""
    if not history:
        return None, "履歴がありません"
    
    # CSVファイルを作成
    filename = f"inspection_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['timestamp', 'result', 'confidence'])
        writer.writeheader()
        writer.writerows(history)
    
    return filename, f"✅ 履歴を{filename}にエクスポートしました"

def create_demo_interface():
    """デモ用インターフェースを作成"""
    with gr.Blocks(title="傷検出AIアプリ", theme=gr.themes.Soft()) as demo:
        gr.Markdown("""
        # 🔍 傷検出AIアプリ
        
        部品の画像をアップロードすると、AIが良品/不良品を判定します。
        """)
        
        with gr.Tab("単一画像検査"):
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
                outputs=[output_image, result_text, confidence_chart]
            )
        
        with gr.Tab("バッチ処理"):
            batch_files = gr.File(
                label="画像ファイル（複数選択可）",
                file_count="multiple"
            )
            batch_btn = gr.Button("📦 一括処理開始", variant="primary")
            batch_result = gr.Textbox(
                label="処理結果",
                lines=10
            )
            
            batch_btn.click(
                batch_process,
                inputs=[batch_files],
                outputs=[batch_result]
            )
        
        with gr.Tab("履歴・設定"):
            gr.Markdown("### 検査履歴")
            export_btn = gr.Button("📥 履歴をエクスポート")
            export_result = gr.Textbox(label="エクスポート結果")
            export_file = gr.File(label="ダウンロード")
            
            export_btn.click(
                export_history,
                outputs=[export_file, export_result]
            )
            
            gr.Markdown("### モデル設定")
            model_file = gr.File(label="モデルファイル (keras_model.h5)")
            labels_file = gr.File(label="ラベルファイル (labels.txt)")
            load_btn = gr.Button("📤 モデルを読み込む")
            load_result = gr.Textbox(label="読み込み結果")
            
            def load_uploaded_model(model_f, labels_f):
                if model_f is None or labels_f is None:
                    return "ファイルを選択してください"
                
                return load_model(model_f.name, labels_f.name)
            
            load_btn.click(
                load_uploaded_model,
                inputs=[model_file, labels_file],
                outputs=[load_result]
            )
        
        # サンプル画像
        gr.Examples(
            examples=[
                ["sample_good.jpg"],
                ["sample_bad.jpg"]
            ],
            inputs=input_image,
            label="サンプル画像"
        )
    
    return demo

def main():
    """メイン処理"""
    print("🚀 傷検出AIアプリを起動します")
    
    # デフォルトモデルの読み込みを試みる
    if os.path.exists("keras_model.h5") and os.path.exists("labels.txt"):
        result = load_model()
        print(result)
    else:
        print("⚠️  デフォルトモデルが見つかりません")
        print("アプリ内でモデルをアップロードしてください")
    
    # デモを作成して起動
    demo = create_demo_interface()
    
    # ローカルURLを表示
    print("\n" + "="*50)
    print("アプリが起動しました！")
    print("ブラウザで以下のURLにアクセスしてください:")
    print("http://localhost:7860")
    print("="*50 + "\n")
    
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False  # Trueにすると公開URLを生成
    )

if __name__ == "__main__":
    main()