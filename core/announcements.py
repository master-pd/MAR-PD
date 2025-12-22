from typing import Dict, List, Optional
from utils.helpers import JSONHelper, TimeHelper
from config import ConfigManager

class AnnouncementHandler:
    def __init__(self, config_manager: ConfigManager):
        self.config = config_manager
        self.announcements_file = self.config.get_response_file("announcements")
        self.announcements = JSONHelper.load_json(self.announcements_file)
    
    def get_announcement(self, ann_type: str) -> Optional[str]:
        """অ্যানাউন্সমেন্ট"""
        announcements = self.announcements.get(ann_type, [])
        if announcements:
            import random
            return random.choice(announcements)
        return None
    
    def add_announcement(self, ann_type: str, message: str) -> bool:
        """নতুন অ্যানাউন্সমেন্ট যোগ"""
        if ann_type not in self.announcements:
            self.announcements[ann_type] = []
        
        self.announcements[ann_type].append(message)
        return JSONHelper.save_json(self.announcements_file, self.announcements)
    
    def get_birthday_message(self, name: str) -> str:
        """বার্থডে মেসেজ"""
        messages = self.announcements.get('birthday', [])
        if messages:
            import random
            template = random.choice(messages)
            return template.format(name=name)
        return f"🎂 Happy Birthday, {name}! 🎉"
    
    def get_anniversary_message(self, name: str, years: int) -> str:
        """অ্যানিভার্সারি মেসেজ"""
        messages = self.announcements.get('anniversary', [])
        if messages:
            import random
            template = random.choice(messages)
            return template.format(name=name, years=years)
        return f"🎉 Happy {years} years anniversary, {name}! 🎊"