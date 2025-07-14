# Kaggle Notebook 実行ガイド

このディレクトリには、Kaggle Notebookで各授業の内容を実行するためのスクリプトが含まれています。

## 📚 Kaggle Notebookとは

- 無料で使えるクラウド実行環境
- GPUが無料で利用可能（週30時間）
- ライブラリがプリインストール済み
- ファイルの保存・共有が簡単

## 🚀 Kaggleの始め方

### 1. アカウント作成
1. [Kaggle.com](https://www.kaggle.com) にアクセス
2. 「Register」をクリックしてアカウント作成
3. メールアドレスまたはGoogleアカウントで登録

### 2. 新しいNotebookの作成
1. ログイン後、右上の「Create」→「New Notebook」
2. 言語は「Python」を選択
3. アクセラレータで「GPU」を選択（画像処理用）

## 📤 ファイルのアップロード方法

### 方法1: Kaggle UIから直接アップロード
1. Notebookの右側パネルで「Add data」をクリック
2. 「Upload」タブを選択
3. ファイルをドラッグ&ドロップまたは選択
4. アップロード完了後、ファイルパスは `/kaggle/input/` 以下に

### 方法2: コードセルでアップロード
```python
# ファイルアップロード用のウィジェットを表示
from google.colab import files
uploaded = files.upload()

# アップロードしたファイル名を確認
for filename in uploaded.keys():
    print(f'アップロードされたファイル: {filename}')
```

## 🤖 Teachable Machineモデルのアップロード手順

### 1. Teachable Machineでモデルをエクスポート
1. [Teachable Machine](https://teachablemachine.withgoogle.com/)でプロジェクトを開く
2. 「モデルをエクスポート」をクリック
3. 「Tensorflow」タブを選択
4. 「Keras」を選択
5. 「モデルをダウンロード」をクリック
   - `keras_model.h5`（モデルファイル）
   - `labels.txt`（ラベルファイル）
   の2つのファイルがダウンロードされます

### 2. Kaggleにアップロード
1. Notebookで「Add data」→「Upload」
2. `keras_model.h5`と`labels.txt`を両方選択してアップロード
3. アップロード後のパス：
   - `/kaggle/input/[dataset-name]/keras_model.h5`
   - `/kaggle/input/[dataset-name]/labels.txt`

### 3. モデルの読み込み
```python
import os

# アップロードしたファイルのパスを確認
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# モデルを読み込む
model_path = '/kaggle/input/[dataset-name]/keras_model.h5'
labels_path = '/kaggle/input/[dataset-name]/labels.txt'
```

## 📂 各授業用スクリプト

### 1. 機械学習入門
```python
!wget https://raw.githubusercontent.com/[your-repo]/kaggle_notebooks/01_ml_intro_kaggle.py
!python 01_ml_intro_kaggle.py
```

### 2. Teachable Machine実習
```python
!wget https://raw.githubusercontent.com/[your-repo]/kaggle_notebooks/02_teachable_machine_kaggle.py
!python 02_teachable_machine_kaggle.py
```

### 3. 傷検出アプリ開発
```python
!wget https://raw.githubusercontent.com/[your-repo]/kaggle_notebooks/03_damage_detection_kaggle.py
!python 03_damage_detection_kaggle.py
```

### 4. AI画像生成
```python
!wget https://raw.githubusercontent.com/[your-repo]/kaggle_notebooks/04_image_generation_kaggle.py
!python 04_image_generation_kaggle.py
```

## 🖼️ 画像ファイルの扱い方

### サンプル画像のアップロード
1. 検査したい部品の画像を用意（.jpg, .png形式）
2. 「Add data」→「Upload」でアップロード
3. コードで画像パスを指定：
```python
image_path = '/kaggle/input/[dataset-name]/sample.jpg'
```

### 複数画像の一括処理
```python
import os
from pathlib import Path

# アップロードした画像を全て取得
image_dir = '/kaggle/input/[dataset-name]'
image_files = list(Path(image_dir).glob('*.jpg')) + list(Path(image_dir).glob('*.png'))

print(f"見つかった画像: {len(image_files)}枚")
for img_path in image_files:
    print(f"  - {img_path.name}")
```

## 💾 結果の保存とダウンロード

### 結果をファイルに保存
```python
# 結果を保存
output_dir = '/kaggle/working'  # 作業ディレクトリ
result_path = f'{output_dir}/results.csv'

# CSVとして保存
import pandas as pd
df = pd.DataFrame(results)
df.to_csv(result_path, index=False)
print(f"結果を保存: {result_path}")
```

### ファイルのダウンロード
```python
from IPython.display import FileLink

# ダウンロードリンクを表示
FileLink('results.csv')
```

## ⚡ GPU/TPUの使用

### GPU設定の確認
```python
import tensorflow as tf

# GPU利用可能か確認
print("GPU利用可能:", tf.test.is_gpu_available())
print("GPU情報:", tf.config.list_physical_devices('GPU'))
```

### セッション設定
1. 右側パネルの「Settings」
2. 「Accelerator」で「GPU」または「TPU」を選択
3. 「Save」をクリック

## 🔧 トラブルシューティング

### よくある問題と解決法

#### 1. ファイルが見つからない
```python
# 正しいパスを確認
import os
for dirname, _, filenames in os.walk('/kaggle'):
    for filename in filenames:
        if filename.endswith(('.h5', '.txt', '.jpg', '.png')):
            print(os.path.join(dirname, filename))
```

#### 2. メモリ不足
- 画像サイズを小さくする
- バッチサイズを減らす
- 不要な変数を削除: `del variable_name`

#### 3. セッションタイムアウト
- Kaggleは9時間でセッションが切れます
- 定期的に結果を保存してください

## 📝 ベストプラクティス

1. **データセットの作成**
   - よく使うファイルはデータセットとして保存
   - 他のNotebookでも再利用可能

2. **バージョン管理**
   - Notebookは自動保存される
   - 「Save Version」で手動保存も可能

3. **共有設定**
   - 「Share」で公開/非公開を設定
   - URLを共有すれば他の人も実行可能

## 🎓 学習の進め方

1. このREADMEを参考にKaggleアカウントを作成
2. 新しいNotebookを作成
3. 各授業のスクリプトをコピー&ペースト
4. 必要なファイルをアップロード
5. セルを順番に実行

## 🔗 参考リンク

- [Kaggle Learn](https://www.kaggle.com/learn)
- [Kaggle Notebooks Guide](https://www.kaggle.com/docs/notebooks)
- [GPU使用に関するFAQ](https://www.kaggle.com/docs/efficient-gpu-usage)