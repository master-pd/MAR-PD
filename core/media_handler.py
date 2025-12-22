import random
from typing import List, Dict, Optional
from utils.helpers import JSONHelper
from config import ConfigManager

class MediaHandler:
    def __init__(self, config_manager: ConfigManager):
        self.config = config_manager
        self.media_file = self.config.get_response_file("media")
        self.media_data = JSONHelper.load_json(self.media_file)
    
    def get_emoji(self, category: str = None) -> str:
        """ইমোজি গেট"""
        emojis = self.media_data.get('emojis', [])
        if category and category in self.media_data.get('categories', {}):
            category_emojis = self.media_data['categories'][category]
            if category_emojis:
                return random.choice(category_emojis)
        
        if emojis:
            return random.choice(emojis)
        return "😊"
    
    def get_sticker(self) -> Optional[str]:
        """স্টিকার ID"""
        stickers = self.media_data.get('stickers', [])
        if stickers:
            return random.choice(stickers)
        return None
    
    def get_template(self, template_name: str) -> Optional[str]:
        """টেম্পলেট"""
        templates = self.media_data.get('templates', {})
        return templates.get(template_name)
    
    def format_message(self, message: str, template_name: str = None) -> str:
        """মেসেজ ফরম্যাট"""
        if template_name:
            template = self.get_template(template_name)
            if template:
                return template.format(message=message)
        
        # ডিফল্ট ফরম্যাট
        emoji = self.get_emoji()
        return f"{emoji} {message} {emoji}"
    
    def get_random_media(self) -> str:
        """র্যান্ডম মিডিয়া"""
        all_emojis = []
        
        # সব ইমোজি কালেক্ট
        emojis = self.media_data.get('emojis', [])
        all_emojis.extend(emojis)
        
        # ক্যাটাগরি ইমোজি
        categories = self.media_data.get('categories', {})
        for category_emojis in categories.values():
            all_emojis.extend(category_emojis)
        
        if all_emojis:
            return random.choice(all_emojis)
        return "✨"
    
    def add_emoji(self, emoji: str, category: str = None) -> bool:
        """নতুন ইমোজি যোগ"""
        if not emoji:
            return False
        
        if category:
            if 'categories' not in self.media_data:
                self.media_data['categories'] = {}
            
            if category not in self.media_data['categories']:
                self.media_data['categories'][category] = []
            
            if emoji not in self.media_data['categories'][category]:
                self.media_data['categories'][category].append(emoji)
        else:
            if 'emojis' not in self.media_data:
                self.media_data['emojis'] = []
            
            if emoji not in self.media_data['emojis']:
                self.media_data['emojis'].append(emoji)
        
        return JSONHelper.save_json(self.media_file, self.media_data)