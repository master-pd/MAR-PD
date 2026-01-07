import json
import os

class ConfigManager:
    def __init__(self):
        # Base directories
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.data_dir = os.path.join(self.base_dir, "data")
        self.config_file = os.path.join(self.data_dir, "config.json")

        # Ensure data directory exists
        os.makedirs(self.data_dir, exist_ok=True)

        # Load config.json
        self.config = self._load_config()

    # ==================================
    # MASTER JSON FILE
    # ==================================
    def get_master_file(self):
        """Return path to master.json"""
        master_path = os.path.join(self.data_dir, 'master.json')
        if not os.path.exists(master_path):
            # create empty master.json if missing
            with open(master_path, "w", encoding="utf-8") as f:
                json.dump([], f, indent=4, ensure_ascii=False)
        return master_path

    # ==================================
    # RESPONSE FILES
    # ==================================
    def get_response_file(self, file_type):
        """Return path to a response JSON, create if missing"""
        files = {
            "default": "default.json",
            "extra": "extra.json",
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

    # ==================================
    # DEFAULT JSON CREATOR
    # ==================================
    def create_default_json(self, file_type):
        """Create default JSON file if missing"""
        default_data = {
            "default": {
                "hello": ["Hi! 👋", "Hello! 😃", "Assalamu Alaikum! 🤲"],
                "how are you": ["I'm fine, alhamdulillah!", "All good by Allah's grace!"]
            },
            "extra": {
                "good morning": ["Good morning 🌞", "Morning! 😴"],
                "good night": ["Good night 🌙", "Sleep tight 🌟"]
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
                "emojis": ["😊", "👍", "❤️", "🤲", "🌙", "☀️", "🌟", "✨", "🎉"],
                "stickers": []
            },
            "events": {},
            "announcements": {},
            "hacking": {
                "module": "hacking",
                "enabled": True,
                "mode": "learning",
                "permissions": {"admin_only": True, "allowed_users": []},
                "features": {"scanner": True, "analyzer": False, "logger": True},
                "limits": {"cooldown_seconds": 60, "daily_limit": 50}
            }
        }

        if file_type in default_data:
            file_path = os.path.join(self.data_dir, f"{file_type}.json")
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(default_data[file_type], f, indent=4, ensure_ascii=False)

    # ==================================
    # CONFIG.JSON HANDLING
    # ==================================
    def _load_config(self):
        """Load or create default config.json"""
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
                print("[CONFIG] Corrupted config.json detected, recreating...")
                return self._create_default_config(default_config)
        else:
            return self._create_default_config(default_config)

    def _create_default_config(self, default_config):
        self._save_config(default_config)
        return default_config

    def _save_config(self, config):
        with open(self.config_file, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4, ensure_ascii=False)

    # ==================================
    # CONFIG VALIDATION
    # ==================================
    def is_valid_config(self):
        """Check Telegram API credentials"""
        try:
            telegram = self.config.get("telegram", {})
            api_id = telegram.get("api_id")
            api_hash = telegram.get("api_hash")

            if not api_id or not api_hash:
                print("❌ Telegram API credentials missing")
                return False

            return True
        except Exception as e:
            print(f"❌ Config validation failed: {e}")
            return False

    # ==================================
    # TELEGRAM CREDENTIALS
    # ==================================
    def get_telegram_creds(self):
        telegram = self.config.get("telegram", {})
        return telegram.get("api_id"), telegram.get("api_hash")
