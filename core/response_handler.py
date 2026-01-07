import re
import random
from typing import Dict, Any, Optional
from utils.helpers import JSONHelper, TextHelper
from config import ConfigManager

class ResponseHandler:
    def __init__(self, config_manager: ConfigManager):
        self.config = config_manager
        self.responses: Dict[str, Any] = {}
        self.master_file_path = self.config.get_master_file()  # master.json path
        self.load_all_responses()
    
    def load_all_responses(self):
        """মাস্টার ফাইল থেকে সব রেসপন্স JSON load করা"""
        master_data = JSONHelper.load_json(self.master_file_path)
        response_files = master_data.get("response_files", ["default"])
        
        for file_name in response_files:
            file_path = self.config.get_response_file(file_name)
            if file_path:
                self.responses[file_name] = JSONHelper.load_json(file_path)
    
    def get_auto_reply(self, message_text: str) -> Optional[str]:
        """মেসেজের জন্য অটো রিপ্লাই (সব ফাইল scan করবে)"""
        message_text = TextHelper.clean_text(message_text)
        
        for file_name, responses in self.responses.items():
            for key, response_list in responses.items():
                if re.search(rf'\b{re.escape(key)}\b', message_text, re.IGNORECASE):
                    return JSONHelper.get_random_response(response_list)
        
        return None
    
    def get_quote(self) -> str:
        quotes = self.responses.get('quotes', {}).get('quotes', [])
        return random.choice(quotes) if quotes else "Stay positive and keep moving forward."
    
    def get_dua(self) -> str:
        duas = self.responses.get('duas', {}).get('duas', [])
        return random.choice(duas) if duas else "May Allah bless you and protect you."
    
    def get_media(self, media_type: str) -> str:
        media = self.responses.get('media', {}).get(media_type, [])
        return random.choice(media) if media else ""
    
    def get_event_message(self, event_type: str) -> Optional[str]:
        events = self.responses.get('events', {}).get(event_type, [])
        return JSONHelper.get_random_response(events) if events else None
    
    def get_announcement(self, ann_type: str) -> Optional[str]:
        announcements = self.responses.get('announcements', {}).get(ann_type, [])
        return JSONHelper.get_random_response(announcements) if announcements else None
    
    def get_bot_response(self, intent: str) -> Optional[str]:
        intent_responses = {
            'greeting': ["Hello! 👋", "Hi there! 😊", "Assalamu Alaikum! 🤲"],
            'farewell': ["Goodbye! 👋", "See you later! 😊", "Take care! 🤲"],
            'thanks': ["You're welcome! 😊", "Happy to help! 👍", "Anytime! 😄"],
            'help': ["I can help with:\n• Prayer times\n• Reminders\n• Quotes\n• Duas\n• And more!"],
            'status': ["I'm running smoothly! ✅", "All systems operational! 🚀", "Working perfectly! 😎"]
        }
        return random.choice(intent_responses[intent]) if intent in intent_responses else None
    
    def process_message(self, message_text: str) -> Dict:
        """মেসেজ প্রসেস করা"""
        result = {
            'reply': None,
            'action': None,
            'data': None
        }
        message_lower = message_text.lower()
        
        # Intent check
        if any(word in message_lower for word in ['hello', 'hi', 'hey', 'assalam']):
            result['reply'] = self.get_bot_response('greeting')
        elif any(word in message_lower for word in ['quote', 'motivation', 'inspire']):
            result['reply'] = self.get_quote()
        elif any(word in message_lower for word in ['dua', 'prayer', 'blessing']):
            result['reply'] = self.get_dua()
        elif any(word in message_lower for word in ['help', 'what can you do', 'features']):
            result['reply'] = self.get_bot_response('help')
        elif any(word in message_lower for word in ['status', 'how are you', 'alive']):
            result['reply'] = self.get_bot_response('status')
        
        # Auto reply যদি আগের condition match না করে
        if not result['reply']:
            result['reply'] = self.get_auto_reply(message_text)
        
        return result
