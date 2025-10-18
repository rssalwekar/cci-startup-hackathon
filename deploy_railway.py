#!/usr/bin/env python3
"""
Quick Railway deployment script
"""
import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"Error: {e.stderr}")
        return False

def main():
    print("🚀 AI Interview Platform - Railway Deployment")
    print("=" * 50)
    
    # Check if git is initialized
    if not os.path.exists('.git'):
        print("📦 Initializing git repository...")
        if not run_command("git init", "Initializing git"):
            return
    
    # Check if we have a remote
    result = subprocess.run("git remote -v", shell=True, capture_output=True, text=True)
    if not result.stdout.strip():
        print("\n🔗 You need to add a GitHub remote first:")
        print("1. Create a new repository on GitHub")
        print("2. Run: git remote add origin https://github.com/yourusername/your-repo-name.git")
        print("3. Run: git push -u origin main")
        print("\nThen run this script again!")
        return
    
    # Add all files and commit
    print("\n📝 Adding files to git...")
    run_command("git add .", "Adding files")
    run_command("git commit -m 'Deploy to Railway'", "Committing changes")
    
    # Push to GitHub
    print("\n🚀 Pushing to GitHub...")
    if run_command("git push", "Pushing to GitHub"):
        print("\n🎉 Code pushed to GitHub!")
        print("\n📋 Next steps:")
        print("1. Go to https://railway.app")
        print("2. Sign up with GitHub")
        print("3. Click 'New Project' → 'Deploy from GitHub repo'")
        print("4. Select your repository")
        print("5. Add environment variables:")
        print("   - KRONOS_API_KEY")
        print("   - ELEVEN_LABS_API_KEY")
        print("   - SECRET_KEY (generate a new Django secret key)")
        print("6. Railway will auto-deploy and give you an HTTPS URL!")
        print("\n🔗 Your app will be available at: https://your-app-name.railway.app")
        print("✅ The HTTPS domain will resolve microphone permission issues!")

if __name__ == "__main__":
    main()
