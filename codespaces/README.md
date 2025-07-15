# GitHub Codespaces 授業実行ガイド

このディレクトリには、GitHub Codespacesで各授業テキストの内容を実行するためのスクリプトが含まれています。

## 🎯 授業の全体像

### 授業目標
工業高校生が**要件定義から始めて、実際に製造現場で使える傷検出AIアプリを開発**できるようになることを目指します。

### 対象者
- 工業高校2-3年生（プログラミング初心者）
- 全12時間（50分×12コマ）のプログラム

### 学習の流れ
```
基礎スキル習得（3時間）
    ↓
要件定義とAI活用開発（4時間）
    ↓
アプリ実装とデプロイ（3時間）
    ↓
AI画像生成と発表（2時間）
```

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

## 📚 各授業の詳細と実行方法

### 第1時：GitHub基礎を学ぶ（50分）

**学習目標**: GitHubでプロジェクト管理ができるようになる

**なぜGitHubを学ぶのか？**
- 現代のソフトウェア開発で必須のツール
- チーム開発の基礎を身につける
- 作品を世界に公開できる

**授業の流れ**:

1. **GitHubアカウントの作成（10分）**
   ```bash
   # ブラウザでGitHub.comにアクセス
   # アカウントを作成
   ```

2. **基本操作の練習（30分）**
   ```bash
   cd codespaces/01_github_basics
   python github_practice.py
   
   # 対話形式で以下を学習:
   # - リポジトリの作成
   # - ファイルの追加・編集
   # - コミットメッセージの書き方
   # - プッシュとプル
   ```

3. **プロジェクト用リポジトリの準備（10分）**
   ```bash
   # 新しいリポジトリ「damage-detection-app」を作成
   mkdir -p damage-detection-app/{models,data,src,docs}
   cd damage-detection-app
   echo "# 傷検出AIアプリ" > README.md
   git add .
   git commit -m "初期設定"
   git push
   ```

**重要な概念**:
- **リポジトリ**: プロジェクトの保管庫
- **コミット**: 変更履歴の記録
- **プッシュ**: ローカルの変更をGitHubに反映
- **プル**: GitHubの変更をローカルに反映

### 第2時：ディープラーニングで物体認識を体験（50分）

**学習目標**: AIの仕組みを理解し、画像認識を体験する

**なぜ画像認識から始めるのか？**
- AIの実力を実感できる
- 傷検出AIの基礎技術
- 視覚的で理解しやすい

**授業の流れ**:

1. **AIの基本概念を理解（10分）**
   ```bash
   cd codespaces/02_ml_intro
   
   # インタラクティブな説明を表示
   python show_ai_basics.py
   ```
   
   学ぶ内容:
   - 機械学習とは「パターンを見つける」こと
   - ディープラーニング = 人間の脳を模倣
   - 学習データの重要性

2. **VGG16で画像認識体験（20分）**
   ```bash
   # 事前学習済みモデルで1000種類の物体認識
   python codespaces_ml_intro.py sample.jpg --vgg16-only
   
   # 結果を確認
   ls output/
   # vgg16_results.png - 認識結果（トップ5）
   # feature_maps.png - AIが見ている特徴
   ```
   
   **実験してみよう**:
   ```bash
   # 色々な画像で試す
   python codespaces_ml_intro.py dog.jpg --vgg16-only
   python codespaces_ml_intro.py car.jpg --vgg16-only
   python codespaces_ml_intro.py tool.jpg --vgg16-only
   ```

3. **人物検出の体験（15分）**
   ```bash
   # YOLOとOpenCVで人物検出
   python codespaces_ml_intro.py people.jpg --detection-only
   
   # 結果を比較
   # - yolo_detection.png: 最新のAI技術
   # - opencv_detection.png: 従来の画像処理技術
   # - comparison_all_methods.png: 手法の比較
   ```

4. **工場での応用を考える（5分）**
   ```bash
   # 工業製品の画像で実験
   python codespaces_ml_intro.py gear.jpg
   python codespaces_ml_intro.py circuit.jpg
   
   # 考察：なぜ専用のAIが必要か？
   # → 一般的なAIは工業部品を知らない
   # → だからTeachable Machineで作る！
   ```

**バッチ処理（発展）**:
```bash
# 複数画像を一括処理
for img in images/*.jpg; do
    python codespaces_ml_intro.py "$img" --output-dir "results/$(basename $img .jpg)"
done

# 結果をまとめて確認
ls -la results/*/
```

