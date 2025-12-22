#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Bot Controller - Safe UserBot
Control bot status, restart, stop, etc.
"""

import os
import sys
import time
import signal
import subprocess
import threading
from datetime import datetime

class BotController:
    def __init__(self):
        self.process = None
        self.log_file = f"logs/bot_controller_{datetime.now().strftime('%Y%m%d')}.log"
        self.status_file = "data/bot_status.json"
        
    def start(self):
        """বট শুরু"""
        if self.is_running():
            print("❌ Bot is already running")
            return False
        
        print("🚀 Starting bot...")
        
        # Start bot in background
        self.process = subprocess.Popen(
            [sys.executable, "main.py"],
            stdout=open(self.log_file, 'a'),
            stderr=subprocess.STDOUT
        )
        
        # Save PID
        self.save_status({
            'pid': self.process.pid,
            'start_time': datetime.now().isoformat(),
            'status': 'running'
        })
        
        print(f"✅ Bot started with PID: {self.process.pid}")
        return True
    
    def stop(self):
        """বট থামানো"""
        if not self.is_running():
            print("❌ Bot is not running")
            return False
        
        print("🛑 Stopping bot...")
        
        # Send SIGTERM
        self.process.terminate()
        
        try:
            # Wait for graceful shutdown
            self.process.wait(timeout=10)
            print("✅ Bot stopped gracefully")
        except subprocess.TimeoutExpired:
            # Force kill
            self.process.kill()
            print("⚠️ Bot force stopped")
        
        self.save_status({
            'stop_time': datetime.now().isoformat(),
            'status': 'stopped'
        })
        
        return True
    
    def restart(self):
        """বট রিস্টার্ট"""
        print("🔄 Restarting bot...")
        
        if self.is_running():
            self.stop()
            time.sleep(2)
        
        return self.start()
    
    def is_running(self):
        """চেক বট চলছে কিনা"""
        if self.process and self.process.poll() is None:
            return True
        
        # Check from status file
        status = self.load_status()
        if status and status.get('status') == 'running':
            pid = status.get('pid')
            if pid and self.check_pid(pid):
                return True
        
        return False
    
    def check_pid(self, pid):
        """PID চেক"""
        try:
            os.kill(pid, 0)
            return True
        except OSError:
            return False
    
    def save_status(self, data):
        """স্ট্যাটাস সেভ"""
        status = self.load_status() or {}
        status.update(data)
        
        os.makedirs('data', exist_ok=True)
        with open(self.status_file, 'w') as f:
            import json
            json.dump(status, f, indent=2)
    
    def load_status(self):
        """স্ট্যাটাস লোড"""
        try:
            with open(self.status_file, 'r') as f:
                import json
                return json.load(f)
        except:
            return None
    
    def get_status(self):
        """বট স্ট্যাটাস"""
        if self.is_running():
            status = self.load_status()
            if status:
                start_time = status.get('start_time', 'Unknown')
                pid = status.get('pid', 'Unknown')
                return f"✅ RUNNING (PID: {pid}, Started: {start_time})"
            return "✅ RUNNING"
        else:
            return "❌ STOPPED"
    
    def view_logs(self, lines=50):
        """লগ দেখা"""
        if not os.path.exists(self.log_file):
            print("❌ No log file found")
            return
        
        print(f"📋 Last {lines} lines of log:")
        print("="*60)
        
        with open(self.log_file, 'r') as f:
            log_lines = f.readlines()
        
        for line in log_lines[-lines:]:
            print(line.rstrip())
    
    def monitor(self, interval=10):
        """মনিটর মোড"""
        print("👁️  Starting monitor mode...")
        print("Press Ctrl+C to stop\n")
        
        try:
            while True:
                status = self.get_status()
                timestamp = datetime.now().strftime('%H:%M:%S')
                print(f"[{timestamp}] {status}")
                
                # Check for errors
                if os.path.exists(self.log_file):
                    with open(self.log_file, 'r') as f:
                        logs = f.readlines()
                        if logs and "ERROR" in logs[-1]:
                            print("⚠️  Error detected in logs!")
                
                time.sleep(interval)
        except KeyboardInterrupt:
            print("\n👋 Monitor stopped")

def main():
    """মেইন কন্ট্রোলার"""
    controller = BotController()
    
    print("="*50)
    print("🤖 BOT CONTROLLER - SAFE USERBOT")
    print("="*50)
    
    while True:
        print("\nOptions:")
        print("1. Start bot")
        print("2. Stop bot")
        print("3. Restart bot")
        print("4. Check status")
        print("5. View logs")
        print("6. Monitor mode")
        print("7. Exit")
        
        choice = input("\nEnter choice (1-7): ")
        
        if choice == '1':
            controller.start()
        elif choice == '2':
            controller.stop()
        elif choice == '3':
            controller.restart()
        elif choice == '4':
            print(f"\nStatus: {controller.get_status()}")
        elif choice == '5':
            lines = input("Lines to show (default 50): ")
            lines = int(lines) if lines.isdigit() else 50
            controller.view_logs(lines)
        elif choice == '6':
            interval = input("Check interval seconds (default 10): ")
            interval = int(interval) if interval.isdigit() else 10
            controller.monitor(interval)
        elif choice == '7':
            print("\n👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice")

if __name__ == "__main__":
    main()