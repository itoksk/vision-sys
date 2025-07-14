#!/bin/bash
# GitHub Codespaces用のセットアップスクリプト

echo "==================================="
echo "機械学習入門 - 環境セットアップ"
echo "==================================="

# Pythonバージョンの確認
echo -e "\n📌 Pythonバージョンを確認中..."
python3 --version

# 基本的なライブラリのインストール
echo -e "\n📦 基本ライブラリをインストール中..."
echo "これには数分かかる場合があります..."

# pip更新と基本ライブラリ
pip install --upgrade pip
pip install tensorflow==2.15.0
pip install pillow
pip install matplotlib
pip install numpy

# OpenCV
echo -e "\n📦 OpenCVをインストール中..."
pip install opencv-python

# YOLO (Ultralytics)
echo -e "\n📦 YOLOをインストール中..."
pip install ultralytics

# Gradio（アプリ開発用）
echo -e "\n🌐 Gradioをインストール中..."
pip install gradio

# 画像生成用ライブラリ（オプション）
echo -e "\n🎨 画像生成ライブラリをインストール中（オプション）..."
pip install diffusers transformers accelerate

# Jupyter関連
pip install ipython
pip install notebook

echo -e "\n✅ インストール完了！"
echo -e "\n📋 インストールされたパッケージ:"
pip list | grep -E "(tensorflow|pillow|matplotlib|opencv|ultralytics|numpy|gradio|diffusers)"

# ディレクトリ構造を表示
echo -e "\n📁 プロジェクト構造:"
echo "vision-sys/"
echo "├── 授業テキスト/        # 各授業の教材"
echo "├── sample_codes/       # Jupyterノートブック"
echo "├── codespaces/         # Codespaces用実行スクリプト"
echo "│   ├── 01_github_basics/      # GitHub基礎"
echo "│   ├── 02_ml_intro/           # 機械学習入門"
echo "│   ├── 03_teachable_machine/  # Teachable Machine"
echo "│   ├── 04_requirements/       # 要件定義"
echo "│   ├── 05_app_dev/           # アプリ開発"
echo "│   └── 06_image_generation/   # AI画像生成"
echo "└── README.md"

echo -e "\n🚀 セットアップが完了しました！"
echo -e "\n🎯 クイックスタート:"
echo "1. 機械学習入門:"
echo "   cd codespaces/02_ml_intro"
echo "   python codespaces_ml_intro.py sample.jpg"
echo ""
echo "2. Gradioアプリ:"
echo "   cd codespaces/05_app_dev"
echo "   python gradio_app.py"
echo ""
echo "3. AI画像生成:"
echo "   cd codespaces/06_image_generation"
echo "   python generate_image.py --examples"
echo ""
echo "📚 詳細は codespaces/README.md を参照してください"