#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
機械学習入門 - Kaggle Notebook版
VGG16による画像分類とYOLO/OpenCVによる人物検出
"""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import cv2

# TensorFlow/Keras
import tensorflow as tf
from tensorflow.keras.applications import VGG16
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg16 import preprocess_input, decode_predictions
from tensorflow.keras.models import Model

# YOLO
try:
    from ultralytics import YOLO
    YOLO_AVAILABLE = True
except:
    print("⚠️ YOLOが利用できません。OpenCVのみで人物検出を行います。")
    YOLO_AVAILABLE = False

print("🚀 機械学習入門 - Kaggle Notebook版")
print("=" * 50)

# Kaggleでのファイルパス設定
KAGGLE_INPUT_DIR = '/kaggle/input'
KAGGLE_WORKING_DIR = '/kaggle/working'

def find_input_images():
    """Kaggleにアップロードされた画像を探す"""
    image_files = []
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp'}
    
    for root, dirs, files in os.walk(KAGGLE_INPUT_DIR):
        for file in files:
            if os.path.splitext(file.lower())[1] in image_extensions:
                image_files.append(os.path.join(root, file))
    
    if image_files:
        print(f"\n📷 見つかった画像ファイル:")
        for img in image_files:
            print(f"  - {img}")
    else:
        print("\n⚠️ 画像ファイルが見つかりません。")
        print("右側の「Add data」から画像をアップロードしてください。")
    
    return image_files

def vgg16_classification(image_path):
    """VGG16による画像分類"""
    print(f"\n🔍 VGG16による画像分類: {os.path.basename(image_path)}")
    
    # モデルを読み込む
    model = VGG16(weights='imagenet')
    
    # 画像を読み込んで前処理
    img = image.load_img(image_path, target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    
    # 予測
    predictions = model.predict(x)
    results = decode_predictions(predictions, top=5)[0]
    
    # 結果を表示
    print("\n予測結果（上位5件）:")
    for i, (imagenet_id, label, score) in enumerate(results):
        print(f"{i+1}. {label}: {score*100:.2f}%")
    
    # 結果を可視化
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # 元画像
    ax1.imshow(img)
    ax1.set_title(f"入力画像: {os.path.basename(image_path)}")
    ax1.axis('off')
    
    # 予測結果の棒グラフ
    labels = [r[1] for r in results]
    scores = [r[2] * 100 for r in results]
    
    ax2.barh(range(5), scores)
    ax2.set_yticks(range(5))
    ax2.set_yticklabels(labels)
    ax2.set_xlabel('確率 (%)')
    ax2.set_title('VGG16 予測結果')
    ax2.set_xlim(0, 100)
    
    plt.tight_layout()
    output_path = os.path.join(KAGGLE_WORKING_DIR, f'vgg16_result_{os.path.basename(image_path)}')
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.show()
    
    return results

def visualize_feature_maps(image_path):
    """特徴マップの可視化"""
    print(f"\n🎨 特徴マップの可視化")
    
    # VGG16モデルの一部を取り出す
    base_model = VGG16(weights='imagenet', include_top=False)
    model = Model(inputs=base_model.input, outputs=base_model.get_layer('block2_conv2').output)
    
    # 画像を読み込んで前処理
    img = image.load_img(image_path, target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    
    # 特徴マップを取得
    features = model.predict(x)
    
    # 可視化
    fig, axes = plt.subplots(4, 4, figsize=(12, 12))
    for i, ax in enumerate(axes.flat):
        if i < 16:
            ax.imshow(features[0, :, :, i], cmap='viridis')
            ax.set_title(f'Filter {i+1}')
        ax.axis('off')
    
    plt.suptitle('VGG16 Block2 Conv2 特徴マップ', fontsize=16)
    plt.tight_layout()
    
    output_path = os.path.join(KAGGLE_WORKING_DIR, f'feature_maps_{os.path.basename(image_path)}')
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.show()

def detect_person_yolo(image_path):
    """YOLOによる人物検出"""
    if not YOLO_AVAILABLE:
        print("\n⚠️ YOLOが利用できません。")
        return None
    
    print(f"\n👤 YOLOによる人物検出")
    
    # YOLOモデルを読み込む
    model = YOLO('yolov8n.pt')
    
    # 検出実行
    results = model(image_path)
    
    # 結果を描画
    img = cv2.imread(image_path)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    person_count = 0
    for r in results:
        boxes = r.boxes
        for box in boxes:
            # クラスIDが0（人物）の場合のみ
            if box.cls == 0:
                person_count += 1
                x1, y1, x2, y2 = box.xyxy[0]
                cv2.rectangle(img_rgb, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                cv2.putText(img_rgb, f'Person {box.conf[0]:.2f}', 
                           (int(x1), int(y1)-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    
    print(f"検出された人物: {person_count}人")
    
    # 結果を表示
    plt.figure(figsize=(10, 8))
    plt.imshow(img_rgb)
    plt.title(f'YOLO人物検出結果: {person_count}人検出')
    plt.axis('off')
    
    output_path = os.path.join(KAGGLE_WORKING_DIR, f'yolo_result_{os.path.basename(image_path)}')
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.show()
    
    return person_count

def detect_person_opencv(image_path):
    """OpenCVによる人物検出"""
    print(f"\n👤 OpenCV HOGによる人物検出")
    
    # HOG検出器を初期化
    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
    
    # 画像を読み込む
    img = cv2.imread(image_path)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # 人物検出
    (rects, weights) = hog.detectMultiScale(img, 
                                            winStride=(4, 4),
                                            padding=(8, 8),
                                            scale=1.05)
    
    # 検出結果を描画
    person_count = len(rects)
    for (x, y, w, h) in rects:
        cv2.rectangle(img_rgb, (x, y), (x + w, y + h), (255, 0, 0), 2)
    
    print(f"検出された人物: {person_count}人")
    
    # 結果を表示
    plt.figure(figsize=(10, 8))
    plt.imshow(img_rgb)
    plt.title(f'OpenCV HOG人物検出結果: {person_count}人検出')
    plt.axis('off')
    
    output_path = os.path.join(KAGGLE_WORKING_DIR, f'opencv_result_{os.path.basename(image_path)}')
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.show()
    
    return person_count

def create_sample_image():
    """サンプル画像を作成（デモ用）"""
    print("\n🎨 サンプル画像を作成中...")
    
    # 簡単な画像を作成
    img = np.zeros((512, 512, 3), dtype=np.uint8)
    
    # 円を描画（顔のような形）
    cv2.circle(img, (256, 200), 80, (255, 200, 150), -1)  # 顔
    cv2.circle(img, (230, 180), 15, (50, 50, 50), -1)     # 左目
    cv2.circle(img, (280, 180), 15, (50, 50, 50), -1)     # 右目
    cv2.ellipse(img, (256, 220), (40, 20), 0, 0, 180, (50, 50, 50), 2)  # 口
    
    # 体を描画
    cv2.rectangle(img, (200, 280), (310, 450), (100, 100, 200), -1)
    
    # 画像を保存
    sample_path = os.path.join(KAGGLE_WORKING_DIR, 'sample_person.jpg')
    cv2.imwrite(sample_path, img)
    
    print(f"✅ サンプル画像を作成: {sample_path}")
    return sample_path

def main():
    """メイン処理"""
    print("\n📁 Kaggle環境を確認中...")
    print(f"入力ディレクトリ: {KAGGLE_INPUT_DIR}")
    print(f"作業ディレクトリ: {KAGGLE_WORKING_DIR}")
    
    # GPU確認
    print(f"\n💻 GPU利用可能: {tf.test.is_gpu_available()}")
    if tf.test.is_gpu_available():
        print(f"GPU情報: {tf.config.list_physical_devices('GPU')}")
    
    # アップロードされた画像を探す
    image_files = find_input_images()
    
    # 画像がない場合はサンプルを作成
    if not image_files:
        print("\n📸 サンプル画像で実行します")
        sample_image = create_sample_image()
        image_files = [sample_image]
    
    # 各画像を処理
    for image_path in image_files[:3]:  # 最初の3枚まで処理
        print(f"\n{'='*60}")
        print(f"処理中: {image_path}")
        print('='*60)
        
        try:
            # VGG16による分類
            vgg16_classification(image_path)
            
            # 特徴マップの可視化
            visualize_feature_maps(image_path)
            
            # 人物検出
            if YOLO_AVAILABLE:
                detect_person_yolo(image_path)
            detect_person_opencv(image_path)
            
        except Exception as e:
            print(f"\n❌ エラーが発生しました: {e}")
            continue
    
    print("\n✅ すべての処理が完了しました！")
    print(f"結果は {KAGGLE_WORKING_DIR} に保存されています。")

# スクリプトとして実行された場合
if __name__ == "__main__":
    main()

# Jupyter Notebook用のインタラクティブ実行
print("\n💡 ヒント:")
print("個別の関数を実行することもできます:")
print("- vgg16_classification('/path/to/image.jpg')")
print("- detect_person_opencv('/path/to/image.jpg')")
print("\n画像をアップロードするには、右側の「Add data」を使用してください。")