### 第3時：Teachable Machineで傷検出AIを作る（50分）

**学習目標**: ノーコードで自分専用のAIモデルを作成する

**なぜTeachable Machineを使うのか？**
- プログラミング不要でAIが作れる
- 視覚的に学習過程が理解できる
- すぐに結果が確認できる

**授業の流れ**:

1. **Teachable Machineの準備（10分）**
   ```bash
   # ブラウザでTeachable Machineを開く
   # https://teachablemachine.withgoogle.com/
   
   # プロジェクトの作成:
   # 1. 「使ってみる」→「画像プロジェクト」→「標準の画像モデル」
   # 2. Class 1を「良品」に変更
   # 3. Class 2を「不良品」に変更
   ```

2. **データ収集（20分）**
   
   **撮影のコツ**:
   - 照明を一定に保つ
   - 背景をシンプルに
   - 様々な角度から撮影
   
   ```bash
   # 参考：良いデータ収集の例を確認
   cd codespaces/03_teachable_machine
   python show_data_collection_tips.py
   ```
   
   **収集目標**:
   - 良品：100枚以上
   - 不良品：100枚以上（様々な傷のパターン）

3. **モデルの学習とエクスポート（10分）**
   
   **重要：エクスポート手順**
   ```
   1. 「モデルをエクスポート」をクリック
   2. 「Tensorflow」タブを選択
   3. 「Keras」を選択
   4. 「モデルをダウンロード」をクリック
   → keras_model.h5とlabels.txtがダウンロードされる
   ```

4. **Codespacesでモデルをテスト（10分）**
   ```bash
   cd codespaces/03_teachable_machine
   
   # モデルファイルをアップロード
   # VSCodeでフォルダを右クリック→「Upload...」
   # keras_model.h5とlabels.txtを選択
   
   # テスト実行
   python test_model.py --image test.jpg
   
   # バッチテスト（複数画像）
   python test_model.py --batch-dir test_images/
   
   # 結果をCSVで保存
   python test_model.py --batch-dir test_images/ --output-csv test_results.csv
   ```

**実践的な使い方**:
```bash
# 信頼度の閾値を設定（80%以上を不良品と判定）
python test_model.py --image part.jpg --threshold 0.8

# サンプル画像で動作確認
python test_model.py --create-sample

# 詳細な分析レポートを生成
python test_model.py --batch-dir images/ --detailed-report
```

**トラブルシューティング**:
```bash
# モデルが読み込めない場合
ls -la *.h5 *.txt  # ファイル名を確認

# 精度が低い場合の対処
# → データを追加して再学習
# → 照明条件を統一
# → 背景を単純化
```

### 第4時：要件定義書を作成する（50分）

**学習目標**: 開発前の設計の重要性を理解し、要件定義書を作成する

**なぜ要件定義が重要なのか？**
- 作る前に「何を作るか」を明確にする
- チームで認識を統一できる
- 手戻りを防ぎ、開発効率が上がる

**授業の流れ**:

1. **要件定義の基本を学ぶ（15分）**
   ```bash
   cd codespaces/04_requirements
   
   # インタラクティブな学習
   python learn_requirements.py
   ```
   
   **5W1Hで整理**:
   - **Who（誰が）**: 工場の検査員
   - **What（何を）**: 金属部品の傷を検出
   - **When（いつ）**: 製造ラインで随時
   - **Where（どこで）**: 検査工程
   - **Why（なぜ）**: 品質向上と効率化
   - **How（どうやって）**: AIによる自動判定

2. **要件定義書の作成（20分）**
   ```bash
   # テンプレートを生成
   python generate_requirements.py --project-name "傷検出AI"
   
   # インタラクティブモードで詳細を入力
   python generate_requirements.py --interactive
   ```
   
   **記載する項目**:
   - プロジェクト概要
   - 機能要件（必須機能/あったら良い機能）
   - 非機能要件（性能/使いやすさ）
   - 制約条件
   - データ要件

3. **ワイヤーフレームの作成（10分）**
   ```bash
   # 画面設計ツールを起動
   python create_wireframe.py
   
   # ASCII artで簡単な画面イメージを作成
   # または、紙に手書きでもOK！
   ```
   
   **画面構成の例**:
   ```
   ┌─────────────────────────┐
   │  傷検出AIシステム        │
   ├─────────────────────────┤
   │  [画像アップロード]      │
   │  ┌─────────┐          │
   │  │         │          │
   │  │ 画像表示 │          │
   │  │         │          │
   │  └─────────┘          │
   │                        │
   │  判定結果：良品 ✓      │
   │  信頼度：95%           │
   │  [次の検査へ]          │
   └─────────────────────────┘
   ```

