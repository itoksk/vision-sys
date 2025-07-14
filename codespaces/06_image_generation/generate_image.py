#!/usr/bin/env python3
"""
AI画像生成スクリプト（Stable Diffusion）
工業高校生向け画像生成実習
"""

import os
import sys
import argparse
from datetime import datetime
import torch
from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler
import warnings
warnings.filterwarnings("ignore")

# 利用可能なモデル
MODELS = {
    "anything-v5": {
        "id": "stablediffusionapi/anything-v5",
        "name": "Anything V5（アニメ・イラスト）",
        "description": "幅広いアニメスタイルに対応",
        "prompt_tips": "best quality, ultra detailed, masterpiece"
    },
    "counterfeit-v3": {
        "id": "gsdf/Counterfeit-V3.0",
        "name": "Counterfeit V3.0（高品質アニメ）",
        "description": "美麗なアニメイラスト生成",
        "prompt_tips": "best quality, masterpiece, ultra-detailed"
    },
    "realistic-vision": {
        "id": "SG161222/Realistic_Vision_V6.0_B1_noVAE",
        "name": "Realistic Vision V6.0（写実的）",
        "description": "フォトリアリスティックな画像",
        "prompt_tips": "RAW photo, best quality, realistic, photo-realistic"
    },
    "dreamshaper": {
        "id": "Lykon/DreamShaper",
        "name": "DreamShaper（多目的）",
        "description": "幅広いスタイルに対応",
        "prompt_tips": "highly detailed, 8k, best quality"
    }
}

class ImageGenerator:
    def __init__(self, model_name="anything-v5", device="cuda"):
        """画像生成器を初期化"""
        self.model_name = model_name
        self.model_info = MODELS[model_name]
        
        # デバイスを設定
        if device == "cuda" and not torch.cuda.is_available():
            print("⚠️  GPUが利用できません。CPUを使用します（遅い可能性があります）")
            self.device = "cpu"
        else:
            self.device = device
        
        print(f"🎨 モデルを読み込み中: {self.model_info['name']}")
        print(f"   {self.model_info['description']}")
        
        # パイプラインを初期化
        self.pipe = StableDiffusionPipeline.from_pretrained(
            self.model_info['id'],
            torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
            safety_checker=None,
            requires_safety_checker=False
        )
        
        # スケジューラを設定（高速化）
        self.pipe.scheduler = DPMSolverMultistepScheduler.from_config(
            self.pipe.scheduler.config
        )
        
        # デバイスに移動
        self.pipe = self.pipe.to(self.device)
        
        # メモリ最適化
        if self.device == "cuda":
            self.pipe.enable_attention_slicing()
        
        print("✅ モデルの準備が完了しました")
    
    def generate(self, prompt, negative_prompt="", width=512, height=512, 
                 steps=20, guidance_scale=7.5, seed=None):
        """画像を生成"""
        # シードを設定
        if seed is not None:
            generator = torch.Generator(device=self.device).manual_seed(seed)
        else:
            generator = None
        
        # プロンプトを強化
        enhanced_prompt = f"{prompt}, {self.model_info['prompt_tips']}"
        
        print(f"\n🎨 画像を生成中...")
        print(f"プロンプト: {enhanced_prompt}")
        print(f"サイズ: {width}x{height}, ステップ数: {steps}")
        
        # 画像を生成
        result = self.pipe(
            prompt=enhanced_prompt,
            negative_prompt=negative_prompt,
            width=width,
            height=height,
            num_inference_steps=steps,
            guidance_scale=guidance_scale,
            generator=generator
        )
        
        return result.images[0]

