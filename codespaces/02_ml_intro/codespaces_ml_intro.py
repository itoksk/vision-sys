#!/usr/bin/env python3
"""
機械学習入門 - GitHub Codespaces対応版
工業高校生向け「要件定義から始める傷検出AIアプリ開発」

このスクリプトはGitHub Codespacesのターミナルから実行できます。
必要なライブラリのインストール:
pip install tensorflow pillow matplotlib opencv-python ultralytics
"""

import os
import sys
import argparse
import numpy as np
import matplotlib
matplotlib.use('Agg')  # GUI無し環境用
import matplotlib.pyplot as plt
from PIL import Image

# TensorFlow/Keras
import tensorflow as tf
from tensorflow.keras.applications import VGG16
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg16 import preprocess_input, decode_predictions
from tensorflow.keras.models import Model

# OpenCV
import cv2

# YOLO
from ultralytics import YOLO


def print_section(title):
    """セクションヘッダーを表示"""
    print("\n" + "=" * 50)
    print(f"{title}")
    print("=" * 50)


def vgg16_image_classification(image_path, output_dir="output"):
    """VGG16を使った画像分類"""
    print_section("VGG16による画像分類")
    
    # 出力ディレクトリ作成
    os.makedirs(output_dir, exist_ok=True)
    
    # モデルを読み込む
    print("モデルを読み込んでいます...")
    model = VGG16(weights='imagenet')
    print("準備完了！")
    
    # 画像を読み込んで前処理
    print(f"画像 '{image_path}' を読み込んでいます...")
    img = image.load_img(image_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)
    
    # 予測実行
    print("AIが画像を分析中...")
    predictions = model.predict(img_array)
    
    # 結果を解釈（上位3つ）
    results = decode_predictions(predictions, top=3)[0]
    
    # 結果を表示
    print("\n=== 認識結果 ===")
    for i, (imagenet_id, label, score) in enumerate(results):
        print(f"{i+1}位: {label} ({score*100:.1f}%)")
    
    # 結果を視覚的に保存
    plt.figure(figsize=(10, 5))
    
    # 左側に画像
    plt.subplot(1, 2, 1)
    plt.imshow(img)
    plt.title('入力画像')
    plt.axis('off')
    
    # 右側に結果のグラフ
    plt.subplot(1, 2, 2)
    labels = [r[1] for r in results]
    scores = [r[2] for r in results]
    plt.barh(labels, scores)
    plt.xlabel('確率')
    plt.title('認識結果 Top3')
    plt.xlim(0, 1)
    
    plt.tight_layout()
    output_path = os.path.join(output_dir, "vgg16_results.png")
    plt.savefig(output_path)
    plt.close()
    print(f"\n結果を保存しました: {output_path}")
    
    return model, img_array, results


def visualize_feature_maps(model, img_array, output_dir="output"):
    """特徴マップの可視化"""
    print_section("特徴マップの可視化")
    
    # 最初の畳み込み層の出力を取得
    layer_outputs = [layer.output for layer in model.layers[1:6]]
    activation_model = Model(inputs=model.input, outputs=layer_outputs)
    
    # 特徴マップを計算
    activations = activation_model.predict(img_array)
    
    # 最初の層の特徴マップを表示
    first_layer_activation = activations[0]
    plt.figure(figsize=(15, 8))
    
    # 8個の特徴マップを表示
    for i in range(8):
        plt.subplot(2, 4, i + 1)
        plt.imshow(first_layer_activation[0, :, :, i], cmap='viridis')
        plt.title(f'特徴マップ {i+1}')
        plt.axis('off')
    
    plt.suptitle('AIが見ている特徴（最初の層）')
    output_path = os.path.join(output_dir, "feature_maps.png")
    plt.savefig(output_path)
    plt.close()
    print(f"特徴マップを保存しました: {output_path}")