4. **要件の優先順位付け（5分）**
   ```bash
   # MoSCoW法で優先順位を設定
   python prioritize_requirements.py
   
   # Must have（必須）
   # Should have（あるべき）
   # Could have（あれば良い）
   # Won't have（今回は実装しない）
   ```

**実践的な要件定義**:
```bash
# 実際のプロジェクトで使える要件定義書を出力
python generate_requirements.py \
  --project-name "傷検出AI" \
  --target-accuracy 90 \
  --response-time 3 \
  --output requirements_final.md

# PDFに変換（pandocが必要）
pandoc requirements_final.md -o requirements_final.pdf
```

### 第5-6時：実用的なWebアプリを開発（100分）

**学習目標**: 要件定義に基づいて、実際に使えるWebアプリを完成させる

**なぜWebアプリにするのか？**
- どこからでもアクセス可能
- インストール不要で使いやすい
- スマートフォンからも利用可能

**授業の流れ**:

1. **第5時：基本機能の実装（50分）**

   a. **Gradioアプリの基本構造を理解（10分）**
   ```bash
   cd codespaces/05_app_dev
   
   # シンプルなデモアプリを確認
   python simple_demo.py
   
   # コードの構造を理解
   cat simple_demo.py
   ```
   
   b. **傷検出アプリの起動（15分）**
   ```bash
   # Teachable Machineのモデルをアップロード
   # keras_model.h5とlabels.txtをVSCode経由でアップロード
   
   # アプリを起動
   python gradio_app.py
   
   # ブラウザで開く（ポート7860）
   # Codespacesの「ポート」タブで確認
   ```
   
   c. **基本機能のテスト（15分）**
   ```bash
   # 画像アップロードして検査
   # 1. 「画像をアップロード」をクリック
   # 2. テスト画像を選択
   # 3. 「検査開始」をクリック
   # 4. 結果を確認
   ```
   
   d. **カスタマイズ（10分）**
   ```bash
   # 判定基準を調整
   python gradio_app.py --threshold 0.7
   
   # デバッグモードで詳細情報を表示
   python gradio_app.py --debug
   
   # ポートを変更
   python gradio_app.py --port 8080
   ```

2. **第6時：発展機能の追加（50分）**

   a. **バッチ処理機能（15分）**
   ```bash
   # 複数画像の一括処理
   python batch_process.py --input-dir test_images/ --output-csv results.csv
   
   # 結果を確認
   cat results.csv
   ```
   
   b. **履歴管理機能（15分）**
   ```bash
   # 履歴機能付きアプリを起動
   python gradio_app_with_history.py
   
   # 検査履歴の確認とエクスポート
   # UIの「検査履歴」タブで確認
   ```
   
   c. **性能評価とレポート（10分）**
   ```bash
   # テストデータで性能評価
   python evaluate_model.py --test-dir test_images/
   
   # レポートを生成
   python generate_report.py --output performance_report.pdf
   ```
   
   d. **公開設定（10分）**
   ```bash
   # 外部からアクセス可能なURLを生成
   python gradio_app.py --share
   
   # または、Codespacesのポート設定を「Public」に変更
   ```

**実践的なTips**:
```bash
# プロセスをバックグラウンドで実行
nohup python gradio_app.py > app.log 2>&1 &

# ログを確認
tail -f app.log

# エラーが出た場合
python gradio_app.py --debug 2>&1 | tee debug.log

# 別のUIフレームワークを試す（Streamlit）
pip install streamlit
streamlit run streamlit_app.py
```

**カスタマイズ例**:
```bash
# 会社のロゴを追加
python gradio_app.py --logo company_logo.png

# カスタムCSSでデザイン変更
python gradio_app.py --css custom_style.css

# 多言語対応
python gradio_app.py --language ja
```

### 第7時：AI画像生成技術を学ぶ（50分）

**学習目標**: 最新のAI画像生成技術を理解し、製造業での活用を考える

**なぜAI画像生成を学ぶのか？**
- データ不足を補える（不良品サンプルの生成）
- 新製品のデザイン検討
- 将来の重要技術

**授業の流れ**:

