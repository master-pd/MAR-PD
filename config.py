import json
import os
from datetime import datetime

class ConfigManager:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.data_dir = os.path.join(self.base_dir, 'data')
        self.config_file = os.path.join(self.data_dir, 'config.json')
        
        # Create directories if not exist
        os.makedirs(self.data_dir, exist_ok=True)
        
        # লোড কনফিগারেশন
        self.config = self._load_config()
    
    def _load_config(self):
        """JSON থেকে কনফিগারেশন লোড"""
        default_config = {
            "bot_info": {
                "name": "YOUR CRUSH ⟵o_0",
                "developer": "RANA",
                "version": "1.0.0"
            },
            "settings": {
                "timezone": "Asia/Dhaka",
                "language": "bn",
                "human_delay": 1.5,
                "max_retries": 3,
                "log_level": "INFO"
            },
            "features": {
                "auto_reply": True,
                "namaz_alert": True,
                "slot_reminders": True,
                "quotes_enabled": True,
                "duas_enabled": True,
                "developer_info": True
            },
            "telegram": {
                "api_id": 123456,  # আপনার API ID দিন
                "api_hash": "your_api_hash_here"  # আপনার API Hash দিন
            }
        }
        
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                print("Config file corrupted, creating new one")
                return self._create_default_config(default_config)
        else:
            return self._create_default_config(default_config)
    
    def _create_default_config(self, default_config):
        """ডিফল্ট কনফিগারেশন তৈরি"""
        self._save_config(default_config)
        return default_config
    
    def _save_config(self, config):
        """কনফিগারেশন সেভ"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
    
    def get_response_file(self, file_type):
        """রেসপন্স ফাইল পাথ রিটার্ন"""
        files = {
            "default": "default.json",
            "extra": "extra_responses.json",
            "namaz": "namaz.json",
            "slot": "slot.json",
            "users": "users.json",
            "quotes": "quotes.json",
            "duas": "duas.json",
            "media": "media.json",
            "events": "events.json",
            "announcements": "announcements.json",
            "hacking": "hacking.json"
        }
        
        if file_type in files:
            file_path = os.path.join(self.data_dir, files[file_type])
            # ফাইল না থাকলে তৈরি করবে
            if not os.path.exists(file_path):
                self.create_default_json(file_type)
            return file_path
        return None
    
    def create_default_json(self, file_type):
        """ডিফল্ট JSON ফাইল তৈরি"""
        default_data = {
            "default": {
                "hello": ["Hi! 👋", "Hello! 😃", "Assalamu Alaikum! 🤲"],
                "how are you": ["I'm fine, alhamdulillah!", "All good by Allah's grace!"]
            },
            "extra": {
                "good morning": ["Good morning 🌞", "Morning! Hope you slept well 😴"],
                "good night": ["Good night 🌙", "Sleep tight! 🌟"]
            },
            "namaz": {
                "Fajr": "05:00",
                "Dhuhr": "12:30",
                "Asr": "15:45",
                "Maghrib": "18:20",
                "Isha": "19:40"
            },
            "slot": {
                "slots": [
                    {
                        "name": "morning",
                        "start": "06:00",
                        "end": "09:00",
                        "level1": "Good morning! 🌞",
                        "level2": "Time to start your work ⏰",
                        "level3": "Don't forget your morning routine!"
                    }
                ]
            },
            "users": {},
            "quotes": {
                "quotes": [
                    "The best among you are those who have the best manners.",
                    "Patience is the key to success."
                ]
            },
            "duas": {
                "duas": [
                    "O Allah, guide me to the straight path.",
                    "Grant me patience and strength."
                ]
            },
            "media": {
                "emojis": ["😊", "👍", "❤️", "🤲", "🌙", "☀️"],
                "stickers": []
            },
            "events": {},
            "announcements": {}
        },
        "hacking": {
    "module": "hacking",
    "enabled": false,
    "mode": "learning",
    "permissions": {
        "admin_only": true,
        "allowed_users": []
    },
    "features": {
        "scanner": true,
        "analyzer": false,
        "logger": true
    },
    "limits": {
        "cooldown_seconds": 60,
        "daily_limit": 50
    }
}
        
        if file_type in default_data:
            file_path = os.path.join(self.data_dir, f"{file_type}.json")
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(default_data[file_type], f, indent=4, ensure_ascii=False)
    
    def get_telegram_creds(self):
        """টেলিগ্রাম ক্রিডেনশিয়াল"""
        return (
            self.config['telegram']['api_id'],
            self.config['telegram']['api_hash']
        )
