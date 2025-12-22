#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Easy Launch Script - Safe UserBot
One-click to start the bot
"""

import os
import sys
import subprocess
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

def print_banner():
    """ব্যানার প্রিন্ট"""
    print(Fore.CYAN + "=" * 60)
    print(Fore.YELLOW + "🚀 SAFE USERBOT - PROFESSIONAL & SAFE")
    print(Fore.CYAN + "=" * 60)
    print(Fore.GREEN + "👨‍💻 Developer: RANA")
    print(Fore.GREEN + "📧 Email: ranaeditz333@gmail.com")
    print(Fore.GREEN + "📱 Telegram: @rana_editz_00")
    print(Fore.CYAN + "=" * 60)
    print()

def check_requirements():
    """রিকোয়ারমেন্টস চেক"""
    print(Fore.BLUE + "🔍 Checking requirements...")
    
    # Check Python version
    if sys.version_info < (3, 7):
        print(Fore.RED + "❌ Python 3.7+ required")
        return False
    
    # Check required files
    required_files = ['config.py', 'main.py', 'requirements.txt']
    missing_files = []
    
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(Fore.RED + f"❌ Missing files: {', '.join(missing_files)}")
        print(Fore.YELLOW + "💡 Run setup.py first")
        return False
    
    print(Fore.GREEN + "✅ All requirements met")
    return True

def install_dependencies():
    """ডিপেন্ডেন্সি ইন্সটল"""
    print(Fore.BLUE + "\n📦 Installing dependencies...")
    
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print(Fore.GREEN + "✅ Dependencies installed")
            return True
        else:
            print(Fore.RED + f"❌ Failed to install dependencies")
            print(Fore.YELLOW + result.stderr)
            return False
    except Exception as e:
        print(Fore.RED + f"❌ Error: {e}")
        return False

def create_directories():
    """ডিরেক্টরি তৈরি"""
    print(Fore.BLUE + "\n📁 Creating directories...")
    
    directories = ['data', 'sessions', 'logs', 'backups']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(Fore.GREEN + f"  ✓ {directory}")
    
    return True

def check_session():
    """সেশন চেক"""
    print(Fore.BLUE + "\n🔐 Checking session...")
    
    if os.path.exists('sessions/main_account.session'):
        print(Fore.GREEN + "✅ Session file found")
        return True
    else:
        print(Fore.YELLOW + "⚠️ No session file found")
        print(Fore.YELLOW + "💡 You'll need to login on first run")
        return True

def run_bot():
    """বট রান"""
    print(Fore.BLUE + "\n🤖 Starting bot...")
    print(Fore.CYAN + "=" * 60)
    
    try:
        # Set Python path
        current_dir = os.getcwd()
        sys.path.insert(0, current_dir)
        
        # Import and run bot
        from main import SafeUserBot
        import asyncio
        
        bot = SafeUserBot()
        asyncio.run(bot.run())
        
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n👋 Bot stopped by user")
    except Exception as e:
        print(Fore.RED + f"\n❌ Error starting bot: {e}")
        return False
    
    return True

def main():
    """মেইন ফাংশন"""
    print_banner()
    
    print(Fore.YELLOW + "Select option:")
    print(Fore.CYAN + "1. First-time setup & run")
    print(Fore.CYAN + "2. Just run bot (skip setup)")
    print(Fore.CYAN + "3. Install dependencies only")
    print(Fore.CYAN + "4. Check system")
    print(Fore.CYAN + "5. Exit")
    
    choice = input(Fore.YELLOW + "\nEnter choice (1-5): " + Style.RESET_ALL)
    
    if choice == '1':
        # Full setup
        if not check_requirements():
            return
        if not install_dependencies():
            return
        if not create_directories():
            return
        if not check_session():
            return
        run_bot()
    
    elif choice == '2':
        # Just run
        if not check_requirements():
            return
        run_bot()
    
    elif choice == '3':
        # Install only
        install_dependencies()
    
    elif choice == '4':
        # System check
        check_requirements()
        create_directories()
        check_session()
        print(Fore.GREEN + "\n✅ System check completed")
    
    elif choice == '5':
        print(Fore.YELLOW + "\n👋 Goodbye!")
    
    else:
        print(Fore.RED + "❌ Invalid choice")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n\n👋 Operation cancelled")
    except Exception as e:
        print(Fore.RED + f"\n❌ Error: {e}")