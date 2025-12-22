#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Complete File Creator for Safe UserBot
This script creates ALL files for the project
"""

import os
import json

def create_directory_structure():
    """ডিরেক্টরি স্ট্রাকচার তৈরি"""
    directories = [
        'data',
        'core',
        'utils',
        'sessions',
        'logs',
        'plugins',
        'analytics',
        'admin',
        'notifications',
        'media/photos',
        'media/stickers',
        'media/audio',
        'docs'
    ]
    
    print("📁 Creating directory structure...")
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"  ✅ Created: {directory}")
    
    print("✅ All directories created successfully!")

def create_file(file_path, content):
    """ফাইল তৈরি"""
    # ডিরেক্টরি তৈরি
    directory = os.path.dirname(file_path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    
    # ফাইল তৈরি
    with open(file_path, 'w', encoding='utf-8') as f:
        if isinstance(content, (dict, list)):
            json.dump(content, f, indent=4, ensure_ascii=False)
        else:
            f.write(content)
    
    print(f"  📄 Created: {file_path}")

def create_all_files():
    """সব ফাইল তৈরি"""
    print("🚀 Creating all files for Safe UserBot...")
    print("=" * 60)
    
    # 1. রিকোয়ারমেন্টস
    create_file('requirements.txt', """telethon==1.28.1
apscheduler==3.10.1
pytz==2022.7
python-dotenv==1.0.0
colorlog==6.7.0""")
    
    # 2. ইনস্টলেশন গাইড
    create_file('INSTALLATION.md', """# Safe UserBot - Installation Guide

## 📋 Requirements
- Python 3.7 or higher
- Telegram Account
- API ID and Hash from my.telegram.org

## 🚀 Installation Steps

### 1. Clone or Download
```bash
git clone <repository-url>
cd SAFE_USERBOT