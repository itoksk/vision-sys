# GitHub Codespaces 授業実行ガイド

このディレクトリには、GitHub Codespacesで各授業テキストの内容を実行するためのスクリプトが含まれています。

## 📁 ディレクトリ構成

```
codespaces/
├── README.md（本ファイル）
├── 01_github_basics/      # GitHub基礎の実習用
├── 02_ml_intro/           # 機械学習入門の実習用
├── 03_teachable_machine/  # Teachable Machine実習用
├── 04_requirements/       # 要件定義実習用
├── 05_app_dev/           # アプリ開発実習用
├── 06_image_generation/   # AI画像生成実習用
└── utils/                 # 共通ユーティリティ
```

## 🚀 クイックスタート

### 1. Codespacesの起動

1. GitHubでこのリポジトリを開く
2. 緑色の「Code」ボタンをクリック
3. 「Codespaces」タブを選択
4. 「Create codespace on main」をクリック

### 2. 環境セットアップ

Codespacesが起動したら、ターミナルで以下を実行：

```bash
# セットアップスクリプトの実行
bash setup_codespaces.sh
```

## 📚 各授業の実行方法

### 第1時：GitHub基礎

```bash
cd codespaces/01_github_basics
python github_practice.py
```

- GitHubの基本操作を体験
- リポジトリの作成、コミット、プッシュの練習

### 第2時：機械学習入門

```bash
cd codespaces/02_ml_intro

# 画像認識の体験（すべての機能を実行）
python codespaces_ml_intro.py sample.jpg

# VGG16の画像分類のみ実行
python codespaces_ml_intro.py sample.jpg --vgg16-only

# 人物検出のみ実行
python codespaces_ml_intro.py sample.jpg --detection-only

# YOLO検出をスキップ（OpenCVのみ使用）
python codespaces_ml_intro.py sample.jpg --skip-yolo

# カスタム出力ディレクトリを指定
python codespaces_ml_intro.py sample.jpg --output-dir results/experiment1

# 複数画像のバッチ処理
for img in images/*.jpg; do
    python codespaces_ml_intro.py "$img" --output-dir "results/$(basename $img .jpg)"
done
```

### 第3時：Teachable Machine

```bash
cd codespaces/03_teachable_machine

# モデルファイルを指定して実行（基本）
python test_model.py --model keras_model.h5 --labels labels.txt --image test.jpg

# サンプル画像を自動生成してテスト
python test_model.py --create-sample

# ディレクトリ内の全画像を一括処理
python test_model.py --batch-dir images/

# 結果をCSVファイルに保存
python test_model.py --batch-dir images/ --output-csv results.csv

# カスタム出力ディレクトリ
python test_model.py --image test.jpg --output-dir my_results

# 信頼度の閾値を設定（0.8以上のみ表示）
python test_model.py --image test.jpg --threshold 0.8
```

### 第4時：要件定義

```bash
cd codespaces/04_requirements

# 要件定義書テンプレートの生成
python generate_requirements.py --project-name "傷検出AI"

# インタラクティブモードで作成
python generate_requirements.py --interactive

# カスタムテンプレートを使用
python generate_requirements.py --template custom_template.md

# マークダウン形式でエクスポート
python generate_requirements.py --format markdown --output requirements.md
```

### 第5時：アプリ開発

```bash
cd codespaces/05_app_dev

# Gradioアプリの起動（基本）
python gradio_app.py

# カスタムポートで起動
python gradio_app.py --port 8080

# 公開URLを生成（外部からアクセス可能）
python gradio_app.py --share

# デバッグモードで起動
python gradio_app.py --debug

# 既存のモデルを指定して起動
python gradio_app.py --model keras_model.h5 --labels labels.txt

# バッチ処理モードのみ
python batch_process.py --input-dir images/ --output-csv results.csv

# StreamlitバージョンのUIを起動（別実装）
streamlit run streamlit_app.py
```

### 第6時：AI画像生成（新規追加）

