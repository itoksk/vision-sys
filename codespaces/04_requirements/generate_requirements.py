#!/usr/bin/env python3
"""
要件定義書生成スクリプト
授業テキスト「04_要件定義.md」の実践
"""

import os
import json
from datetime import datetime
import argparse

def create_requirements_template(project_name, output_dir="output"):
    """要件定義書のテンプレートを作成"""
    os.makedirs(output_dir, exist_ok=True)
    
    # 要件定義書の内容
    requirements_content = f"""# {project_name} 要件定義書

作成日: {datetime.now().strftime('%Y年%m月%d日')}
作成者: [あなたの名前]

---

## 1. プロジェクト概要

### 1.1 プロジェクト名
{project_name}

### 1.2 目的
[なぜこのシステムを作るのか、解決したい課題を記載]

### 1.3 背景
[現状の問題点や開発に至った経緯を記載]

### 1.4 期待される効果
- [ ] 効果1: 
- [ ] 効果2: 
- [ ] 効果3: 

---

## 2. 利用者とシナリオ

### 2.1 想定利用者
- **主要利用者**: [誰が主に使うか]
- **利用者のスキルレベル**: [初心者/中級者/上級者]
- **利用人数**: [想定される利用者数]

### 2.2 利用シナリオ
1. [利用者]が[どんな状況で]
2. [何をしたくて]
3. [どのように使うか]

---

## 3. 機能要件

### 3.1 必須機能（Must Have）
優先度が高く、必ず実装する機能

| No. | 機能名 | 説明 | 優先度 |
|-----|--------|------|--------|
| 1 | 画像アップロード | ユーザーが画像をアップロードできる | 高 |
| 2 | 傷検出 | AIが画像から傷を検出する | 高 |
| 3 | 結果表示 | 検出結果を分かりやすく表示する | 高 |

### 3.2 あったら良い機能（Nice to Have）
時間があれば実装したい機能

| No. | 機能名 | 説明 | 優先度 |
|-----|--------|------|--------|
| 1 | 履歴保存 | 過去の検査結果を保存・閲覧 | 中 |
| 2 | レポート出力 | 検査結果をPDFで出力 | 中 |
| 3 | バッチ処理 | 複数画像を一括処理 | 低 |

### 3.3 実装しない機能（Won't Have）
今回は実装しない機能

- ユーザー認証機能
- データベース連携
- リアルタイム処理

---

## 4. 非機能要件

### 4.1 性能要件
- **処理速度**: 1枚の画像を3秒以内に処理
- **同時接続数**: 5人まで同時利用可能
- **応答時間**: ユーザー操作から1秒以内に応答

### 4.2 品質要件
- **検出精度**: 90%以上の精度で傷を検出
- **誤検出率**: 5%以下
- **使いやすさ**: 説明書なしで直感的に使える

### 4.3 セキュリティ要件
- アップロードされた画像は処理後に削除
- 外部からのアクセスは制限
- HTTPSで通信を暗号化

---

## 5. 制約条件

### 5.1 技術的制約
- **開発環境**: Google Colab / GitHub Codespaces
- **使用言語**: Python 3.8以上
- **フレームワーク**: TensorFlow, Gradio
- **AIモデル**: Teachable Machine / 独自CNN

### 5.2 リソース制約
- **開発期間**: 6時間（授業3回分）
- **開発人数**: 2-3名のチーム
- **予算**: 無料ツールのみ使用

### 5.3 その他の制約
- インターネット接続必須
- ブラウザはChrome推奨
- 画像サイズは5MB以下

---

## 6. データ要件

### 6.1 学習データ
- **良品画像**: 100枚以上
- **不良品画像**: 100枚以上
- **画像形式**: JPEG, PNG
- **画像サイズ**: 224×224ピクセル以上

### 6.2 テストデータ
- **良品画像**: 20枚
- **不良品画像**: 20枚
- **未知のパターン**: 10枚

### 6.3 データ収集方法
1. スマートフォンで撮影
2. 同じ照明条件で統一
3. 背景は単色で統一
4. 様々な角度から撮影

---

## 7. UI/UX要件

### 7.1 画面構成
1. **トップ画面**
   - タイトル表示
   - 画像アップロードボタン
   - 使い方の簡単な説明

2. **結果表示画面**
   - 元画像と検出結果を並べて表示
   - 判定結果（良品/不良品）を大きく表示
   - 信頼度をパーセントで表示

### 7.2 デザイン方針
- シンプルで分かりやすい
- 色使いは3色以内
- アイコンを活用
- レスポンシブ対応

---

## 8. テスト要件

### 8.1 単体テスト
- [ ] 画像アップロード機能
- [ ] 画像前処理機能
- [ ] AI推論機能
- [ ] 結果表示機能

### 8.2 統合テスト
- [ ] エンドツーエンドの動作確認
- [ ] エラー処理の確認
- [ ] 異常系のテスト

### 8.3 受け入れテスト
- [ ] 実際の部品画像でテスト
- [ ] ユーザーによる操作テスト
- [ ] 性能要件の確認

---

## 9. リスクと対策

| リスク | 影響度 | 発生確率 | 対策 |
|--------|--------|----------|------|
| 精度が目標に達しない | 高 | 中 | データ増強、モデル改良 |
| 開発期間の超過 | 中 | 中 | 機能を絞る、役割分担 |
| チーム内の意見相違 | 低 | 低 | 定期的な話し合い |

---

## 10. スケジュール

### 開発スケジュール
1. **第1回（2時間）**: 要件定義・設計
2. **第2回（2時間）**: データ収集・モデル作成
3. **第3回（2時間）**: アプリ実装・テスト

### マイルストーン
- [ ] 要件定義書完成
- [ ] AIモデル完成
- [ ] プロトタイプ完成
- [ ] 最終版完成

---

## 11. 用語集

| 用語 | 説明 |
|------|------|
| CNN | 畳み込みニューラルネットワーク。画像認識に適したAI |
| Teachable Machine | Googleが提供するノーコードAI開発ツール |
| Gradio | PythonでWebアプリを簡単に作れるライブラリ |
| 精度(Accuracy) | 全体の予測のうち正解した割合 |
| 信頼度(Confidence) | AIがその予測にどれだけ自信があるか |

---

## 12. 承認

| 役割 | 名前 | 承認日 | 署名 |
|------|------|--------|------|
| プロジェクトリーダー | | | |
| 開発担当者 | | | |
| 指導教員 | | | |

---

## 改訂履歴

| 版 | 日付 | 変更内容 | 変更者 |
|----|------|----------|---------|
| 1.0 | {datetime.now().strftime('%Y/%m/%d')} | 初版作成 | |
"""
    
    # ファイルに保存
    output_path = os.path.join(output_dir, f"{project_name}_要件定義書.md")
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(requirements_content)
    
    print(f"✅ 要件定義書を作成しました: {output_path}")
    
    return output_path

