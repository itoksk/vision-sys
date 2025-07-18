# 第3時：Teachable Machineで自分のAIモデルを作ろう

## 🎯 今日の目標
Teachable Machineを使って、実際に工場で使える「良品/不良品」判定AIを作る！

---

## 📝 Teachable Machineとは？

### プログラミング不要でAIが作れる！

**Teachable Machine**は、Googleが提供する無料のAI作成ツールです。

特徴：
- 🖱️ ドラッグ＆ドロップで簡単操作
- 📸 Webカメラですぐに画像収集
- ⚡ リアルタイムで学習結果を確認
- 💾 作ったモデルをダウンロード可能

---

## 🚀 Teachable Machineを始めよう

### ステップ1：サイトにアクセス

1. **Teachable Machineを開く**
   - https://teachablemachine.withgoogle.com/
   - 「使ってみる」をクリック

2. **新しいプロジェクトを作成**
   - 「画像プロジェクト」を選択
   - 「標準の画像モデル」を選択

### ステップ2：画面の説明

```
┌─────────────────────────────────────┐
│  Class 1  │  Class 2  │ + Add Class │  ← クラス（分類）
├───────────┼───────────┼─────────────┤
│           │           │             │
│  画像追加  │  画像追加  │             │  ← データ収集エリア
│           │           │             │
└───────────┴───────────┴─────────────┘
         ↓
    [トレーニング]  ← 学習開始ボタン
         ↓
    プレビューエリア  ← 結果確認
```

---

## 🏭 工具判別AIを作ってみよう（練習）

### 準備するもの
- ドライバー（プラス/マイナス）
- レンチ
- その他の工具

### ステップ1：クラスの設定

1. **Class 1の名前を変更**
   - 鉛筆アイコンをクリック
   - 「ドライバー」と入力

2. **Class 2の名前を変更**
   - 「レンチ」と入力

3. **Class 3を追加**（必要に応じて）
   - 「Add a class」をクリック
   - 「その他」と入力

### ステップ2：画像の収集

#### 方法1：Webカメラで撮影

1. **「Webcam」をクリック**
2. **「Hold to Record」を長押し**
   - 角度を変えながら撮影
   - 各クラス50枚以上が目安

#### 方法2：画像をアップロード

1. **「Upload」をクリック**
2. **画像を選択またはドラッグ＆ドロップ**

### 撮影のコツ 📸

```
✅ 良い撮影方法：
- いろんな角度から
- 背景を変える
- 明るさを変える
- 距離を変える

❌ 避けるべき撮影：
- 同じ角度ばかり
- 暗すぎる/明るすぎる
- ピンボケ
- 一部しか写っていない
```

### ステップ3：モデルの学習

1. **「トレーニング」ボタンをクリック**
   - 自動で学習が始まる
   - 1-2分程度で完了

2. **プレビューで確認**
   - カメラに工具をかざす
   - リアルタイムで判定結果が表示

---

## 🔧 本番：傷検出AIを作ろう

### 準備するもの
- 良品の金属部品（10個以上）
- 傷のある不良品（10個以上）
- 撮影ボックス（照明を一定に）

### ステップ1：プロジェクトの設定

1. **新しいプロジェクトを作成**
2. **クラス名を設定**
   - Class 1: 「良品」
   - Class 2: 「不良品（傷あり）」

### ステップ2：高品質なデータ収集

#### 撮影環境の準備

```
┌─────────────────┐
│     照明↓       │
│  ┌─────────┐  │
│  │         │  │
│  │  部品    │  │  ← 撮影ボックス
│  │         │  │
│  └─────────┘  │
│    カメラ↑      │
└─────────────────┘
```

#### データ収集のポイント

**良品の撮影**
- 表面がきれいな部品
- 各面を撮影（表、裏、側面）
- 1個につき5-10枚
- 合計100枚以上

**不良品の撮影**
- 様々な傷のパターン
  - 小さな傷
  - 大きな傷
  - 複数の傷
  - 打痕
- 傷の位置も変える
- 合計100枚以上

### ステップ3：学習と調整

1. **トレーニング実行**
2. **詳細設定**（Advanced）
   ```
   Epochs: 50 → 100に増やす（精度向上）
   Batch Size: 16（そのまま）
   Learning Rate: 0.001（そのまま）
   ```

