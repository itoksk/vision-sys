#!/bin/bash
# GitHub Codespaces用のセットアップスクリプト

echo "==================================="
echo "機械学習入門 - 環境セットアップ"
echo "==================================="

# Pythonバージョンの確認
echo -e "\n📌 Pythonバージョンを確認中..."
python3 --version

# 必要なライブラリのインストール
echo -e "\n📦 必要なライブラリをインストール中..."
echo "これには数分かかる場合があります..."

# 基本的なライブラリ
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

# 追加の依存関係
pip install ipython
pip install notebook

echo -e "\n✅ インストール完了！"
echo -e "\n📋 インストールされたパッケージ:"
pip list | grep -E "(tensorflow|pillow|matplotlib|opencv|ultralytics|numpy)"

echo -e "\n🚀 セットアップが完了しました！"
echo -e "\n次のコマンドで実行できます:"
echo "python3 codespaces_ml_intro.py <画像ファイルパス>"
echo -e "\n例:"
echo "python3 codespaces_ml_intro.py sample.jpg"