def create_simple_requirements(project_name, output_dir="output"):
    """簡易版要件定義書を作成"""
    os.makedirs(output_dir, exist_ok=True)
    
    simple_content = f"""# {project_name} 要件定義書（簡易版）

## 5W1Hで整理

### What（何を）
- 作るもの: {project_name}
- 主な機能: 

### Why（なぜ）
- 解決したい課題: 
- 期待される効果: 

### Who（誰が）
- 利用者: 
- 開発者: 

### When（いつ）
- 開発期間: 
- リリース予定: 

### Where（どこで）
- 利用場所: 
- 開発環境: 

### How（どのように）
- 使用技術: 
- 実装方法: 

---

## 機能一覧

### 必須機能
- [ ] 
- [ ] 
- [ ] 

### あったら良い機能
- [ ] 
- [ ] 

---

## 成功の基準
1. 
2. 
3. 
"""
    
    output_path = os.path.join(output_dir, f"{project_name}_要件定義書_簡易版.md")
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(simple_content)
    
    print(f"✅ 簡易版要件定義書を作成しました: {output_path}")
    
    return output_path

def create_checklist(output_dir="output"):
    """要件定義チェックリストを作成"""
    os.makedirs(output_dir, exist_ok=True)
    
    checklist_content = """# 要件定義チェックリスト

## 基本項目
- [ ] プロジェクトの目的は明確か？
- [ ] 解決したい課題は具体的か？
- [ ] 利用者は特定されているか？
- [ ] 期待される効果は測定可能か？

## 機能要件
- [ ] 必須機能は明確に定義されているか？
- [ ] 優先順位は決まっているか？
- [ ] 実装しない機能も明記されているか？
- [ ] 各機能の詳細は十分か？

## 非機能要件
- [ ] 性能目標は数値化されているか？
- [ ] セキュリティ要件は考慮されているか？
- [ ] 使いやすさの基準は明確か？

## 制約条件
- [ ] 技術的制約は現実的か？
- [ ] スケジュールは実現可能か？
- [ ] リソースは十分か？

## リスク
- [ ] 主要なリスクは洗い出されているか？
- [ ] 各リスクに対策があるか？
- [ ] リスクの影響度は評価されているか？

## その他
- [ ] 関係者全員が内容を理解しているか？
- [ ] 変更管理の方法は決まっているか？
- [ ] テスト方法は明確か？
"""
    
    output_path = os.path.join(output_dir, "要件定義チェックリスト.md")
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(checklist_content)
    
    print(f"✅ チェックリストを作成しました: {output_path}")
    
    return output_path

