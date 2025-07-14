#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Teachable Machine実習 - Kaggle Notebook版
アップロードしたモデルで画像分類を実行
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import tensorflow as tf
from tensorflow import keras
import pandas as pd
from datetime import datetime

print("🤖 Teachable Machine実習 - Kaggle Notebook版")
print("=" * 50)

# Kaggleディレクトリ設定
KAGGLE_INPUT_DIR = '/kaggle/input'
KAGGLE_WORKING_DIR = '/kaggle/working'

class TeachableMachineClassifier:
    def __init__(self, model_path=None, labels_path=None):
        """Teachable Machineモデルの初期化"""
        self.model = None
        self.labels = []
        
        if model_path and labels_path:
            self.load_model(model_path, labels_path)
    
    def find_model_files(self):
        """Kaggleにアップロードされたモデルファイルを探す"""
        model_files = []
        label_files = []
        
        print("\n📁 モデルファイルを検索中...")
        
        for root, dirs, files in os.walk(KAGGLE_INPUT_DIR):
            for file in files:
                full_path = os.path.join(root, file)
                if file.endswith('.h5'):
                    model_files.append(full_path)
                    print(f"  📦 モデル: {full_path}")
                elif file == 'labels.txt':
                    label_files.append(full_path)
                    print(f"  🏷️ ラベル: {full_path}")
        
        if not model_files:
            print("\n⚠️ モデルファイル(.h5)が見つかりません。")
            print("Teachable Machineからエクスポートしたファイルをアップロードしてください:")
            print("1. keras_model.h5")
            print("2. labels.txt")
        
        return model_files, label_files
    
    def load_model(self, model_path, labels_path):
        """モデルとラベルを読み込む"""
        try:
            print(f"\n📦 モデルを読み込み中: {model_path}")
            self.model = keras.models.load_model(model_path, compile=False)
            self.model.compile(
                optimizer='adam',
                loss='categorical_crossentropy',
                metrics=['accuracy']
            )
            
            # ラベルを読み込む
            with open(labels_path, 'r', encoding='utf-8') as f:
                self.labels = [line.strip() for line in f.readlines()]
            
            print(f"✅ モデルを読み込みました")
            print(f"クラス数: {len(self.labels)}")
            print(f"クラス: {', '.join(self.labels)}")
            
            return True
            
        except Exception as e:
            print(f"❌ モデルの読み込みに失敗: {e}")
            return False
    
    def preprocess_image(self, image_path, target_size=(224, 224)):
        """画像を前処理"""
        img = Image.open(image_path)
        
        # RGBに変換
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # リサイズ
        img = img.resize(target_size)
        
        # numpy配列に変換して正規化
        img_array = np.array(img) / 255.0
        
        # バッチ次元を追加
        img_array = np.expand_dims(img_array, axis=0)
        
        return img, img_array
    
    def predict(self, image_path):
        """画像を予測"""
        if self.model is None:
            print("❌ モデルが読み込まれていません")
            return None
        
        # 画像を前処理
        original_img, processed_img = self.preprocess_image(image_path)
        
        # 予測
        predictions = self.model.predict(processed_img)
        
        # 結果を取得
        predicted_class = np.argmax(predictions[0])
        confidence = predictions[0][predicted_class] * 100
        
        result = {
            'image_path': image_path,
            'predicted_class': self.labels[predicted_class],
            'confidence': confidence,
            'all_predictions': {
                self.labels[i]: predictions[0][i] * 100 
                for i in range(len(self.labels))
            }
        }
        
        return result, original_img
    
    def visualize_prediction(self, result, image):
        """予測結果を可視化"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # 元画像を表示
        ax1.imshow(image)
        ax1.set_title(f"予測: {result['predicted_class']} ({result['confidence']:.1f}%)")
        ax1.axis('off')
        
        # 確率分布を表示
        labels = list(result['all_predictions'].keys())
        values = list(result['all_predictions'].values())
        
        colors = ['green' if label == result['predicted_class'] else 'blue' for label in labels]
        bars = ax2.barh(labels, values, color=colors)
        ax2.set_xlabel('確率 (%)')
        ax2.set_title('クラス別確率分布')
        ax2.set_xlim(0, 100)
        
        # 値を表示
        for bar, value in zip(bars, values):
            ax2.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2, 
                    f'{value:.1f}%', va='center')
        
        plt.tight_layout()
        
        # 保存
        output_path = os.path.join(KAGGLE_WORKING_DIR, 
                                  f'prediction_{os.path.basename(result["image_path"])}')
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.show()

def find_images():
    """アップロードされた画像を探す"""
    image_files = []
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp'}
    
    for root, dirs, files in os.walk(KAGGLE_INPUT_DIR):
        for file in files:
            if os.path.splitext(file.lower())[1] in image_extensions:
                full_path = os.path.join(root, file)
                # モデル関連の画像は除外
                if 'model' not in file.lower():
                    image_files.append(full_path)
    
    if image_files:
        print(f"\n📷 見つかったテスト画像: {len(image_files)}枚")
        for img in image_files[:5]:  # 最初の5枚を表示
            print(f"  - {img}")
        if len(image_files) > 5:
            print(f"  ... 他 {len(image_files) - 5}枚")
    
    return image_files

def batch_predict(classifier, image_files, output_csv=True):
    """複数画像を一括予測"""
    print(f"\n🔄 バッチ処理開始: {len(image_files)}枚")
    
    results = []
    
    for i, image_path in enumerate(image_files):
        print(f"\n処理中 [{i+1}/{len(image_files)}]: {os.path.basename(image_path)}")
        
        try:
            result, img = classifier.predict(image_path)
            
            # 結果を表示
            print(f"  → {result['predicted_class']} ({result['confidence']:.1f}%)")
            
            # 可視化
            classifier.visualize_prediction(result, img)
            
            # 結果を保存
            results.append({
                'filename': os.path.basename(image_path),
                'prediction': result['predicted_class'],
                'confidence': result['confidence'],
                'timestamp': datetime.now().isoformat()
            })
            
        except Exception as e:
            print(f"  ❌ エラー: {e}")
            results.append({
                'filename': os.path.basename(image_path),
                'prediction': 'ERROR',
                'confidence': 0,
                'timestamp': datetime.now().isoformat()
            })
    
    # CSVに保存
    if output_csv and results:
        df = pd.DataFrame(results)
        csv_path = os.path.join(KAGGLE_WORKING_DIR, 'batch_predictions.csv')
        df.to_csv(csv_path, index=False)
        print(f"\n📊 結果をCSVに保存: {csv_path}")
        
        # サマリーを表示
        print("\n📈 予測結果サマリー:")
        print(df['prediction'].value_counts())
    
    return results

def create_confusion_matrix(results_df):
    """混同行列を作成（真のラベルがある場合）"""
    # この例では真のラベルがないため、予測結果の分布を表示
    plt.figure(figsize=(8, 6))
    
    prediction_counts = results_df['prediction'].value_counts()
    
    plt.pie(prediction_counts.values, labels=prediction_counts.index, autopct='%1.1f%%')
    plt.title('予測結果の分布')
    
    output_path = os.path.join(KAGGLE_WORKING_DIR, 'prediction_distribution.png')
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.show()

def main():
    """メイン処理"""
    print("\n🚀 Teachable Machine モデルテストを開始")
    
    # 初期化
    classifier = TeachableMachineClassifier()
    
    # モデルファイルを探す
    model_files, label_files = classifier.find_model_files()
    
    if model_files and label_files:
        # 最初に見つかったモデルを使用
        classifier.load_model(model_files[0], label_files[0])
        
        # テスト画像を探す
        test_images = find_images()
        
        if test_images:
            # バッチ予測
            results = batch_predict(classifier, test_images)
            
            # 結果の分析
            if results:
                df = pd.DataFrame(results)
                create_confusion_matrix(df)
                
                print("\n✅ 処理完了！")
                print(f"結果は {KAGGLE_WORKING_DIR} に保存されています。")
        else:
            print("\n⚠️ テスト画像が見つかりません。")
            print("画像をアップロードして再実行してください。")
    else:
        print("\n📝 使い方:")
        print("1. Teachable Machineでモデルをエクスポート")
        print("2. 「Tensorflow」→「Keras」→「モデルをダウンロード」")
        print("3. keras_model.h5 と labels.txt をKaggleにアップロード")
        print("4. テストしたい画像もアップロード")
        print("5. このスクリプトを再実行")

# インタラクティブ使用のためのヘルパー関数
def quick_test(image_path):
    """単一画像のクイックテスト"""
    # モデルを自動検索して読み込む
    classifier = TeachableMachineClassifier()
    model_files, label_files = classifier.find_model_files()
    
    if model_files and label_files:
        classifier.load_model(model_files[0], label_files[0])
        result, img = classifier.predict(image_path)
        classifier.visualize_prediction(result, img)
        return result
    else:
        print("モデルファイルが見つかりません")
        return None

# スクリプトとして実行
if __name__ == "__main__":
    main()

# 使用方法の表示
print("\n💡 インタラクティブ使用:")
print("quick_test('/kaggle/input/your-dataset/test_image.jpg')")
print("\n詳細はREADMEを参照してください。")