1. **AI画像生成の基礎（10分）**
   ```bash
   cd codespaces/06_image_generation
   
   # インタラクティブな説明
   python learn_image_generation.py
   ```
   
   **主な技術**:
   - Stable Diffusion（オープンソース、カスタマイズ可能）
   - DALL-E（OpenAI、高品質）
   - Midjourney（アート寄り、美しい画像）

2. **テキストから画像を生成（20分）**
   ```bash
   # 基本的な生成（工業用ロボット）
   python generate_image.py --prompt "industrial robot"
   
   # 製造業向けのプロンプト例を確認
   python generate_image.py --examples
   ```
   
   **利用可能なモデル**:
   ```bash
   # モデル一覧を表示
   python generate_image.py --list-models
   
   # 現在利用可能なモデル:
   # - anything-v5: アニメ・イラスト向け（デフォルト）
   # - counterfeit-v3: 高品質アニメイラスト
   # - realistic-vision: 写実的な画像
   # - dreamshaper: 多目的（幅広いスタイル）
   ```
   
   **実際の使い方**:
   ```bash
   # 1. シンプルな例
   python generate_image.py --prompt "metal gear" --output gear.png
   
   # 2. 写実的なモデルを使用
   python generate_image.py --prompt "factory interior" --model realistic-vision
   
   # 3. ネガティブプロンプトで品質向上
   python generate_image.py \
     --prompt "precision machined part" \
     --negative "blurry, low quality, damaged"
   
   # 4. 画像サイズとステップ数を調整
   python generate_image.py \
     --prompt "welding robot in action" \
     --width 768 --height 768 \
     --steps 30
   
   # 5. シード値を固定して同じ画像を再現
   python generate_image.py \
     --prompt "industrial sensor" \
     --seed 42
   ```
   
   **製造業向けプロンプトの実例**:
   ```bash
   # 品質検査シーン
   python generate_image.py \
     --prompt "quality inspection process, worker examining parts, bright lighting" \
     --model realistic-vision
   
   # 精密部品
   python generate_image.py \
     --prompt "precision gear mechanism, technical photography, macro lens" \
     --negative "rust, damage, poor quality"
   
   # 自動化ライン
   python generate_image.py \
     --prompt "modern automated production line, industrial robots, clean factory"
   
   # 傷のある部品（データ拡張用）
   python generate_image.py \
     --prompt "metal surface with scratch defect, close-up, inspection lighting" \
     --model realistic-vision
   
   # シンプルな狼アイコン
   python generate_image.py \
     --prompt "simple wolf icon, minimalist design, black and white, clean lines, vector style, flat design, logo, white background" \
     --negative "realistic, detailed fur, complex shading, 3D, photorealistic, cluttered, busy design, multiple colors, gradient"
   ```
   
   **出力ディレクトリについて**:
   ```bash
   # 生成された画像は以下に保存されます
   ls ../../generated_images/06_image_generation/
   
   # ファイル名の形式: generated_YYYYMMDD_HHMMSS.png
   ```

3. **画像の編集と修正（15分）**
   ```bash
   # 傷の除去シミュレーション
   python edit_image.py --examples
   
   # 簡単なマスクを自動作成して修正 
   python edit_image.py \
     --input damaged_part.jpg \
     --create-mask center \
     --prompt "smooth metal surface, no scratches" \
     --output repaired.jpg
   
   # マスク位置のオプション:
   # - center: 中央の円形領域
   # - top: 上部1/3
   # - bottom: 下部1/3
   # - left: 左側1/3
   # - right: 右側1/3
   
   # カスタムマスクを使用
   python edit_image.py \
     --input damaged.jpg \
     --mask mask.png \
     --prompt "perfect surface finish" \
     --negative "scratch, defect" \
     --steps 50
   ```
   
   **実践的な使用例**:
   ```bash
   # 1. 傷のある部品を修正
   python edit_image.py \
     --input scratched_gear.jpg \
     --create-mask center \
     --prompt "polished metal surface, no defects"
   
   # 2. 溶接部の仕上げ
   python edit_image.py \
     --input rough_weld.jpg \
     --mask weld_area.png \
     --prompt "smooth professional weld seam"
   
   # 3. 塗装面の修復
   python edit_image.py \
     --input chipped_paint.jpg \
     --create-mask top \
     --prompt "uniform paint finish, perfect coating"
   ```

