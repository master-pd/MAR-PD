import json
import os

class ConfigManager:
    def __init__(self):
        # Base directory
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.data_dir = os.path.join(self.base_dir, "data")
        self.config_file = os.path.join(self.data_dir, "config.json")

        # Ensure data directory exists
        os.makedirs(self.data_dir, exist_ok=True)

        # Load configuration
        self.config = self._load_config()

    # Master JSON path
    def get_master_file(self):
        return os.path.join(self.data_dir, 'master.json')
        
    # ==================================
    # CONFIG VALIDATION
    # ==================================
    def is_valid_config(self):
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
    # CONFIG.JSON HANDLING
    # ==================================
    def _load_config(self):
        default_config = {
            "bot_info": {
                "name": "YOUR BOT",
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
    # TELEGRAM CREDENTIALS
    # ==================================
    def get_telegram_creds(self):
        telegram = self.config.get("telegram", {})
        return telegram.get("api_id"), telegram.get("api_hash")
