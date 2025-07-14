#!/usr/bin/env python3
"""
AI画像編集スクリプト（Inpainting）
既存画像の一部をAIで修正・編集
"""

import os
import argparse
from PIL import Image, ImageDraw
import numpy as np
import torch
from diffusers import StableDiffusionInpaintPipeline
import warnings
warnings.filterwarnings("ignore")

class ImageEditor:
    def __init__(self, device="cuda"):
        """画像編集器を初期化"""
        # デバイスを設定
        if device == "cuda" and not torch.cuda.is_available():
            print("⚠️  GPUが利用できません。CPUを使用します")
            self.device = "cpu"
        else:
            self.device = device
        
        print("🎨 Inpaintingモデルを読み込み中...")
        
        # Inpaintingパイプラインを初期化
        self.pipe = StableDiffusionInpaintPipeline.from_pretrained(
            "runwayml/stable-diffusion-inpainting",
            torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
            safety_checker=None,
            requires_safety_checker=False
        )
        
        self.pipe = self.pipe.to(self.device)
        
        # メモリ最適化
        if self.device == "cuda":
            self.pipe.enable_attention_slicing()
        
        print("✅ モデルの準備が完了しました")
    
    def edit_image(self, image_path, mask_path, prompt, 
                   negative_prompt="", steps=50, guidance_scale=7.5):
        """画像を編集"""
        # 画像とマスクを読み込む
        image = Image.open(image_path).convert("RGB")
        mask = Image.open(mask_path).convert("L")  # グレースケール
        
        # サイズを調整（512x512推奨）
        width, height = image.size
        if width != 512 or height != 512:
            print(f"📐 画像サイズを512x512に調整します（元: {width}x{height}）")
            image = image.resize((512, 512))
            mask = mask.resize((512, 512))
        
        print(f"\n🎨 画像を編集中...")
        print(f"プロンプト: {prompt}")
        
        # 編集を実行
        result = self.pipe(
            prompt=prompt,
            negative_prompt=negative_prompt,
            image=image,
            mask_image=mask,
            num_inference_steps=steps,
            guidance_scale=guidance_scale
        )
        
        return result.images[0]