```bash
cd codespaces/06_image_generation

# テキストから画像を生成
python generate_image.py --prompt "industrial robot working in factory"

# 複数の画像を生成
python generate_image.py --prompt "metal parts with scratches" --num-images 4

# 高解像度で生成
python generate_image.py --prompt "precision components" --size 1024x1024

# スタイルを指定
python generate_image.py --prompt "damaged gear" --style photorealistic

# 画像を編集（インペインティング）
python edit_image.py --input original.jpg --mask mask.png --prompt "remove scratch"

# 画像のバリエーションを生成
python variations.py --input reference.jpg --num-variations 5

# プロンプトのバッチ処理
python batch_generate.py --prompts-file prompts.txt --output-dir generated/
```

## 🔧 トラブルシューティング

### ポートが開かない場合

1. 「ポート」タブを確認
2. 該当ポートの「公開」設定を「Public」に変更

### メモリ不足の場合

```bash
# 使用可能なメモリを確認
free -h

# 不要なプロセスを終了
pkill -f python
```

### ライブラリインストールエラー

```bash
# pipをアップグレード
pip install --upgrade pip

# 個別にインストール
pip install -r requirements.txt --no-cache-dir
```

## 💡 便利な機能

### ファイルのアップロード・ダウンロード

```bash
# Teachable Machineのモデルファイルをアップロード（VSCode経由）
# 1. エクスプローラーで対象フォルダを右クリック
# 2. 「Upload...」を選択
# 3. keras_model.h5とlabels.txtを選択

# wgetでダウンロード
wget https://example.com/keras_model.h5
wget https://example.com/labels.txt

# 結果ファイルをダウンロード
# VSCodeエクスプローラーでファイルを右クリック → 「Download...」
```

### 画像ファイルの準備

```bash
# サンプル画像をダウンロード
wget https://github.com/your-repo/raw/main/sample_images/good_part.jpg
wget https://github.com/your-repo/raw/main/sample_images/bad_part.jpg

# 画像をリサイズ（ImageMagickを使用）
convert original.jpg -resize 640x480 resized.jpg

# 画像形式を変換
convert image.png image.jpg

# ディレクトリ内の画像を一括変換
for img in *.png; do convert "$img" "${img%.png}.jpg"; done
```

### 結果の保存と共有

```bash
# 結果をGitHubにプッシュ
git add output/
git commit -m "実習結果を追加"
git push

# 結果をZIPファイルにまとめる
zip -r results.zip output/

# 大きなファイルはGit LFSを使用
git lfs track "*.h5"
git add .gitattributes
git add keras_model.h5
git commit -m "Add model file with Git LFS"
git push
```

### プロセス管理

```bash
# 実行中のPythonプロセスを確認
ps aux | grep python

# バックグラウンドでGradioアプリを起動
nohup python gradio_app.py > gradio.log 2>&1 &

# プロセスを終了
pkill -f gradio_app.py

# ポートを使用しているプロセスを確認
lsof -i :7860
```

### 複数人での共同作業

1. Codespacesの「共有」機能を使用
2. Live Shareで画面を共有
3. 同時編集が可能

### GPUの使用（Premium機能）

```bash
# GPU対応のCodespaceを作成
# .devcontainer/devcontainer.jsonで設定

# GPUが利用可能か確認
python -c "import torch; print(torch.cuda.is_available())"
```

### よく使うエイリアス設定

```bash
# ~/.bashrcに追加すると便利
alias tm='cd ~/workspaces/vision-sys/codespaces/03_teachable_machine'
alias app='cd ~/workspaces/vision-sys/codespaces/05_app_dev'
alias gradio='python gradio_app.py'
alias results='ls -la output/'
```

## 📝 注意事項

- Codespacesは無料枠に制限があります（月60時間）
- 大きなファイルはGit LFSを使用してください
- セッション終了時は必ず保存してください

## 🆘 サポート

問題が発生した場合：

1. このREADMEのトラブルシューティングを確認
2. GitHubのIssuesに投稿
3. 先生に相談

## 🔗 関連リンク

- [GitHub Codespaces公式ドキュメント](https://docs.github.com/ja/codespaces)
- [本プロジェクトのメインREADME](../README.md)
- [授業テキスト一覧](../授業テキスト/)