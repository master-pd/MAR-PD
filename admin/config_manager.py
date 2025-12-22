import json
from utils.helpers import JSONHelper

class ConfigManager:
    def __init__(self):
        self.config_file = 'data/config.json'
        self.config = JSONHelper.load_json(self.config_file)
    
    def update_setting(self, section: str, key: str, value):
        """সেটিং আপডেট"""
        if section in self.config:
            self.config[section][key] = value
            return JSONHelper.save_json(self.config_file, self.config)
        return False
    
    def toggle_feature(self, feature: str) -> bool:
        """ফিচার টগল"""
        if 'features' in self.config:
            if feature in self.config['features']:
                self.config['features'][feature] = not self.config['features'][feature]
                return JSONHelper.save_json(self.config_file, self.config)
        return False
    
    def get_config_summary(self) -> str:
        """কনফিগারেশন সামারি"""
        summary = "⚙️ **কনফিগারেশন সামারি:**\n\n"
        
        # বট ইনফো
        if 'bot_info' in self.config:
            summary += "🤖 **বট ইনফো:**\n"
            for key, value in self.config['bot_info'].items():
                summary += f"• {key}: {value}\n"
            summary += "\n"
        
        # সেটিংস
        if 'settings' in self.config:
            summary += "🔧 **সেটিংস:**\n"
            for key, value in self.config['settings'].items():
                summary += f"• {key}: {value}\n"
            summary += "\n"
        
        # ফিচারস
        if 'features' in self.config:
            summary += "✨ **ফিচারস:**\n"
            for key, value in self.config['features'].items():
                status = "✅" if value else "❌"
                summary += f"• {key}: {status}\n"
        
        return summary