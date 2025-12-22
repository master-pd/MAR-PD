#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Quick Setup Script - Safe UserBot
Fast setup for experienced users
"""

import os
import json
import sys

def create_minimal_files():
    """মিনিমাল ফাইলস তৈরি"""
    
    print("⚡ Quick Setup - Safe UserBot")
    print("="*40)
    
    # 1. Create minimal config
    config = {
        "bot_info": {
            "name": "Safe UserBot",
            "developer": "RANA", 
            "version": "1.0.0"
        },
        "telegram": {
            "api_id": int(input("Enter API ID: ")),
            "api_hash": input("Enter API Hash: ")
        }
    }
    
    with open('config.py', 'w') as f:
        f.write(f'''import json
import os

class ConfigManager:
    def __init__(self):
        self.config = {json.dumps(config, indent=4)}
    
    def get_telegram_creds(self):
        return (self.config['telegram']['api_id'], 
                self.config['telegram']['api_hash'])
''')
    
    print("✓ config.py created")
    
    # 2. Create requirements.txt
    requirements = """telethon==1.28.1
apscheduler==3.10.1
pytz==2022.7"""
    
    with open('requirements.txt', 'w') as f:
        f.write(requirements)
    
    print("✓ requirements.txt created")
    
    # 3. Create minimal main.py
    main_py = '''#!/usr/bin/env python3
import asyncio
from telethon import TelegramClient, events

async def main():
    from config import ConfigManager
    config = ConfigManager()
    api_id, api_hash = config.get_telegram_creds()
    
    client = TelegramClient('sessions/main_account', api_id, api_hash)
    
    @client.on(events.NewMessage(pattern='(?i)hello'))
    async def handler(event):
        await event.reply("Hello! I'm Safe UserBot 🚀")
    
    await client.start()
    print("✅ Bot started!")
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
'''
    
    with open('main.py', 'w') as f:
        f.write(main_py)
    
    print("✓ main.py created")
    
    # 4. Create directories
    os.makedirs('data', exist_ok=True)
    os.makedirs('sessions', exist_ok=True)
    os.makedirs('logs', exist_ok=True)
    
    print("✓ Directories created")
    
    print("\n" + "="*40)
    print("✅ Quick setup completed!")
    print("\nNext steps:")
    print("1. pip install -r requirements.txt")
    print("2. python main.py")
    print("3. Enter phone number & code")
    print("="*40)

if __name__ == "__main__":
    create_minimal_files()