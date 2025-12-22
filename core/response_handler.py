import re
import random
from typing import Dict, List, Optional, Any
from utils.helpers import JSONHelper, TextHelper
from config import ConfigManager

class ResponseHandler:
    def __init__(self, config_manager: ConfigManager):
        self.config = config_manager
        self.responses: Dict[str, Any] = {}
        self.load_all_responses()
    
    def load_all_responses(self):
        """সব রেসপন্স JSON লোড"""
        response_files = [
            'default', 'extra', 'quotes', 'duas', 
            'media', 'events', 'announcements'
        ]
        
        for file_type in response_files:
            file_path = self.config.get_response_file(file_type)
            if file_path:
                self.responses[file_type] = JSONHelper.load_json(file_path)
    
    def get_auto_reply(self, message_text: str) -> Optional[str]:
        """মেসেজের জন্য অটো রিপ্লাই"""
        message_text = TextHelper.clean_text(message_text)
        
        # ডিফল্ট রেসপন্স চেক
        default_responses = self.responses.get('default', {})
        for key, responses in default_responses.items():
            if re.search(rf'\b{re.escape(key)}\b', message_text):
                return JSONHelper.get_random_response(responses)
        
        # এক্সট্রা রেসপন্স চেক
        extra_responses = self.responses.get('extra', {})
        for key, responses in extra_responses.items():
            if re.search(rf'\b{re.escape(key)}\b', message_text):
                return JSONHelper.get_random_response(responses)
        
        return None
    
    def get_quote(self) -> str:
        """র্যান্ডম কোট"""
        quotes = self.responses.get('quotes', {}).get('quotes', [])
        if quotes:
            return random.choice(quotes)
        return "Stay positive and keep moving forward."
    
    def get_dua(self) -> str:
        """র্যান্ডম দোয়া"""
        duas = self.responses.get('duas', {}).get('duas', [])
        if duas:
            return random.choice(duas)
        return "May Allah bless you and protect you."
    
    def get_media(self, media_type: str) -> str:
        """মিডিয়া আইটেম"""
        media = self.responses.get('media', {}).get(media_type, [])
        if media:
            return random.choice(media)
        return ""
    
    def get_event_message(self, event_type: str) -> Optional[str]:
        """ইভেন্ট মেসেজ"""
        events = self.responses.get('events', {}).get(event_type, [])
        if events:
            return JSONHelper.get_random_response(events)
        return None
    
    def get_announcement(self, ann_type: str) -> Optional[str]:
        """অ্যানাউন্সমেন্ট"""
        announcements = self.responses.get('announcements', {}).get(ann_type, [])
        if announcements:
            return JSONHelper.get_random_response(announcements)
        return None
    
    def get_bot_response(self, intent: str) -> Optional[str]:
        """বট রেসপন্স (ইনটেন্ট ভিত্তিক)"""
        intent_responses = {
            'greeting': ["Hello! 👋", "Hi there! 😊", "Assalamu Alaikum! 🤲"],
            'farewell': ["Goodbye! 👋", "See you later! 😊", "Take care! 🤲"],
            'thanks': ["You're welcome! 😊", "Happy to help! 👍", "Anytime! 😄"],
            'help': ["I can help with:\n• Prayer times\n• Reminders\n• Quotes\n• Duas\n• And more!"],
            'status': ["I'm running smoothly! ✅", "All systems operational! 🚀", "Working perfectly! 😎"]
        }
        
        if intent in intent_responses:
            return random.choice(intent_responses[intent])
        return None
    
    def process_message(self, message_text: str) -> Dict:
        """মেসেজ প্রসেস"""
        result = {
            'reply': None,
            'action': None,
            'data': None
        }
        
        message_lower = message_text.lower()
        
        # গ্রিটিং
        if any(word in message_lower for word in ['hello', 'hi', 'hey', 'assalam']):
            result['reply'] = self.get_bot_response('greeting')
        
        # কোটস
        elif any(word in message_lower for word in ['quote', 'motivation', 'inspire']):
            result['reply'] = self.get_quote()
        
        # দোয়া
        elif any(word in message_lower for word in ['dua', 'prayer', 'blessing']):
            result['reply'] = self.get_dua()
        
        # হেল্প
        elif any(word in message_lower for word in ['help', 'what can you do', 'features']):
            result['reply'] = self.get_bot_response('help')
        
        # স্ট্যাটাস
        elif any(word in message_lower for word in ['status', 'how are you', 'alive']):
            result['reply'] = self.get_bot_response('status')
        
        # ডিফল্ট অটো রিপ্লাই
        if not result['reply']:
            result['reply'] = self.get_auto_reply(message_text)
        
        return result