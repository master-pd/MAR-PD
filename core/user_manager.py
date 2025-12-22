from typing import Dict, Any, Optional
from utils.helpers import JSONHelper, TimeHelper
from config import ConfigManager

class UserManager:
    def __init__(self, config_manager: ConfigManager):
        self.config = config_manager
        self.users_file = self.config.get_response_file("users")
        self.users = self.load_users()
    
    def load_users(self) -> Dict:
        """ইউজার ডেটা লোড"""
        return JSONHelper.load_json(self.users_file)
    
    def save_users(self) -> bool:
        """ইউজার ডেটা সেভ"""
        return JSONHelper.save_json(self.users_file, self.users)
    
    def get_user(self, user_id: str) -> Dict:
        """ইউজার ডেটা গেট"""
        user_id = str(user_id)
        if user_id not in self.users:
            self.users[user_id] = self.create_default_user(user_id)
            self.save_users()
        return self.users[user_id]
    
    def create_default_user(self, user_id: str) -> Dict:
        """ডিফল্ট ইউজার তৈরি"""
        return {
            "id": user_id,
            "name": f"User_{user_id}",
            "namaz_alert": True,
            "slot_reminder": True,
            "quotes_enabled": True,
            "duas_enabled": True,
            "slot_reminder_count": {},
            "namaz_count": 0,
            "total_messages": 0,
            "last_activity": TimeHelper.get_current_time().isoformat(),
            "join_date": TimeHelper.get_current_time().isoformat(),
            "settings": {
                "language": "bn",
                "timezone": "Asia/Dhaka"
            }
        }
    
    def update_user_activity(self, user_id: str) -> None:
        """ইউজার এক্টিভিটি আপডেট"""
        user = self.get_user(user_id)
        user['last_activity'] = TimeHelper.get_current_time().isoformat()
        user['total_messages'] = user.get('total_messages', 0) + 1
        self.save_users()
    
    def update_user_setting(self, user_id: str, setting: str, value: Any) -> bool:
        """ইউজার সেটিং আপডেট"""
        user = self.get_user(user_id)
        
        if '.' in setting:
            # nested setting (e.g., "settings.language")
            keys = setting.split('.')
            current = user
            for key in keys[:-1]:
                if key not in current:
                    current[key] = {}
                current = current[key]
            current[keys[-1]] = value
        else:
            user[setting] = value
        
        return self.save_users()
    
    def update_slot_count(self, user_id: str, slot_name: str) -> bool:
        """স্লট কাউন্ট আপডেট"""
        user = self.get_user(user_id)
        if 'slot_reminder_count' not in user:
            user['slot_reminder_count'] = {}
        
        user['slot_reminder_count'][slot_name] = user['slot_reminder_count'].get(slot_name, 0) + 1
        return self.save_users()
    
    def update_namaz_count(self, user_id: str) -> bool:
        """নামাজ কাউন্ট আপডেট"""
        user = self.get_user(user_id)
        user['namaz_count'] = user.get('namaz_count', 0) + 1
        return self.save_users()
    
    def get_user_stats(self, user_id: str) -> Dict:
        """ইউজার স্ট্যাটস"""
        user = self.get_user(user_id)
        slot_counts = user.get('slot_reminder_count', {})
        
        return {
            'total_messages': user.get('total_messages', 0),
            'namaz_count': user.get('namaz_count', 0),
            'slot_reminders': sum(slot_counts.values()),
            'active_days': self.calculate_active_days(user),
            'last_active': user.get('last_activity', 'Never')
        }
    
    def calculate_active_days(self, user: Dict) -> int:
        """অ্যাক্টিভ দিন ক্যালকুলেট"""
        join_date = user.get('join_date')
        if not join_date:
            return 1
        
        try:
            from datetime import datetime
            join_dt = datetime.fromisoformat(join_date)
            current_dt = TimeHelper.get_current_time()
            days_diff = (current_dt - join_dt).days
            return max(1, days_diff)
        except:
            return 1
    
    def get_all_users(self) -> Dict:
        """সব ইউজার"""
        return self.users
    
    def get_active_users(self, hours: int = 24) -> Dict:
        """অ্যাক্টিভ ইউজার"""
        active_users = {}
        current_time = TimeHelper.get_current_time()
        
        for user_id, user_data in self.users.items():
            last_active = user_data.get('last_activity')
            if last_active:
                try:
                    from datetime import datetime
                    last_dt = datetime.fromisoformat(last_active)
                    hours_diff = (current_time - last_dt).total_seconds() / 3600
                    if hours_diff <= hours:
                        active_users[user_id] = user_data
                except:
                    pass
        
        return active_users
    
    def delete_user(self, user_id: str) -> bool:
        """ইউজার ডিলিট"""
        user_id = str(user_id)
        if user_id in self.users:
            del self.users[user_id]
            return self.save_users()
        return False
    
    def reset_user_stats(self, user_id: str) -> bool:
        """ইউজার স্ট্যাটস রিসেট"""
        user = self.get_user(user_id)
        user['total_messages'] = 0
        user['namaz_count'] = 0
        user['slot_reminder_count'] = {}
        return self.save_users()