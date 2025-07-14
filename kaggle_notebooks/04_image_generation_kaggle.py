#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
AI画像生成 - Kaggle Notebook版
Stable Diffusionを使った製造業向け画像生成
"""

import os
import torch
from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler
from diffusers import StableDiffusionInpaintPipeline
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
from datetime import datetime
import json

print("🎨 AI画像生成 - Kaggle Notebook版")
print("=" * 50)

# Kaggleディレクトリ設定
KAGGLE_WORKING_DIR = '/kaggle/working'

# GPU確認
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"💻 使用デバイス: {device}")
if device == "cuda":
    print(f"GPU情報: {torch.cuda.get_device_name(0)}")

# 利用可能なモデル（軽量版）
MODELS = {
    "stable-diffusion": {
        "id": "CompVis/stable-diffusion-v1-4",
        "name": "Stable Diffusion v1.4",
        "description": "汎用的な画像生成"
    },
    "anything-v3": {
        "id": "Linaqruf/anything-v3.0",
        "name": "Anything V3",
        "description": "アニメ・イラスト風"
    }
}

class ImageGenerator:
    def __init__(self, model_name="stable-diffusion"):
        """画像生成器を初期化"""
        self.model_name = model_name
        self.model_info = MODELS[model_name]
        
        print(f"\n🎨 モデルを読み込み中: {self.model_info['name']}")
        print(f"   {self.model_info['description']}")
        print("   初回は時間がかかります（モデルダウンロード）...")
        
        try:
            # パイプラインを初期化
            self.pipe = StableDiffusionPipeline.from_pretrained(
                self.model_info['id'],
                torch_dtype=torch.float16 if device == "cuda" else torch.float32,
                safety_checker=None,
                requires_safety_checker=False
            )
            
            # スケジューラを高速化
            self.pipe.scheduler = DPMSolverMultistepScheduler.from_config(
                self.pipe.scheduler.config
            )
            
            # デバイスに移動
            self.pipe = self.pipe.to(device)
            
            # メモリ最適化
            if device == "cuda":
                self.pipe.enable_attention_slicing()
                self.pipe.enable_vae_slicing()
            
            print("✅ モデルの準備完了")
            
        except Exception as e:
            print(f"❌ モデル読み込みエラー: {e}")
            self.pipe = None
    
    def generate(self, prompt, negative_prompt="", 
                 width=512, height=512, steps=20, 
                 guidance_scale=7.5, seed=None):
        """画像を生成"""
        if self.pipe is None:
            print("❌ モデルが読み込まれていません")
            return None
        
        # シード設定
        if seed is not None:
            generator = torch.Generator(device=device).manual_seed(seed)
        else:
            generator = None
        
        print(f"\n🎨 画像生成中...")
        print(f"プロンプト: {prompt}")
        print(f"サイズ: {width}x{height}, ステップ: {steps}")
        
        try:
            # 画像生成
            with torch.autocast(device):
                result = self.pipe(
                    prompt=prompt,
                    negative_prompt=negative_prompt,
                    width=width,
                    height=height,
                    num_inference_steps=steps,
                    guidance_scale=guidance_scale,
                    generator=generator
                )
            
            image = result.images[0]
            
            # メタデータを追加
            metadata = {
                "prompt": prompt,
                "negative_prompt": negative_prompt,
                "model": self.model_name,
                "size": f"{width}x{height}",
                "steps": steps,
                "guidance_scale": guidance_scale,
                "seed": seed,
                "timestamp": datetime.now().isoformat()
            }
            
            return image, metadata
            
        except Exception as e:
            print(f"❌ 生成エラー: {e}")
            return None, None

def create_manufacturing_prompts():
    """製造業向けプロンプトの例"""
    prompts = {
        "品質検査": {
            "prompt": "quality inspection process in modern factory, worker examining metal parts with magnifying glass, bright LED lighting, clean environment, professional photography",
            "negative": "blurry, dark, dirty, unsafe"
        },
        "自動化ライン": {
            "prompt": "automated production line, industrial robots assembling products, blue and white color scheme, high tech factory, wide angle shot",
            "negative": "old, broken, rusty, manual labor"
        },
        "精密部品": {
            "prompt": "precision machined metal components, gear mechanisms, technical photography, macro lens, perfect surface finish, engineering drawing style",
            "negative": "rough, damaged, dirty, low quality"
        },
        "クリーンルーム": {
            "prompt": "semiconductor cleanroom facility, workers in white protective suits, advanced equipment, sterile environment, futuristic atmosphere",
            "negative": "contaminated, dirty, casual clothing"
        },
        "溶接作業": {
            "prompt": "professional welding operation, bright sparks, safety equipment, industrial setting, dramatic lighting, high speed photography",
            "negative": "unsafe, amateur, poor quality weld"
        }
    }
    return prompts

def generate_prompt_variations(base_prompt, variations=3):
    """プロンプトのバリエーションを生成"""
    styles = [
        "photorealistic, 8k, highly detailed",
        "technical drawing style, blueprint, precise",
        "professional photography, studio lighting",
        "cinematic, dramatic lighting, wide angle",
        "macro photography, extreme close-up, sharp focus"
    ]
    
    varied_prompts = []
    for i in range(variations):
        style = styles[i % len(styles)]
        varied_prompt = f"{base_prompt}, {style}"
        varied_prompts.append(varied_prompt)
    
    return varied_prompts

def create_comparison_grid(images, prompts, save_path=None):
    """複数の生成画像を比較表示"""
    n_images = len(images)
    cols = min(3, n_images)
    rows = (n_images + cols - 1) // cols
    
    fig, axes = plt.subplots(rows, cols, figsize=(cols * 4, rows * 4))
    
    if n_images == 1:
        axes = [axes]
    else:
        axes = axes.flatten() if rows > 1 else axes
    
    for i, (img, prompt) in enumerate(zip(images, prompts)):
        if i < len(axes):
            axes[i].imshow(img)
            axes[i].set_title(prompt[:50] + "..." if len(prompt) > 50 else prompt, 
                            fontsize=10, wrap=True)
            axes[i].axis('off')
    
    # 余分な軸を非表示
    for i in range(len(images), len(axes)):
        axes[i].axis('off')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
    
    plt.show()
    return fig

def batch_generate(generator, prompt_dict, save_results=True):
    """複数のプロンプトで一括生成"""
    results = []
    images = []
    prompts_used = []
    
    for name, prompt_info in prompt_dict.items():
        print(f"\n📸 生成中: {name}")
        
        image, metadata = generator.generate(
            prompt=prompt_info['prompt'],
            negative_prompt=prompt_info['negative'],
            width=512,
            height=512,
            steps=20
        )
        
        if image:
            # 保存
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{name.replace(' ', '_')}_{timestamp}.png"
            filepath = os.path.join(KAGGLE_WORKING_DIR, filename)
            image.save(filepath)
            
            results.append({
                'name': name,
                'filename': filename,
                'metadata': metadata
            })
            
            images.append(image)
            prompts_used.append(name)
            
            print(f"✅ 保存: {filename}")
    
    # 比較グリッドを作成
    if images:
        grid_path = os.path.join(KAGGLE_WORKING_DIR, "comparison_grid.png")
        create_comparison_grid(images, prompts_used, grid_path)
    
    # メタデータを保存
    if save_results and results:
        meta_path = os.path.join(KAGGLE_WORKING_DIR, "generation_metadata.json")
        with open(meta_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"\n📄 メタデータ保存: {meta_path}")
    
    return results

def create_inpainting_demo():
    """インペインティング（画像修正）のデモ"""
    print("\n🔧 画像修正デモ")
    
    # サンプル画像とマスクを作成
    base_image = Image.new('RGB', (512, 512), color='lightgray')
    draw = ImageDraw.Draw(base_image)
    
    # 金属部品のような形を描画
    draw.rectangle([100, 100, 400, 400], fill='silver')
    draw.ellipse([200, 200, 300, 300], fill='darkgray')
    
    # 傷を追加
    draw.line([(150, 150), (350, 350)], fill='black', width=5)
    draw.line([(150, 350), (350, 150)], fill='black', width=5)
    
    # マスク（修正したい部分）
    mask = Image.new('L', (512, 512), color='white')
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.line([(150, 150), (350, 350)], fill='black', width=20)
    mask_draw.line([(150, 350), (350, 150)], fill='black', width=20)
    
    # 表示
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
    ax1.imshow(base_image)
    ax1.set_title("元画像（傷あり）")
    ax1.axis('off')
    
    ax2.imshow(mask, cmap='gray')
    ax2.set_title("修正マスク（黒い部分を修正）")
    ax2.axis('off')
    
    plt.tight_layout()
    plt.show()
    
    # ファイルとして保存
    base_path = os.path.join(KAGGLE_WORKING_DIR, "sample_damaged.png")
    mask_path = os.path.join(KAGGLE_WORKING_DIR, "sample_mask.png")
    base_image.save(base_path)
    mask.save(mask_path)
    
    print(f"✅ サンプル画像を保存:")
    print(f"  - 元画像: {base_path}")
    print(f"  - マスク: {mask_path}")
    
    return base_path, mask_path

def main():
    """メイン処理"""
    print("\n🚀 AI画像生成を開始")
    
    # 画像生成器を初期化
    generator = ImageGenerator("stable-diffusion")
    
    if generator.pipe is None:
        print("⚠️ モデルの読み込みに失敗しました")
        return
    
    # 製造業向けプロンプトを取得
    prompts = create_manufacturing_prompts()
    
    # インタラクティブメニュー
    print("\n📋 実行オプション:")
    print("1. 製造業サンプルを一括生成")
    print("2. カスタムプロンプトで生成")
    print("3. 画像修正デモ")
    
    # デフォルトで1を実行
    choice = "1"
    
    if choice == "1":
        # サンプルを一括生成
        print("\n🏭 製造業サンプルを生成します")
        results = batch_generate(generator, prompts)
        
        print(f"\n✅ {len(results)}枚の画像を生成しました")
        print(f"保存先: {KAGGLE_WORKING_DIR}")
        
    elif choice == "2":
        # カスタムプロンプト
        custom_prompt = "modern factory interior with advanced robotics"
        print(f"\n🎨 カスタム生成: {custom_prompt}")
        
        image, metadata = generator.generate(
            prompt=custom_prompt,
            negative_prompt="old, dirty, dangerous",
            width=512,
            height=512,
            steps=30
        )
        
        if image:
            save_path = os.path.join(KAGGLE_WORKING_DIR, "custom_generation.png")
            image.save(save_path)
            print(f"✅ 保存: {save_path}")
            
            plt.figure(figsize=(8, 8))
            plt.imshow(image)
            plt.title(custom_prompt)
            plt.axis('off')
            plt.show()
    
    elif choice == "3":
        # 画像修正デモ
        create_inpainting_demo()
    
    print("\n📝 次のステップ:")
    print("- 生成した画像をダウンロードして使用")
    print("- プロンプトを調整してより良い結果を得る")
    print("- seed値を固定して同じ画像を再現")

# インタラクティブ関数
def quick_generate(prompt, negative="low quality, blurry", size=512, steps=20):
    """簡単な画像生成関数"""
    generator = ImageGenerator("stable-diffusion")
    
    if generator.pipe:
        image, metadata = generator.generate(
            prompt=prompt,
            negative_prompt=negative,
            width=size,
            height=size,
            steps=steps
        )
        
        if image:
            # 表示
            plt.figure(figsize=(8, 8))
            plt.imshow(image)
            plt.title(prompt[:80] + "..." if len(prompt) > 80 else prompt)
            plt.axis('off')
            plt.show()
            
            # 保存
            filename = f"generated_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            filepath = os.path.join(KAGGLE_WORKING_DIR, filename)
            image.save(filepath)
            print(f"💾 保存: {filepath}")
            
            return image
    
    return None

# スクリプト実行
if __name__ == "__main__":
    main()

# 使用方法
print("\n💡 クイック生成:")
print('quick_generate("industrial robot in action")')
print('quick_generate("precision mechanical parts", negative="damaged, dirty", steps=30)')