def yolo_person_detection(image_path, output_dir="output"):
    """YOLOv8を使った人物検出"""
    print_section("YOLO人物検出")
    
    # YOLOv8モデルをロード（初回は自動ダウンロード）
    print("YOLOモデルをロード中...")
    model = YOLO('yolov8n.pt')  # nano版（軽量）
    
    # 画像を読み込み
    image = cv2.imread(image_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # 推論実行
    results = model(image_path)
    
    # 人物（クラス0）のみを抽出
    person_detections = []
    for r in results:
        boxes = r.boxes
        if boxes is not None:
            for box in boxes:
                class_id = int(box.cls[0])
                confidence = float(box.conf[0])
                
                # クラス0が人物
                if class_id == 0 and confidence > 0.5:
                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                    person_detections.append({
                        'bbox': (int(x1), int(y1), int(x2), int(y2)),
                        'confidence': confidence
                    })
    
    # 結果を描画
    result_image = image_rgb.copy()
    for detection in person_detections:
        x1, y1, x2, y2 = detection['bbox']
        confidence = detection['confidence']
        
        # バウンディングボックスを描画
        cv2.rectangle(result_image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(result_image, f'Person: {confidence:.2f}', 
                   (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    
    print(f"検出された人物数: {len(person_detections)}")
    for i, detection in enumerate(person_detections):
        print(f"人物{i+1}: 信頼度 {detection['confidence']:.3f}")
    
    # 結果を保存
    plt.figure(figsize=(10, 8))
    plt.imshow(result_image)
    plt.title(f'YOLO検出結果 ({len(person_detections)}人)')
    plt.axis('off')
    output_path = os.path.join(output_dir, "yolo_detection.png")
    plt.savefig(output_path)
    plt.close()
    print(f"検出結果を保存しました: {output_path}")
    
    return result_image, person_detections


def opencv_person_detection(image_path, output_dir="output"):
    """OpenCVのHOG + SVMを使った人物検出"""
    print_section("OpenCV人物検出")
    
    # 画像を読み込み
    image = cv2.imread(image_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # HOG記述子を初期化
    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
    
    # 人物検出を実行
    boxes, weights = hog.detectMultiScale(
        image_rgb,
        winStride=(8, 8),
        padding=(32, 32),
        scale=1.05,
        useMeanshiftGrouping=False
    )
    
    # 結果を描画
    result_image = image_rgb.copy()
    person_detections = []
    
    for i, (x, y, w, h) in enumerate(boxes):
        # weightsの形状を確認して適切に処理
        if len(weights) > 0:
            if weights.ndim > 1 and weights.shape[1] > 0:
                confidence = weights[i][0] if i < len(weights) else 0.5
            else:
                confidence = weights[i] if i < len(weights) else 0.5
        else:
            confidence = 0.5
        
        # バウンディングボックスを描画
        cv2.rectangle(result_image, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cv2.putText(result_image, f'Person: {confidence:.2f}', 
                   (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
        
        person_detections.append({
            'bbox': (x, y, x + w, y + h),
            'confidence': float(confidence)
        })
    
    print(f"検出された人物数: {len(person_detections)}")
    for i, detection in enumerate(person_detections):
        print(f"人物{i+1}: 信頼度 {detection['confidence']:.3f}")
    
    # 結果を保存
    plt.figure(figsize=(10, 8))
    plt.imshow(result_image)
    plt.title(f'OpenCV HOG検出結果 ({len(person_detections)}人)')
    plt.axis('off')
    output_path = os.path.join(output_dir, "opencv_detection.png")
    plt.savefig(output_path)
    plt.close()
    print(f"検出結果を保存しました: {output_path}")
    
    return result_image, person_detections


def opencv_face_detection(image_path, output_dir="output"):
    """OpenCVのカスケード分類器を使った顔検出"""
    print_section("OpenCV顔検出")
    
    # 画像を読み込み
    image = cv2.imread(image_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # カスケード分類器をロード
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    # 顔検出
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    
    # 結果を描画
    result_image = image_rgb.copy()
    face_detections = []
    
    for (x, y, w, h) in faces:
        cv2.rectangle(result_image, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.putText(result_image, 'Face', 
                   (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
        
        face_detections.append({
            'bbox': (x, y, x + w, y + h),
            'confidence': 1.0  # カスケード分類器は信頼度を返さない
        })
    
    print(f"検出された顔数: {len(face_detections)}")
    
    # 結果を保存
    plt.figure(figsize=(10, 8))
    plt.imshow(result_image)
    plt.title(f'OpenCV顔検出結果 ({len(face_detections)}顔)')
    plt.axis('off')
    output_path = os.path.join(output_dir, "face_detection.png")
    plt.savefig(output_path)
    plt.close()
    print(f"検出結果を保存しました: {output_path}")
    
    return result_image, face_detections


def compare_all_methods(image_path, output_dir="output"):
    """すべての検出方法を比較"""
    print_section("すべての検出方法の比較")
    
    # 各手法で検出実行
    yolo_result, yolo_detections = yolo_person_detection(image_path, output_dir)
    opencv_result, opencv_detections = opencv_person_detection(image_path, output_dir)
    face_result, face_detections = opencv_face_detection(image_path, output_dir)
    
    # 比較結果を可視化
    plt.figure(figsize=(15, 5))
    
    plt.subplot(1, 3, 1)
    plt.imshow(yolo_result)
    plt.title(f'YOLO検出 ({len(yolo_detections)}人)')
    plt.axis('off')
    
    plt.subplot(1, 3, 2)
    plt.imshow(opencv_result)
    plt.title(f'OpenCV HOG検出 ({len(opencv_detections)}人)')
    plt.axis('off')
    
    plt.subplot(1, 3, 3)
    plt.imshow(face_result)
    plt.title(f'OpenCV顔検出 ({len(face_detections)}顔)')
    plt.axis('off')
    
    plt.tight_layout()
    output_path = os.path.join(output_dir, "comparison_all_methods.png")
    plt.savefig(output_path)
    plt.close()
    print(f"\n比較結果を保存しました: {output_path}")
    
    # 総合結果
    print("\n=== 総合結果 ===")
    print(f"YOLO: {len(yolo_detections)}人検出")
    print(f"OpenCV HOG: {len(opencv_detections)}人検出") 
    print(f"OpenCV 顔検出: {len(face_detections)}顔検出")
    
    return {
        'yolo': yolo_detections,
        'opencv_hog': opencv_detections,
        'face': face_detections
    }


def main():
    parser = argparse.ArgumentParser(description='機械学習入門 - 画像認識と人物検出')
    parser.add_argument('image_path', help='処理する画像のパス')
    parser.add_argument('--output-dir', default='output', help='結果を保存するディレクトリ（デフォルト: output）')
    parser.add_argument('--vgg16-only', action='store_true', help='VGG16のみ実行')
    parser.add_argument('--detection-only', action='store_true', help='人物検出のみ実行')
    parser.add_argument('--skip-yolo', action='store_true', help='YOLO検出をスキップ')
    
    args = parser.parse_args()
    
    # 画像の存在確認
    if not os.path.exists(args.image_path):
        print(f"エラー: 画像ファイル '{args.image_path}' が見つかりません。")
        sys.exit(1)
    
    print(f"画像を処理します: {args.image_path}")
    print(f"出力ディレクトリ: {args.output_dir}")
    
    # 出力ディレクトリ作成
    os.makedirs(args.output_dir, exist_ok=True)
    
    if not args.detection_only:
        # VGG16による画像分類
        model, img_array, results = vgg16_image_classification(args.image_path, args.output_dir)
        
        # 特徴マップの可視化
        visualize_feature_maps(model, img_array, args.output_dir)
    
    if not args.vgg16_only:
        # 人物・顔検出
        if args.skip_yolo:
            # YOLOをスキップ
            opencv_person_detection(args.image_path, args.output_dir)
            opencv_face_detection(args.image_path, args.output_dir)
        else:
            # すべての方法で比較
            compare_all_methods(args.image_path, args.output_dir)
    
    print(f"\n処理が完了しました！結果は '{args.output_dir}' ディレクトリに保存されています。")


if __name__ == "__main__":
    main()