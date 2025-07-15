# Google Colab ノートブック集

このディレクトリには、Google Colabで実行できるAI/機械学習の実習用ノートブックが含まれています。

## 🚀 使い方

1. Google Colab (https://colab.research.google.com/) にアクセス
2. 「ファイル」→「ノートブックを開く」→「GitHub」タブを選択
3. このリポジトリのURLを入力してノートブックを開く
4. または、ノートブックファイルをダウンロードしてアップロード

## 📚 ノートブック一覧

### 0. 機械学習入門 (`00_機械学習入門.ipynb`) 【新規追加】
- **内容**: AIの基本概念を理解し、画像認識を体験
- **特徴**:
  - VGG16による1000種類の物体認識
  - AIが見ている特徴の可視化
  - YOLOとOpenCVによる人物検出の比較
  - 工業製品での実験
- **学習ポイント**: なぜ専用のAIが必要なのかを理解

### 1. Teachable Machine体験 (`01_teachable_machine_体験.ipynb`)
- **内容**: Teachable Machineで作成したモデルを使った画像認識
- **特徴**:
  - モデルファイルのアップロード機能
  - リアルタイムカメラ撮影機能
  - 結果の可視化（グラフ表示）
  - 日本語対応
- **必要なファイル**:
  - `keras_model.h5`（Teachable Machineからエクスポート）
  - `labels.txt`（Teachable Machineからエクスポート）

### 2. 傷検出AI開発 - 完全版 (`02_傷検出AI開発.ipynb`)
- **内容**: 製造現場向けの本格的な傷検出AIアプリケーション
- **特徴**:
  - Google Driveとの連携
  - データ収集・管理機能
  - Gradioを使ったWebアプリUI
  - バッチ処理機能
  - 検査履歴の管理とエクスポート
  - 性能評価レポート生成
  - Google Vision API連携（オプション）
- **活用シーン**: 品質管理、製造ライン検査

### 3. 傷検出AI開発 - シンプル版 (`03_傷検出AI開発_シンプル版.ipynb`)
- **内容**: 基本的な傷検出機能に絞ったシンプル版
- **特徴**:
  - 最小限のコードで実装
  - 初心者にも理解しやすい構成
  - 基本的な画像分類機能

### 4. AI画像生成入門 (`04_AI画像生成入門.ipynb`)
- **内容**: Stable DiffusionなどのAI画像生成技術の体験
- **特徴**:
  - テキストから画像を生成（Text-to-Image）
  - 画像の編集・加工（Image-to-Image）
  - プロンプトエンジニアリングの基礎
  - 生成画像の保存とダウンロード
  - 複数モデルの比較（SD、SDXL、DALL-E等）
  - ControlNetやLoRAなどの高度な技術

### 5. 要件定義実習 (`05_要件定義実習.ipynb`) 【新規追加】
- **内容**: インタラクティブに要件定義書を作成
- **特徴**:
  - 5W1Hでの要件整理（ウィジェット入力）
  - 機能要件・非機能要件の設定
  - MoSCoW法での優先順位付け
  - 要件定義書の自動生成
  - ワイヤーフレーム作成
- **成果物**: 実際の開発で使える要件定義書（.md形式）

## 🔧 Google Colab特有の機能

### 1. Google Drive連携
```python
from google.colab import drive
drive.mount('/content/drive')
```

### 2. ファイルアップロード
```python
from google.colab import files
uploaded = files.upload()
```

### 3. GPU利用
- ランタイム → ランタイムのタイプを変更 → GPU を選択

### 4. カメラ撮影
```python
from IPython.display import Javascript
# カメラAPIを使った撮影機能
```

## 📋 必要なライブラリ

各ノートブックの最初のセルで必要なライブラリをインストールします：

```python
!pip install tensorflow pillow opencv-python numpy matplotlib gradio
```

## 💡 Tips

1. **無料版の制限**:
   - 連続実行時間: 最大12時間
   - GPU使用時間: 制限あり
   - アイドル時のタイムアウト: 90分

2. **データの保存**:
   - 重要なデータはGoogle Driveに保存
   - セッション終了時にローカルファイルは削除される

3. **パフォーマンス**:
   - GPU利用時は大幅に高速化
   - 大量データの処理にはProバージョン推奨

4. **Teachable Machineモデルのエクスポート**:
   - 必ず「Tensorflow」→「Keras」形式でエクスポート
   - `keras_model.h5`と`labels.txt`の2つのファイルが必要

## 🚀 授業での使用順序（推奨）

1. **00_機械学習入門.ipynb** - AIの基礎を理解
2. **01_teachable_machine_体験.ipynb** - Teachable Machineでモデル作成
3. **05_要件定義実習.ipynb** - 開発前の設計
4. **02_傷検出AI開発.ipynb** または **03_傷検出AI開発_シンプル版.ipynb** - 実装
5. **04_AI画像生成入門.ipynb** - 発展的な学習

## 🔗 関連リソース

- [Teachable Machine](https://teachablemachine.withgoogle.com/)
- [Google Colab公式ドキュメント](https://colab.research.google.com/notebooks/welcome.ipynb)
- [TensorFlow Hub](https://tfhub.dev/)

## 📝 ライセンス

これらのノートブックは教育目的で作成されています。
自由に改変・利用してください。