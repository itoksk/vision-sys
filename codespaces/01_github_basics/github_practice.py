#!/usr/bin/env python3
"""
GitHub基礎実習スクリプト
授業テキスト「01_GitHub基礎.md」の内容を実践
"""

import os
import sys
import subprocess
import json
from datetime import datetime

def run_command(cmd, capture_output=True):
    """コマンドを実行して結果を返す"""
    print(f"実行中: {cmd}")
    if capture_output:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ 成功")
            if result.stdout:
                print(result.stdout)
        else:
            print("❌ エラー")
            if result.stderr:
                print(result.stderr)
        return result
    else:
        subprocess.run(cmd, shell=True)
        return None

def check_git_config():
    """Git設定を確認"""
    print("\n📋 Git設定を確認中...")
    
    name_result = run_command("git config user.name")
    email_result = run_command("git config user.email")
    
    if not name_result.stdout.strip() or not email_result.stdout.strip():
        print("\n⚠️  Gitの設定が必要です！")
        print("以下のコマンドを実行してください：")
        print('git config --global user.name "あなたの名前"')
        print('git config --global user.email "your.email@example.com"')
        return False
    
    print(f"ユーザー名: {name_result.stdout.strip()}")
    print(f"メール: {email_result.stdout.strip()}")
    return True

def create_practice_repository():
    """練習用リポジトリを作成"""
    print("\n🚀 練習用リポジトリを作成します")
    
    repo_name = f"github-practice-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    os.makedirs(repo_name, exist_ok=True)
    os.chdir(repo_name)
    
    # Gitリポジトリを初期化
    run_command("git init")
    
    # README.mdを作成
    readme_content = f"""# GitHub練習用リポジトリ

作成日: {datetime.now().strftime('%Y年%m月%d日 %H:%M')}

## 目的
- GitHubの基本操作を学ぶ
- コミット、プッシュ、プルの練習

## 学習内容
- [x] リポジトリの作成
- [x] ファイルの追加
- [ ] コミットの実行
- [ ] GitHubへのプッシュ
"""
    
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme_content)
    
    print(f"✅ リポジトリ '{repo_name}' を作成しました")
    return repo_name

def practice_basic_operations():
    """基本操作の練習"""
    print("\n📚 基本操作を練習します")
    
    # 1. ステータス確認
    print("\n1️⃣ 現在の状態を確認")
    run_command("git status")
    
    # 2. ファイルを追加
    print("\n2️⃣ ファイルをステージングエリアに追加")
    run_command("git add README.md")
    run_command("git status")
    
    # 3. コミット
    print("\n3️⃣ 初回コミットを実行")
    run_command('git commit -m "初回コミット: READMEを追加"')
    
    # 4. 新しいファイルを作成
    print("\n4️⃣ 新しいファイルを作成")
    with open("hello.py", "w") as f:
        f.write('print("Hello, GitHub!")\n')
    
    run_command("git add hello.py")
    run_command('git commit -m "feat: hello.pyを追加"')
    
    # 5. ログを確認
    print("\n5️⃣ コミット履歴を確認")
    run_command("git log --oneline")

def create_gitignore():
    """.gitignoreファイルを作成"""
    print("\n📝 .gitignoreファイルを作成します")
    
    gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
.env

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# 出力ファイル
output/
results/
*.log
"""
    
    with open(".gitignore", "w") as f:
        f.write(gitignore_content)
    
    run_command("git add .gitignore")
    run_command('git commit -m "add: .gitignoreを追加"')
    print("✅ .gitignoreを作成しました")

def practice_branch_operations():
    """ブランチ操作の練習"""
    print("\n🌿 ブランチ操作を練習します")
    
    # 1. ブランチ一覧
    print("\n1️⃣ 現在のブランチを確認")
    run_command("git branch")
    
    # 2. 新しいブランチを作成
    print("\n2️⃣ 新しいブランチ 'feature-test' を作成")
    run_command("git branch feature-test")
    run_command("git branch")
    
    # 3. ブランチを切り替え
    print("\n3️⃣ ブランチを切り替え")
    run_command("git checkout feature-test")
    
    # 4. 新機能を追加
    print("\n4️⃣ 新機能を追加")
    with open("feature.txt", "w") as f:
        f.write("新機能のテストです\n")
    
    run_command("git add feature.txt")
    run_command('git commit -m "feat: 新機能を追加"')
    
    # 5. mainブランチに戻る
    print("\n5️⃣ mainブランチに戻る")
    run_command("git checkout main")
    
    # 6. マージ
    print("\n6️⃣ feature-testブランチをマージ")
    run_command("git merge feature-test")
    
    print("✅ ブランチ操作を完了しました")

def show_github_push_instructions():
    """GitHubへのプッシュ方法を表示"""
    print("\n🚀 GitHubへプッシュする方法")
    print("=" * 50)
    print("1. GitHubで新しいリポジトリを作成")
    print("   - https://github.com/new にアクセス")
    print("   - リポジトリ名を入力")
    print("   - 'Create repository'をクリック")
    print("\n2. ローカルリポジトリをGitHubに接続")
    print("   以下のコマンドを実行（URLは自分のものに置き換え）：")
    print("   git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git")
    print("\n3. プッシュ")
    print("   git push -u origin main")
    print("=" * 50)

def main():
    """メイン処理"""
    print("🎓 GitHub基礎実習を開始します")
    print("=" * 60)
    
    # Git設定を確認
    if not check_git_config():
        print("\n⚠️  Git設定を完了してから再実行してください")
        return
    
    # 練習用ディレクトリを作成
    practice_dir = os.path.join(os.getcwd(), "github_practice")
    os.makedirs(practice_dir, exist_ok=True)
    original_dir = os.getcwd()
    
    try:
        os.chdir(practice_dir)
        
        # 練習用リポジトリを作成
        repo_name = create_practice_repository()
        
        # 基本操作の練習
        practice_basic_operations()
        
        # .gitignoreの作成
        create_gitignore()
        
        # ブランチ操作の練習
        practice_branch_operations()
        
        # GitHubへのプッシュ方法を表示
        show_github_push_instructions()
        
        print(f"\n✅ 実習が完了しました！")
        print(f"作成されたリポジトリ: {os.path.join(practice_dir, repo_name)}")
        
    finally:
        os.chdir(original_dir)

if __name__ == "__main__":
    main()