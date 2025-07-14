#!/usr/bin/env python3
"""
Teachable Machine モデルテストスクリプト
授業テキスト「03_Teachable_Machine使い方.md」の実践
"""

import os
import sys
import argparse
import numpy as np
from PIL import Image
import tensorflow as tf
from tensorflow import keras
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # GUI無し環境用

def load_teachable_machine_model(model_path, labels_path):
    """Teachable Machineのモデルとラベルを読み込む"""
    print(f"📦 モデルを読み込み中: {model_path}")
    
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
    
    print(f"✅ モデルを読み込みました")
    print(f"クラス数: {len(labels)}")
    print(f"クラス: {', '.join(labels)}")
    
    return model, labels

def preprocess_image(image_path, target_size=(224, 224)):
    """画像を前処理"""
    # 画像を読み込み
    img = Image.open(image_path)
    
    # RGBに変換（グレースケール画像対応）
    if img.mode != 'RGB':
        img = img.convert('RGB')
    
    # リサイズ
    img = img.resize(target_size)
    
    # numpy配列に変換
    img_array = np.array(img)
    
    # 正規化（0-1の範囲に）
    img_array = img_array / 255.0
    
    # バッチ次元を追加
    img_array = np.expand_dims(img_array, axis=0)
    
    return img, img_array

def predict_image(model, labels, image_path, output_dir="output"):
    """画像を予測"""
    os.makedirs(output_dir, exist_ok=True)
    
    # 画像を前処理
    original_img, processed_img = preprocess_image(image_path)
    
    # 予測
    print(f"\n🔍 予測中: {image_path}")
    predictions = model.predict(processed_img)
    
    # 結果を取得
    predicted_class = np.argmax(predictions[0])
    confidence = predictions[0][predicted_class] * 100
    
    print(f"\n📊 予測結果:")
    print(f"予測クラス: {labels[predicted_class]}")
    print(f"信頼度: {confidence:.2f}%")
    
    # 全クラスの確率を表示
    print(f"\n全クラスの確率:")
    for i, (label, prob) in enumerate(zip(labels, predictions[0])):
        print(f"  {label}: {prob*100:.2f}%")
    
    # 結果を可視化
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # 元画像を表示
    ax1.imshow(original_img)
    ax1.set_title(f"入力画像: {os.path.basename(image_path)}")
    ax1.axis('off')
    
    # 予測結果を棒グラフで表示
    y_pos = np.arange(len(labels))
    ax2.barh(y_pos, predictions[0] * 100)
    ax2.set_yticks(y_pos)
    ax2.set_yticklabels(labels)
    ax2.set_xlabel('確率 (%)')
    ax2.set_title('予測結果')
    ax2.set_xlim(0, 100)
    
    # 予測クラスをハイライト
    ax2.barh(predicted_class, predictions[0][predicted_class] * 100, color='red')
    
    plt.tight_layout()
    
    # 保存
    output_path = os.path.join(output_dir, f"prediction_{os.path.basename(image_path)}")
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"\n💾 結果を保存: {output_path}")
    
    return predicted_class, confidence

def batch_predict(model, labels, image_dir, output_dir="output"):
    """複数画像を一括予測"""
    print(f"\n📁 ディレクトリ内の画像を一括処理: {image_dir}")
    
    # 画像ファイルを取得
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.gif'}
    image_files = [f for f in os.listdir(image_dir) 
                   if os.path.splitext(f.lower())[1] in image_extensions]
    
    if not image_files:
        print("⚠️  画像ファイルが見つかりません")
        return
    
    print(f"見つかった画像: {len(image_files)}枚")
    
    results = []
    for image_file in image_files:
        image_path = os.path.join(image_dir, image_file)
        try:
            predicted_class, confidence = predict_image(
                model, labels, image_path, output_dir
            )
            results.append({
                'file': image_file,
                'class': labels[predicted_class],
                'confidence': confidence
            })
        except Exception as e:
            print(f"❌ エラー ({image_file}): {e}")
    
    # 結果をサマリー表示
    print("\n📊 バッチ処理結果サマリー")
    print("=" * 60)
    for result in results:
        print(f"{result['file']:30} → {result['class']:15} ({result['confidence']:.1f}%)")
    
    # 結果をCSVに保存
    import csv
    csv_path = os.path.join(output_dir, "batch_results.csv")
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['file', 'class', 'confidence'])
        writer.writeheader()
        writer.writerows(results)
    
    print(f"\n💾 結果CSVを保存: {csv_path}")

def create_sample_data(output_dir="sample_data"):
    """サンプルデータを作成（デモ用）"""
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"\n🎨 サンプル画像を生成中...")
    
    # 簡単な図形を生成
    for i, (name, color) in enumerate([
        ("良品", (0, 255, 0)),
        ("不良品", (255, 0, 0))
    ]):
        img = Image.new('RGB', (224, 224), color=color)
        path = os.path.join(output_dir, f"sample_{name}_{i}.png")
        img.save(path)
        print(f"✅ {path} を作成")

def main():
    """メイン処理"""
    parser = argparse.ArgumentParser(
        description="Teachable Machineモデルをテスト"
    )
    parser.add_argument(
        "--model-path",
        default="keras_model.h5",
        help="モデルファイルのパス (default: keras_model.h5)"
    )
    parser.add_argument(
        "--labels-path",
        default="labels.txt",
        help="ラベルファイルのパス (default: labels.txt)"
    )
    parser.add_argument(
        "--image",
        help="予測する画像のパス"
    )
    parser.add_argument(
        "--batch-dir",
        help="バッチ処理するディレクトリ"
    )
    parser.add_argument(
        "--output-dir",
        default="output",
        help="出力ディレクトリ (default: output)"
    )
    parser.add_argument(
        "--create-sample",
        action="store_true",
        help="サンプルデータを作成"
    )
    
    args = parser.parse_args()
    
    print("🤖 Teachable Machine モデルテスト")
    print("=" * 60)
    
    # サンプルデータ作成モード
    if args.create_sample:
        create_sample_data()
        return
    
    # モデルファイルの存在確認
    if not os.path.exists(args.model_path):
        print(f"❌ モデルファイルが見つかりません: {args.model_path}")
        print("\nTeachable Machineからモデルをエクスポートして、")
        print("以下のファイルを配置してください:")
        print("  - keras_model.h5")
        print("  - labels.txt")
        return
    
    if not os.path.exists(args.labels_path):
        print(f"❌ ラベルファイルが見つかりません: {args.labels_path}")
        return
    
    # モデルを読み込む
    try:
        model, labels = load_teachable_machine_model(
            args.model_path, args.labels_path
        )
    except Exception as e:
        print(f"❌ モデルの読み込みに失敗: {e}")
        return
    
    # 予測実行
    if args.image:
        # 単一画像の予測
        if not os.path.exists(args.image):
            print(f"❌ 画像が見つかりません: {args.image}")
            return
        predict_image(model, labels, args.image, args.output_dir)
    
    elif args.batch_dir:
        # バッチ処理
        if not os.path.exists(args.batch_dir):
            print(f"❌ ディレクトリが見つかりません: {args.batch_dir}")
            return
        batch_predict(model, labels, args.batch_dir, args.output_dir)
    
    else:
        print("\n⚠️  予測する画像を指定してください")
        print("使用例:")
        print("  python test_model.py --image sample.jpg")
        print("  python test_model.py --batch-dir images/")

if __name__ == "__main__":
    main()