4. **製造業での活用アイデア（5分）**
   ```bash
   # 活用例を表示
   python show_use_cases.py
   ```
   
   **実践的な活用例**:
   - 不良品データの拡張
   - 新製品のデザイン案作成
   - 取扱説明書の図解生成
   - 安全教育用の画像作成
   - カスタマイズ部品のビジュアル化

**バッチ処理と自動化**:
```bash
# 複数のプロンプトを一度に処理
cat > prompts.txt << EOF
industrial robot arm
precision bearing
metal gear mechanism
quality inspection station
EOF

# バッチ処理実行
while read prompt; do
    python generate_image.py --prompt "$prompt" --model realistic-vision
done < prompts.txt

# 複数モデルで同じプロンプトを比較
for model in anything-v5 realistic-vision dreamshaper; do
    python generate_image.py \
        --prompt "factory automation system" \
        --model $model \
        --output "comparison_${model}.png"
done

# 生成結果の確認
ls -la ../../generated_images/06_image_generation/
```

**トラブルシューティング**:
```bash
# GPUが使えない場合（CPUで実行される）
python generate_image.py --prompt "gear" --device cpu

# メモリ不足の場合
# 1. 画像サイズを小さくする
python generate_image.py --prompt "gear" --width 512 --height 512

# 2. ステップ数を減らす
python generate_image.py --prompt "gear" --steps 15

# モデルの初回ダウンロードが遅い場合
# → 待つしかない（数GB）。一度ダウンロードすればキャッシュされる

# エラーが出る場合
python generate_image.py --prompt "test" 2>&1 | tee error.log
```

### 第8時：プロジェクト発表と振り返り（50分）

**学習目標**: 開発したアプリを発表し、学習内容を振り返る

**発表の準備**:
```bash
cd ~/damage-detection-app

# 発表資料の作成
python create_presentation.py --project-dir . --output slides.pdf

# デモ動画の録画
python record_demo.py --app gradio_app.py --duration 120

# 成果物をまとめる
./package_project.sh
```

**発表内容**:
1. プロジェクト概要（2分）
2. 技術的な工夫点（3分）
3. デモンストレーション（3分）
4. 今後の改善案（2分）

**振り返りのポイント**:
- 要件定義の重要性を実感できたか
- AIツールをうまく活用できたか
- チーム開発の難しさと楽しさ
- 実際の製造現場で使えそうか

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

## 📝 授業を成功させるためのポイント

### 時間配分のコツ
- 各授業の最初5分：前回の復習
- 本編40分：新しい内容の学習と実践
- 最後5分：まとめと次回予告

### よくあるつまずきポイントと対策

1. **ファイルのアップロードがわからない**
   ```bash
   # VSCodeの場合
   # 1. エクスプローラーでフォルダを右クリック
   # 2. 「Upload...」を選択
   # 3. ファイルを選択
   
   # または、ドラッグ&ドロップでも可能
   ```

2. **モデルの精度が低い**
   - データの質を確認（照明、背景）
   - データ量を増やす（各クラス100枚以上）
   - 撮影条件を統一する

3. **Gradioアプリが表示されない**
   ```bash
   # ポート確認
   lsof -i :7860
   
   # Codespacesのポート設定を確認
   # 「ポート」タブで7860番が「Public」になっているか確認
   ```

4. **エラーメッセージが出る**
   ```bash
   # ライブラリの再インストール
   pip install -r requirements.txt --upgrade
   
   # Python環境の確認
   python --version  # 3.8以上であることを確認
   ```

### 生徒のモチベーションを保つ工夫

1. **小さな成功体験を積み重ねる**
   - 各ステップで動作確認
   - 結果を視覚的に表示

2. **実用性を意識させる**
   - 「これが実際の工場で使われたら...」
   - 身近な例で説明

3. **創造性を発揮できる場面を作る**
   - カスタマイズの余地を残す
   - 自由課題の時間を設ける

## 📝 注意事項

- Codespacesは無料枠に制限があります（月60時間）
- 大きなファイルはGit LFSを使用してください
- セッション終了時は必ず保存してください
- 定期的にGitHubにプッシュして作業を保存

## 🆘 サポート

問題が発生した場合：

1. このREADMEのトラブルシューティングを確認
2. GitHubのIssuesに投稿
3. 先生に相談

## 🔗 関連リンク

- [GitHub Codespaces公式ドキュメント](https://docs.github.com/ja/codespaces)
- [本プロジェクトのメインREADME](../README.md)
- [授業テキスト一覧](../授業テキスト/)