def create_simple_mask(image_path, output_path, area):
    """簡単なマスクを作成"""
    image = Image.open(image_path)
    width, height = image.size
    
    # 白い背景（編集しない部分）
    mask = Image.new('L', (width, height), 255)
    draw = ImageDraw.Draw(mask)
    
    # 黒い領域（編集する部分）を描画
    if area == "center":
        # 中央に円形マスク
        center_x, center_y = width // 2, height // 2
        radius = min(width, height) // 4
        draw.ellipse(
            [center_x - radius, center_y - radius, 
             center_x + radius, center_y + radius],
            fill=0
        )
    elif area == "top":
        # 上部1/3
        draw.rectangle([0, 0, width, height // 3], fill=0)
    elif area == "bottom":
        # 下部1/3
        draw.rectangle([0, height * 2 // 3, width, height], fill=0)
    elif area == "left":
        # 左側1/3
        draw.rectangle([0, 0, width // 3, height], fill=0)
    elif area == "right":
        # 右側1/3
        draw.rectangle([width * 2 // 3, 0, width, height], fill=0)
    
    mask.save(output_path)
    print(f"✅ マスクを作成: {output_path}")
    return output_path

def create_scratch_removal_examples():
    """傷除去の例を表示"""
    examples = {
        "金属部品の傷除去": {
            "prompt": "smooth metal surface, polished, no scratches, perfect condition",
            "negative": "scratch, damage, defect, rust"
        },
        "塗装面の修復": {
            "prompt": "perfect paint finish, smooth surface, uniform color",
            "negative": "scratch, chip, peeling, damage"
        },
        "プラスチック部品の修正": {
            "prompt": "clean plastic surface, no marks, factory new condition",
            "negative": "scratch, scuff, wear, damage"
        },
        "溶接部の仕上げ": {
            "prompt": "smooth weld seam, professional finish, clean joint",
            "negative": "rough, uneven, spatter, defect"
        }
    }
    
    print("\n📝 傷除去・修正の例:")
    print("=" * 60)
    for name, ex in examples.items():
        print(f"\n【{name}】")
        print(f"プロンプト: {ex['prompt']}")
        print(f"ネガティブ: {ex['negative']}")
    print("=" * 60)

def main():
    """メイン処理"""
    parser = argparse.ArgumentParser(
        description="AI画像編集ツール（傷や欠陥の修正）"
    )
    parser.add_argument(
        "--input",
        type=str,
        help="編集する画像ファイル"
    )
    parser.add_argument(
        "--mask",
        type=str,
        help="マスク画像（編集する領域を黒、それ以外を白）"
    )
    parser.add_argument(
        "--prompt",
        type=str,
        help="編集内容の説明"
    )
    parser.add_argument(
        "--negative",
        type=str,
        default="low quality, blurry",
        help="避けたい要素"
    )
    parser.add_argument(
        "--output",
        type=str,
        help="出力ファイル名"
    )
    parser.add_argument(
        "--create-mask",
        choices=["center", "top", "bottom", "left", "right"],
        help="簡単なマスクを自動作成"
    )
    parser.add_argument(
        "--steps",
        type=int,
        default=50,
        help="編集ステップ数"
    )
    parser.add_argument(
        "--examples",
        action="store_true",
        help="傷除去の例を表示"
    )
    
    args = parser.parse_args()
    
    print("🔧 AI画像編集ツール")
    print("=" * 60)
    
    # 例を表示
    if args.examples:
        create_scratch_removal_examples()
        return
    
    # 入力チェック
    if not args.input:
        print("\n⚠️  編集する画像を指定してください")
        print("\n使用例:")
        print("  python edit_image.py --input damaged.jpg --mask mask.png --prompt \"smooth surface\"")
        print("\n簡単なマスクを自動作成:")
        print("  python edit_image.py --input damaged.jpg --create-mask center --prompt \"remove scratch\"")
        return
    
    if not os.path.exists(args.input):
        print(f"❌ 画像が見つかりません: {args.input}")
        return
    
    # マスクの準備
    if args.create_mask:
        # 自動でマスクを作成
        mask_path = args.input.replace('.', '_mask.')
        mask_path = create_simple_mask(args.input, mask_path, args.create_mask)
    elif args.mask:
        if not os.path.exists(args.mask):
            print(f"❌ マスクが見つかりません: {args.mask}")
            return
        mask_path = args.mask
    else:
        print("⚠️  マスクを指定するか、--create-maskオプションを使用してください")
        return
    
    # プロンプトチェック
    if not args.prompt:
        print("⚠️  編集内容（プロンプト）を指定してください")
        return
    
    # 出力ファイル名
    if not args.output:
        args.output = args.input.replace('.', '_edited.')
    
    # 編集器を初期化
    editor = ImageEditor()
    
    # 画像を編集
    try:
        edited_image = editor.edit_image(
            args.input,
            mask_path,
            args.prompt,
            args.negative,
            args.steps
        )
        
        # 保存
        edited_image.save(args.output)
        print(f"\n✅ 編集済み画像を保存: {args.output}")
        
        # 比較画像を作成
        original = Image.open(args.input)
        comparison = Image.new('RGB', (original.width * 2, original.height))
        comparison.paste(original, (0, 0))
        comparison.paste(edited_image.resize(original.size), (original.width, 0))
        
        comparison_path = args.output.replace('.', '_comparison.')
        comparison.save(comparison_path)
        print(f"📊 比較画像を保存: {comparison_path}")
        
    except Exception as e:
        print(f"\n❌ エラーが発生しました: {e}")

if __name__ == "__main__":
    main()