def analyze_requirements(requirements_file):
    """要件定義書を分析してフィードバック"""
    print("\n📊 要件定義書の分析")
    print("=" * 50)
    
    if not os.path.exists(requirements_file):
        print(f"❌ ファイルが見つかりません: {requirements_file}")
        return
    
    with open(requirements_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 簡単な分析
    feedback = []
    
    # 必須セクションのチェック
    required_sections = [
        "プロジェクト概要", "機能要件", "非機能要件", 
        "制約条件", "スケジュール"
    ]
    
    for section in required_sections:
        if section not in content:
            feedback.append(f"⚠️  「{section}」セクションが見つかりません")
    
    # 具体性のチェック
    if "[" in content and "]" in content:
        placeholder_count = content.count("[")
        feedback.append(f"📝 未記入の項目が{placeholder_count}個あります")
    
    # 数値目標のチェック
    numbers = ["秒", "%", "枚", "人", "MB"]
    has_numbers = any(num in content for num in numbers)
    if not has_numbers:
        feedback.append("💡 具体的な数値目標を追加することをお勧めします")
    
    # フィードバックを表示
    if feedback:
        print("改善提案:")
        for item in feedback:
            print(f"  {item}")
    else:
        print("✅ 要件定義書は十分に記載されています！")

def main():
    """メイン処理"""
    parser = argparse.ArgumentParser(
        description="要件定義書を生成・分析"
    )
    parser.add_argument(
        "--project-name",
        default="傷検出AIアプリ",
        help="プロジェクト名"
    )
    parser.add_argument(
        "--output-dir",
        default="output",
        help="出力ディレクトリ"
    )
    parser.add_argument(
        "--simple",
        action="store_true",
        help="簡易版を作成"
    )
    parser.add_argument(
        "--analyze",
        help="既存の要件定義書を分析"
    )
    parser.add_argument(
        "--checklist",
        action="store_true",
        help="チェックリストを作成"
    )
    
    args = parser.parse_args()
    
    print("📋 要件定義書ジェネレーター")
    print("=" * 60)
    
    if args.analyze:
        # 既存ファイルの分析
        analyze_requirements(args.analyze)
    
    elif args.checklist:
        # チェックリスト作成
        create_checklist(args.output_dir)
    
    else:
        # 新規作成
        if args.simple:
            create_simple_requirements(args.project_name, args.output_dir)
        else:
            create_requirements_template(args.project_name, args.output_dir)
        
        # チェックリストも作成
        create_checklist(args.output_dir)
        
        print(f"\n📁 出力先: {args.output_dir}")
        print("\n次のステップ:")
        print("1. 作成された要件定義書を開いて内容を記入")
        print("2. チームメンバーと内容を確認")
        print("3. 必要に応じて修正")

if __name__ == "__main__":
    main()