3. **精度の確認**
   - 新しい部品で実際にテスト
   - 間違えやすいパターンを記録

---

## 💾 モデルのエクスポート

### ステップ1：モデルをダウンロード

1. **「モデルをエクスポート」をクリック**
2. **「Tensorflow」タブを選択**
3. **「Keras」を選択**
4. **「モデルをダウンロード」をクリック**

### ステップ2：ファイルの確認

ダウンロードされるファイル：
```
converted_keras.zip
├── keras_model.h5    # モデル本体
└── labels.txt        # クラス名のリスト
```

### ステップ3：GitHubに保存

1. **ZIPファイルを解凍**
2. **GitHubのmodelsフォルダにアップロード**
   - リポジトリを開く
   - `models`フォルダに移動
   - 「Upload files」でアップロード

---

## 🧪 モデルの性能テスト

### テスト用シートの作成

| No. | 実際 | 予測 | 正解？ | メモ |
|-----|------|------|--------|------|
| 1 | 良品 | 良品 | ○ | |
| 2 | 不良品 | 不良品 | ○ | |
| 3 | 良品 | 不良品 | × | 光の反射を傷と誤認 |
| ... | | | | |

### 精度の計算

```
精度 = 正解数 ÷ 全体数 × 100

例：18個正解/20個中 = 90%
```

---

## 💡 精度を上げるテクニック

### 1. データの質を上げる

```python
# 良いデータの条件
- 照明が一定
- ピントが合っている
- 部品全体が写っている
- 背景がシンプル
```

### 2. データのバランス

```
良品：100枚
不良品：100枚  ← 同じくらいの枚数に
```

### 3. 難しいケースを追加

- 境界線上のケース（微妙な傷）
- 誤認しやすいパターン
- 様々な種類の不良

### 4. クラスを細分化

```
変更前：
- 良品
- 不良品

変更後：
- 良品
- 小さな傷
- 大きな傷
- 打痕
```

---

## 🎮 発展課題

### 課題1：マルチクラス分類

3つ以上のクラスで分類：
- 良品
- 傷（小）
- 傷（大）
- 汚れ
- その他の不良

### 課題2：混同行列を作る

|  | 予測:良品 | 予測:不良品 |
|--|----------|------------|
| 実際:良品 | 9 | 1 |
| 実際:不良品 | 2 | 8 |

### 課題3：閾値の調整を考える

- 厳しく判定：不良品の見逃しを防ぐ
- 緩く判定：良品を不良品と誤認するのを防ぐ

---

## 🤔 よくある質問

**Q: 何枚くらい画像が必要？**
A: 最低でも各クラス50枚。100枚以上あると安定します。

**Q: 学習が終わらない**
A: 画像が多すぎるかも。まずは少なめで試してから増やしましょう。

**Q: 精度が低い**
A: データの質を確認。特に照明と撮影角度を統一することが大事。

**Q: エクスポートしたモデルが大きい**
A: 画像の枚数とサイズに比例。必要最小限のデータで学習しましょう。

---

## 📊 今日のまとめ

### できるようになったこと
- [ ] Teachable Machineの基本操作
- [ ] データ収集の方法
- [ ] モデルの学習と調整
- [ ] モデルのエクスポート

### 重要なポイント
1. **データの質 > データの量**
2. **撮影環境の統一が成功の鍵**
3. **実際に使う環境でテストする**

### 次回予告
次回は「要件定義」について学びます。
作りたいアプリの仕様を明確にして、開発の準備をしましょう！

---

## 🏠 宿題

1. **モデルの改良**
   - 今日作ったモデルの精度を記録
   - データを追加して再学習
   - 精度がどう変わったか比較

2. **レポート作成**
   ```markdown
   # Teachable Machine実験レポート
   
   ## 作成したモデル
   - クラス数：
   - 各クラスの画像枚数：
   - 学習時間：
   
   ## 結果
   - テスト精度：
   - うまくいった点：
   - 改善が必要な点：
   
   ## 考察
   - なぜこの精度になったか
   - どうすれば改善できるか
   ```

3. **次回の準備**
   - 実際に作りたいアプリのアイデアを3つ考える

**提出物**:
- keras_model.h5とlabels.txt（GitHubにアップロード）
- 実験レポート（Markdownファイル）