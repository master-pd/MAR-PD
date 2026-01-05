import json
import os


class ConfigManager:
    def __init__(self):
        # Base directory
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.data_dir = os.path.join(self.base_dir, "data")
        self.config_file = os.path.join(self.data_dir, "config.json")

        # Create data directory if not exists
        os.makedirs(self.data_dir, exist_ok=True)

        # Load config
        self.config = self._load_config()

    # ===============================
    # CONFIG.JSON HANDLING
    # ===============================

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
                "slot_reminders": False,
                "quotes_enabled": True,
                "duas_enabled": True,
                "developer_info": True
            },
            "telegram": {
                "api_id": 123456,
                "api_hash": "your_api_hash_here"
            }
        }

        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                print("[CONFIG] Corrupted config.json, recreating...")
                return self._create_default_config(default_config)
        else:
            return self._create_default_config(default_config)

    def _create_default_config(self, default_config):
        self._save_config(default_config)
        return default_config

    def _save_config(self, config):
        with open(self.config_file, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4, ensure_ascii=False)

    # ===============================
    # RESPONSE FILE HANDLING
    # ===============================

    def get_response_file(self, file_type):
        files = {
            "default": "default.json",
            "extra": "extra.json",
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
            if not os.path.exists(file_path):
                self.create_default_json(file_type)
            return file_path
        return None

    # ===============================
    # DEFAULT JSON CREATOR
    # ===============================

    def create_default_json(self, file_type):
        default_data = {
            "default": {
                "hello": ["Hi! 👋", "Hello! 😃", "Assalamu Alaikum! 🤲"],
                "how are you": [
                    "I'm fine, alhamdulillah!",
                    "All good by Allah's grace!"
                ]
            },

            "extra": {
                "good morning": ["Good morning 🌞", "Morning! 😴"],
                "good night": ["Good night 🌙", "Sleep tight 🌟"]
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
                        "level1": "Good morning 🌞",
                        "level2": "Time to start work ⏰",
                        "level3": "Follow your routine 💪"
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
            "announcements": {},

            "hacking": {
                "module": "hacking",
                "enabled": True,
                "mode": "learning",
                "permissions": {
                    "admin_only": True,
                    "allowed_users": []
                },
                "features": {
                    "scanner": True,
                    "analyzer": False,
                    "logger": True
                },
                "limits": {
                    "cooldown_seconds": 60,
                    "daily_limit": 50
                }
            }
        }

        if file_type in default_data:
            file_path = os.path.join(self.data_dir, f"{file_type}.json")
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(default_data[file_type], f, indent=4, ensure_ascii=False)

    # ===============================
    # TELEGRAM CREDS
    # ===============================

    def get_telegram_creds(self):
        return (
            self.config["telegram"]["api_id"],
            self.config["telegram"]["api_hash"]
        )
