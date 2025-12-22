#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
আপডেট স্ক্রিপ্ট - Safe UserBot
"""

import os
import sys
import subprocess
import requests
from datetime import datetime

class Updater:
    def __init__(self):
        self.current_version = "1.0.0"
        self.update_url = "https://api.github.com/repos/username/safe-userbot/releases/latest"
        self.backup_dir = "backups"
        
    def check_for_updates(self):
        """আপডেট চেক"""
        print("🔍 Checking for updates...")
        
        try:
            response = requests.get(self.update_url, timeout=10)
            if response.status_code == 200:
                latest_release = response.json()
                latest_version = latest_release.get('tag_name', 'v1.0.0')
                
                if self._compare_versions(latest_version, self.current_version) > 0:
                    print(f"📦 New version available: {latest_version}")
                    print(f"📝 Current version: {self.current_version}")
                    
                    release_notes = latest_release.get('body', '')
                    print(f"\n📋 Release Notes:\n{release_notes}")
                    
                    return latest_version, latest_release
                else:
                    print("✅ You have the latest version")
                    return None, None
            else:
                print("❌ Could not check for updates")
                return None, None
                
        except Exception as e:
            print(f"❌ Error checking updates: {e}")
            return None, None
    
    def _compare_versions(self, v1, v2):
        """ভার্সন কম্পেয়ার"""
        # Remove 'v' prefix if exists
        v1 = v1.lstrip('v')
        v2 = v2.lstrip('v')
        
        v1_parts = list(map(int, v1.split('.')))
        v2_parts = list(map(int, v2.split('.')))
        
        # Compare each part
        for i in range(max(len(v1_parts), len(v2_parts))):
            v1_part = v1_parts[i] if i < len(v1_parts) else 0
            v2_part = v2_parts[i] if i < len(v2_parts) else 0
            
            if v1_part > v2_part:
                return 1
            elif v1_part < v2_part:
                return -1
        
        return 0
    
    def create_backup_before_update(self):
        """আপডেটের আগে ব্যাকআপ"""
        print("💾 Creating backup before update...")
        
        from backup import BackupManager
        manager = BackupManager()
        backup_file = manager.create_backup('full')
        
        if backup_file:
            print(f"✅ Backup created: {backup_file}")
            return True
        else:
            print("❌ Backup failed")
            return False
    
    def update_dependencies(self):
        """ডিপেন্ডেন্সি আপডেট"""
        print("📦 Updating dependencies...")
        
        try:
            # Install/upgrade requirements
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", "--upgrade", "-r", "requirements.txt"],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                print("✅ Dependencies updated successfully")
                return True
            else:
                print(f"❌ Failed to update dependencies:\n{result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Error updating dependencies: {e}")
            return False
    
    def download_update(self, release_data):
        """আপডেট ডাউনলোড"""
        print("⬇️ Downloading update...")
        
        try:
            # Get download URL
            assets = release_data.get('assets', [])
            if assets:
                download_url = assets[0].get('browser_download_url')
                
                # Download the update
                response = requests.get(download_url, stream=True, timeout=30)
                
                if response.status_code == 200:
                    update_file = f"update_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
                    
                    with open(update_file, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            f.write(chunk)
                    
                    print(f"✅ Update downloaded: {update_file}")
                    return update_file
                else:
                    print("❌ Failed to download update")
                    return None
            else:
                print("❌ No update file found")
                return None
                
        except Exception as e:
            print(f"❌ Error downloading update: {e}")
            return None
    
    def apply_update(self, update_file):
        """আপডেট প্রয়োগ"""
        print("🔄 Applying update...")
        
        try:
            import zipfile
            import shutil
            
            # Extract update
            with zipfile.ZipFile(update_file, 'r') as zip_ref:
                zip_ref.extractall('update_temp')
            
            # Backup current files
            self.create_backup_before_update()
            
            # Copy new files
            for item in os.listdir('update_temp'):
                src = os.path.join('update_temp', item)
                dst = os.path.join('.', item)
                
                if os.path.isdir(src):
                    if os.path.exists(dst):
                        shutil.rmtree(dst)
                    shutil.copytree(src, dst)
                else:
                    shutil.copy2(src, dst)
            
            # Cleanup
            shutil.rmtree('update_temp')
            os.remove(update_file)
            
            print("✅ Update applied successfully")
            return True
            
        except Exception as e:
            print(f"❌ Error applying update: {e}")
            return False
    
    def run_update_sequence(self):
        """আপডেট সিকুয়েন্স রান"""
        print("🚀 Starting update process...")
        print("=" * 50)
        
        # Step 1: Check for updates
        latest_version, release_data = self.check_for_updates()
        
        if not latest_version:
            return
        
        # Step 2: Ask for confirmation
        confirm = input(f"\nUpdate to version {latest_version}? (yes/no): ")
        if confirm.lower() != 'yes':
            print("❌ Update cancelled")
            return
        
        # Step 3: Create backup
        if not self.create_backup_before_update():
            confirm = input("Continue without backup? (yes/no): ")
            if confirm.lower() != 'yes':
                print("❌ Update cancelled")
                return
        
        # Step 4: Update dependencies
        if not self.update_dependencies():
            print("⚠️ Continuing with dependency update issues...")
        
        # Step 5: Download and apply update
        update_file = self.download_update(release_data)
        if update_file:
            if self.apply_update(update_file):
                print("\n" + "=" * 50)
                print("🎉 Update completed successfully!")
                print("🔄 Please restart the bot for changes to take effect.")
            else:
                print("\n❌ Update failed. Restore from backup if needed.")
        else:
            print("\n❌ Could not download update")
        
        print("=" * 50)

if __name__ == "__main__":
    updater = Updater()
    updater.run_update_sequence()