def create_prompt_examples():
    """プロンプト例を表示"""
    examples = {
        "工業部品": {
            "prompt": "industrial metal part, gear mechanism, precise engineering, technical drawing style",
            "negative": "blur, rust, damage"
        },
        "傷のある部品": {
            "prompt": "metal surface with scratch, defect inspection, close-up photography, industrial quality control",
            "negative": "perfect, flawless"
        },
        "工場の風景": {
            "prompt": "modern factory interior, automated production line, industrial robots, clean environment",
            "negative": "dirty, old, abandoned"
        },
        "品質検査": {
            "prompt": "quality inspection process, worker examining parts, magnifying glass, bright lighting",
            "negative": "dark, unclear"
        },
        "AIロボット": {
            "prompt": "futuristic AI robot inspector, examining industrial parts, high-tech factory setting",
            "negative": "old technology, broken"
        }
    }
    
    print("\n📝 プロンプト例:")
    print("=" * 60)
    for name, ex in examples.items():
        print(f"\n【{name}】")
        print(f"プロンプト: {ex['prompt']}")
        print(f"ネガティブ: {ex['negative']}")
    print("=" * 60)

def main():
    """メイン処理"""
    parser = argparse.ArgumentParser(
        description="AI画像生成ツール（Stable Diffusion）"
    )
    parser.add_argument(
        "--prompt",
        type=str,
        help="生成したい画像の説明（英語推奨）"
    )
    parser.add_argument(
        "--negative",
        type=str,
        default="low quality, blurry, bad anatomy",
        help="生成したくない要素"
    )
    parser.add_argument(
        "--model",
        choices=list(MODELS.keys()),
        default="anything-v5",
        help="使用するモデル"
    )
    parser.add_argument(
        "--width",
        type=int,
        default=512,
        help="画像の幅（512推奨）"
    )
    parser.add_argument(
        "--height",
        type=int,
        default=512,
        help="画像の高さ（512推奨）"
    )
    parser.add_argument(
        "--steps",
        type=int,
        default=20,
        help="生成ステップ数（多いほど高品質だが遅い）"
    )
    parser.add_argument(
        "--seed",
        type=int,
        help="乱数シード（同じ画像を再現したい場合）"
    )
    parser.add_argument(
        "--output",
        type=str,
        help="出力ファイル名"
    )
    parser.add_argument(
        "--list-models",
        action="store_true",
        help="利用可能なモデル一覧を表示"
    )
    parser.add_argument(
        "--examples",
        action="store_true",
        help="プロンプト例を表示"
    )
    
    args = parser.parse_args()
    
    print("🎨 AI画像生成ツール")
    print("=" * 60)
    
    # モデル一覧を表示
    if args.list_models:
        print("\n利用可能なモデル:")
        for key, info in MODELS.items():
            print(f"\n{key}:")
            print(f"  名前: {info['name']}")
            print(f"  説明: {info['description']}")
        return
    
    # プロンプト例を表示
    if args.examples:
        create_prompt_examples()
        return
    
    # プロンプトが指定されていない場合
    if not args.prompt:
        print("\n⚠️  プロンプトを指定してください")
        print("\n使用例:")
        print("  python generate_image.py --prompt \"industrial robot\" --output robot.png")
        print("\nプロンプト例を見る:")
        print("  python generate_image.py --examples")
        return
    
    # 出力ファイル名を生成
    if not args.output:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        args.output = f"generated_{timestamp}.png"
    
    # 画像生成器を初期化
    generator = ImageGenerator(args.model)
    
    # 画像を生成
    try:
        image = generator.generate(
            prompt=args.prompt,
            negative_prompt=args.negative,
            width=args.width,
            height=args.height,
            steps=args.steps,
            seed=args.seed
        )
        
        # 保存
        image.save(args.output)
        print(f"\n✅ 画像を保存しました: {args.output}")
        
        # メタデータも保存
        metadata = {
            "prompt": args.prompt,
            "negative_prompt": args.negative,
            "model": args.model,
            "size": f"{args.width}x{args.height}",
            "steps": args.steps,
            "seed": args.seed,
            "timestamp": datetime.now().isoformat()
        }
        
        import json
        metadata_file = args.output.replace('.png', '_metadata.json')
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)
        
        print(f"📄 メタデータを保存: {metadata_file}")
        
    except Exception as e:
        print(f"\n❌ エラーが発生しました: {e}")
        print("\nトラブルシューティング:")
        print("1. GPUメモリ不足の場合: --width 512 --height 512 を指定")
        print("2. モデルのダウンロードが遅い場合: しばらく待ってください")
        print("3. CUDAエラーの場合: CPUモードで実行されます")

if __name__ == "__main__":
    main()