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
# 画像認識の体験
python codespaces_ml_intro.py sample_image.jpg

# 特徴マップの可視化
python codespaces_ml_intro.py sample_image.jpg --vgg16-only
```

### 第3時：Teachable Machine

```bash
cd codespaces/03_teachable_machine
# Teachable Machineモデルのテスト
python test_model.py --model-path path/to/model.h5
```

### 第4時：要件定義

```bash
cd codespaces/04_requirements
# 要件定義書テンプレートの生成
python generate_requirements.py --project-name "傷検出AI"
```

### 第5時：アプリ開発

```bash
cd codespaces/05_app_dev
# Gradioアプリの起動
python gradio_app.py
```

### 第6時：AI画像生成（新規追加）

```bash
cd codespaces/06_image_generation
# テキストから画像を生成
python generate_image.py --prompt "工場の部品" --output output.png

# 画像編集
python edit_image.py --input input.png --mask mask.png --prompt "傷を修正"
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

### 結果の保存と共有

```bash
# 結果をGitHubにプッシュ
git add output/
git commit -m "実習結果を追加"
git push
```

### 複数人での共同作業

1. Codespacesの「共有」機能を使用
2. Live Shareで画面を共有
3. 同時編集が可能

### GPUの使用（Premium機能）

```bash
# GPU対応のCodespaceを作成
# .devcontainer/devcontainer.jsonで設定
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