# 機械学習入門 - GitHub Codespaces対応版

このスクリプトは、授業テキストの「02_機械学習入門.md」のコードをGitHub Codespacesのターミナルから実行できるように修正したものです。

## 必要な環境

- Python 3.8以上
- GitHub Codespaces または ローカルのPython環境

## セットアップ

### 1. 必要なライブラリのインストール

ターミナルで以下のコマンドを実行してください：

```bash
pip install tensorflow pillow matplotlib opencv-python ultralytics
```

### 2. サンプル画像の準備

テスト用の画像を用意してください。例：
- 人物が写っている写真
- 工具や部品の写真
- 風景写真など

## 使い方

### 基本的な使い方

```bash
# 画像を指定して実行
python codespaces_ml_intro.py path/to/your/image.jpg
```

### オプション

```bash
# 出力ディレクトリを指定
python codespaces_ml_intro.py image.jpg --output-dir my_results

# VGG16の画像分類のみ実行
python codespaces_ml_intro.py image.jpg --vgg16-only

# 人物検出のみ実行
python codespaces_ml_intro.py image.jpg --detection-only

# YOLO検出をスキップ（OpenCVのみ使用）
python codespaces_ml_intro.py image.jpg --skip-yolo
```

## 実行例

### 例1: すべての機能を実行

```bash
python codespaces_ml_intro.py sample.jpg
```

このコマンドは以下を実行します：
1. VGG16による画像分類（1000種類の物体認識）
2. 特徴マップの可視化
3. YOLOによる人物検出
4. OpenCV HOGによる人物検出
5. OpenCVによる顔検出
6. すべての検出方法の比較

### 例2: VGG16のみ実行

```bash
python codespaces_ml_intro.py sample.jpg --vgg16-only
```

画像分類と特徴マップの可視化のみを実行します。

### 例3: カスタム出力ディレクトリ

```bash
python codespaces_ml_intro.py sample.jpg --output-dir results/experiment1
```

結果を`results/experiment1`ディレクトリに保存します。

## 出力ファイル

実行後、指定した出力ディレクトリ（デフォルト: `output`）に以下のファイルが生成されます：

- `vgg16_results.png`: VGG16の認識結果
- `feature_maps.png`: 特徴マップの可視化
- `yolo_detection.png`: YOLO人物検出結果
- `opencv_detection.png`: OpenCV HOG人物検出結果
- `face_detection.png`: OpenCV顔検出結果
- `comparison_all_methods.png`: すべての検出方法の比較

## トラブルシューティング

### エラー: "No module named 'cv2'"

OpenCVがインストールされていません。以下を実行してください：

```bash
pip install opencv-python
```

### エラー: "No module named 'ultralytics'"

YOLOライブラリがインストールされていません。以下を実行してください：

```bash
pip install ultralytics
```

### メモリ不足エラー

大きな画像を処理する際にメモリ不足になる場合があります。より小さな画像を使用するか、`--vgg16-only`や`--detection-only`オプションを使って一部の機能のみを実行してください。

## 授業での使い方

1. **デモンストレーション**
   ```bash
   # 教師が画面共有しながら実行
   python codespaces_ml_intro.py demo_image.jpg
   ```

2. **生徒の実習**
   ```bash
   # 各自が自分の画像で実験
   python codespaces_ml_intro.py my_photo.jpg --output-dir my_results
   ```

3. **結果の共有**
   - 生成された画像をGitHubにコミット
   - プルリクエストで提出

## 元の授業テキストとの違い

1. **画像入力**: Google Colabの`files.upload()`の代わりに、コマンドライン引数で画像パスを指定
2. **結果表示**: `plt.show()`の代わりに、画像ファイルとして保存
3. **実行方法**: Jupyter Notebookのセル実行の代わりに、ターミナルからスクリプト実行
4. **GUI対応**: `matplotlib`をGUI無し環境用に設定（`Agg`バックエンド使用）

## 発展的な使い方

### バッチ処理

複数の画像を一度に処理する場合：

```bash
for img in images/*.jpg; do
    python codespaces_ml_intro.py "$img" --output-dir "results/$(basename $img .jpg)"
done
```

### 結果の比較

異なる画像での結果を比較：

```bash
python codespaces_ml_intro.py person1.jpg --output-dir results/person1
python codespaces_ml_intro.py person2.jpg --output-dir results/person2
# 結果を比較
```

## ライセンス

教育目的で自由に使用・改変可能です。