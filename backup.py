#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ব্যাকআপ স্ক্রিপ্ট - Safe UserBot
"""

import os
import shutil
import zipfile
from datetime import datetime
from utils.helpers import JSONHelper

class BackupManager:
    def __init__(self):
        self.backup_dir = 'backups'
        os.makedirs(self.backup_dir, exist_ok=True)
    
    def create_backup(self, backup_type: str = 'full') -> str:
        """ব্যাকআপ তৈরি"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_name = f"backup_{backup_type}_{timestamp}"
        backup_path = os.path.join(self.backup_dir, backup_name)
        
        os.makedirs(backup_path, exist_ok=True)
        
        if backup_type == 'full':
            # সব ডাটা ব্যাকআপ
            self._backup_data(backup_path)
            self._backup_config(backup_path)
            self._backup_sessions(backup_path)
        elif backup_type == 'data':
            # শুধু ডাটা
            self._backup_data(backup_path)
        elif backup_type == 'config':
            # শুধু কনফিগ
            self._backup_config(backup_path)
        
        # জিপ ফাইল তৈরি
        zip_filename = self._create_zip(backup_path)
        
        # টেম্প ফোল্ডার ডিলিট
        shutil.rmtree(backup_path)
        
        return zip_filename
    
    def _backup_data(self, backup_path: str):
        """ডাটা ব্যাকআপ"""
        data_dir = os.path.join(backup_path, 'data')
        shutil.copytree('data', data_dir)
    
    def _backup_config(self, backup_path: str):
        """কনফিগ ব্যাকআপ"""
        config_files = ['config.py', 'requirements.txt', 'main.py']
        for file in config_files:
            if os.path.exists(file):
                shutil.copy2(file, backup_path)
    
    def _backup_sessions(self, backup_path: str):
        """সেশন ব্যাকআপ"""
        if os.path.exists('sessions'):
            sessions_dir = os.path.join(backup_path, 'sessions')
            shutil.copytree('sessions', sessions_dir)
    
    def _create_zip(self, folder_path: str) -> str:
        """জিপ ফাইল তৈরি"""
        zip_filename = f"{folder_path}.zip"
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, folder_path)
                    zipf.write(file_path, arcname)
        
        return zip_filename
    
    def list_backups(self) -> list:
        """ব্যাকআপ লিস্ট"""
        backups = []
        if os.path.exists(self.backup_dir):
            for file in os.listdir(self.backup_dir):
                if file.endswith('.zip'):
                    backups.append({
                        'name': file,
                        'path': os.path.join(self.backup_dir, file),
                        'size': os.path.getsize(os.path.join(self.backup_dir, file)),
                        'date': datetime.fromtimestamp(
                            os.path.getmtime(os.path.join(self.backup_dir, file))
                        ).strftime('%Y-%m-%d %H:%M:%S')
                    })
        
        # সর্ট বাই ডেট
        backups.sort(key=lambda x: x['date'], reverse=True)
        return backups
    
    def restore_backup(self, backup_file: str) -> bool:
        """ব্যাকআপ থেকে রেস্টোর"""
        try:
            # কারেন্ট ফাইলস ব্যাকআপ
            temp_backup = self.create_backup('auto')
            
            # এক্সট্রাক্ট ব্যাকআপ
            with zipfile.ZipFile(backup_file, 'r') as zipf:
                zipf.extractall('restore_temp')
            
            # ফাইলস রিপ্লেস
            restore_path = 'restore_temp'
            
            # ডাটা রেস্টোর
            if os.path.exists(os.path.join(restore_path, 'data')):
                if os.path.exists('data'):
                    shutil.rmtree('data')
                shutil.copytree(os.path.join(restore_path, 'data'), 'data')
            
            # কনফিগ ফাইলস রেস্টোর
            for file in ['config.py', 'main.py']:
                src = os.path.join(restore_path, file)
                if os.path.exists(src):
                    shutil.copy2(src, '.')
            
            # ক্লিনআপ
            shutil.rmtree(restore_path)
            
            return True
        
        except Exception as e:
            print(f"Restore error: {e}")
            return False

if __name__ == "__main__":
    manager = BackupManager()
    
    print("🔧 Backup Manager - Safe UserBot")
    print("=" * 40)
    
    print("Options:")
    print("1. Create full backup")
    print("2. Create data backup")
    print("3. Create config backup")
    print("4. List backups")
    print("5. Restore from backup")
    
    choice = input("\nEnter choice (1-5): ")
    
    if choice == '1':
        backup_file = manager.create_backup('full')
        print(f"✅ Full backup created: {backup_file}")
    
    elif choice == '2':
        backup_file = manager.create_backup('data')
        print(f"✅ Data backup created: {backup_file}")
    
    elif choice == '3':
        backup_file = manager.create_backup('config')
        print(f"✅ Config backup created: {backup_file}")
    
    elif choice == '4':
        backups = manager.list_backups()
        if backups:
            print("\n📂 Available backups:")
            for i, backup in enumerate(backups, 1):
                size_mb = backup['size'] / (1024 * 1024)
                print(f"{i}. {backup['name']}")
                print(f"   Size: {size_mb:.2f} MB | Date: {backup['date']}")
        else:
            print("❌ No backups found")
    
    elif choice == '5':
        backups = manager.list_backups()
        if backups:
            print("\nSelect backup to restore:")
            for i, backup in enumerate(backups, 1):
                print(f"{i}. {backup['name']}")
            
            backup_choice = int(input("\nEnter backup number: ")) - 1
            if 0 <= backup_choice < len(backups):
                confirm = input(f"Restore {backups[backup_choice]['name']}? (yes/no): ")
                if confirm.lower() == 'yes':
                    if manager.restore_backup(backups[backup_choice]['path']):
                        print("✅ Backup restored successfully!")
                    else:
                        print("❌ Restore failed")
                else:
                    print("❌ Restore cancelled")
            else:
                print("❌ Invalid choice")
        else:
            print("❌ No backups available")
    
    else:
        print("❌ Invalid choice")