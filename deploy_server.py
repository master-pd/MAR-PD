#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Server Deployment Script - Safe UserBot
Deploy bot to Linux server
"""

import os
import sys
import subprocess
import getpass
from datetime import datetime

class ServerDeployer:
    def __init__(self):
        self.server_ip = None
        self.username = None
        self.deploy_dir = "/opt/safe_userbot"
        
    def collect_info(self):
        """ইনফো সংগ্রহ"""
        print("🌐 Server Deployment Setup")
        print("="*40)
        
        self.server_ip = input("Server IP/Hostname: ")
        self.username = input("SSH Username (default: root): ") or "root"
        self.deploy_dir = input(f"Deploy directory (default: {self.deploy_dir}): ") or self.deploy_dir
        
        print(f"\n📋 Deployment Info:")
        print(f"  Server: {self.username}@{self.server_ip}")
        print(f"  Directory: {self.deploy_dir}")
        print(f"  Local dir: {os.getcwd()}")
        
        confirm = input("\nContinue? (y/N): ")
        return confirm.lower() == 'y'
    
    def run_ssh_command(self, command):
        """SSH কমান্ড রান"""
        ssh_cmd = [
            'ssh', 
            f'{self.username}@{self.server_ip}',
            command
        ]
        
        print(f"🔧 Running: {command}")
        
        try:
            result = subprocess.run(
                ssh_cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                print(f"✅ Success")
                if result.stdout.strip():
                    print(f"Output: {result.stdout.strip()}")
                return True
            else:
                print(f"❌ Failed: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            print("❌ Timeout")
            return False
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    def run_scp(self, local_path, remote_path):
        """SCP ফাইল ট্রান্সফার"""
        scp_cmd = [
            'scp',
            '-r',
            local_path,
            f'{self.username}@{self.server_ip}:{remote_path}'
        ]
        
        print(f"📤 Uploading: {local_path}")
        
        try:
            result = subprocess.run(
                scp_cmd,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                print(f"✅ Uploaded")
                return True
            else:
                print(f"❌ Failed: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            print("❌ Timeout")
            return False
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    def setup_server(self):
        """সার্ভার সেটআপ"""
        print("\n🛠️  Setting up server...")
        
        commands = [
            # Update system
            'apt-get update && apt-get upgrade -y',
            
            # Install required packages
            'apt-get install -y python3 python3-pip git screen',
            
            # Create deploy directory
            f'mkdir -p {self.deploy_dir}',
            
            # Set permissions
            f'chown -R {self.username}:{self.username} {self.deploy_dir}',
            
            # Create systemd service file
            f'cat > /etc/systemd/system/safe-userbot.service << EOF\n'
            f'[Unit]\n'
            f'Description=Safe UserBot Service\n'
            f'After=network.target\n'
            f'\n'
            f'[Service]\n'
            f'Type=simple\n'
            f'User={self.username}\n'
            f'WorkingDirectory={self.deploy_dir}\n'
            f'ExecStart=/usr/bin/python3 {self.deploy_dir}/main.py\n'
            f'Restart=always\n'
            f'RestartSec=10\n'
            f'\n'
            f'[Install]\n'
            f'WantedBy=multi-user.target\n'
            f'EOF',
            
            # Reload systemd
            'systemctl daemon-reload'
        ]
        
        for cmd in commands:
            if not self.run_ssh_command(cmd):
                return False
        
        return True
    
    def deploy_files(self):
        """ফাইল ডিপ্লয়"""
        print("\n📁 Deploying files...")
        
        # Create temp directory
        temp_dir = f"/tmp/safe_userbot_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        os.makedirs(temp_dir, exist_ok=True)
        
        # Copy project files (excluding large/unnecessary files)
        exclude_patterns = [
            '__pycache__',
            '*.pyc',
            '.git',
            'logs/*',
            'sessions/*',
            'backups/*',
            'media/*'
        ]
        
        import shutil
        
        for item in os.listdir('.'):
            if item.startswith('.'):
                continue
                
            # Check if excluded
            excluded = False
            for pattern in exclude_patterns:
                if pattern in item:
                    excluded = True
                    break
            
            if not excluded:
                dest = os.path.join(temp_dir, item)
                if os.path.isdir(item):
                    shutil.copytree(item, dest, ignore=shutil.ignore_patterns(*exclude_patterns))
                else:
                    shutil.copy2(item, dest)
        
        # Upload to server
        if not self.run_scp(f"{temp_dir}/*", f"{self.deploy_dir}/"):
            return False
        
        # Cleanup
        shutil.rmtree(temp_dir)
        
        return True
    
    def install_dependencies(self):
        """ডিপেন্ডেন্সি ইন্সটল"""
        print("\n📦 Installing dependencies...")
        
        commands = [
            f'cd {self.deploy_dir} && pip3 install --upgrade pip',
            f'cd {self.deploy_dir} && pip3 install -r requirements.txt'
        ]
        
        for cmd in commands:
            if not self.run_ssh_command(cmd):
                return False
        
        return True
    
    def start_service(self):
        """সার্ভিস শুরু"""
        print("\n🚀 Starting service...")
        
        commands = [
            'systemctl enable safe-userbot',
            'systemctl start safe-userbot',
            'systemctl status safe-userbot --no-pager'
        ]
        
        for cmd in commands:
            if not self.run_ssh_command(cmd):
                return False
        
        return True
    
    def deploy(self):
        """ডিপ্লয়মেন্ট রান"""
        if not self.collect_info():
            print("❌ Deployment cancelled")
            return False
        
        print("\n" + "="*40)
        print("🚀 Starting deployment...")
        print("="*40)
        
        steps = [
            ("Server setup", self.setup_server),
            ("File deployment", self.deploy_files),
            ("Dependencies", self.install_dependencies),
            ("Start service", self.start_service)
        ]
        
        for step_name, step_func in steps:
            print(f"\n▶️  {step_name}")
            print("-"*30)
            
            if not step_func():
                print(f"\n❌ Deployment failed at: {step_name}")
                return False
        
        print("\n" + "="*40)
        print("🎉 Deployment completed successfully!")
        print("="*40)
        
        print(f"\n📋 Deployment Summary:")
        print(f"  Server: {self.username}@{self.server_ip}")
        print(f"  Directory: {self.deploy_dir}")
        print(f"  Service: safe-userbot")
        
        print("\n🔧 Management commands:")
        print(f"  ssh {self.username}@{self.server_ip}")
        print(f"  sudo systemctl status safe-userbot")
        print(f"  sudo journalctl -u safe-userbot -f")
        
        return True

def main():
    """মেইন ডিপ্লয়মেন্ট"""
    print("="*50)
    print("🚀 SERVER DEPLOYMENT - SAFE USERBOT")
    print("="*50)
    
    deployer = ServerDeployer()
    
    try:
        deployer.deploy()
    except KeyboardInterrupt:
        print("\n\n❌ Deployment cancelled")
    except Exception as e:
        print(f"\n❌ Deployment error: {e}")

if __name__ == "__main__":
    main()