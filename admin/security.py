import time
from typing import Dict
from datetime import datetime, timedelta

class SecurityManager:
    def __init__(self):
        self.flood_control: Dict[int, Dict] = {}
        self.max_messages_per_minute = 10
        self.block_duration = 300  # 5 minutes
    
    def check_flood(self, user_id: int) -> bool:
        """ফ্লাড চেক"""
        current_time = time.time()
        
        if user_id not in self.flood_control:
            self.flood_control[user_id] = {
                'count': 1,
                'first_message': current_time,
                'last_message': current_time,
                'warnings': 0
            }
            return False
        
        user_data = self.flood_control[user_id]
        
        # রিসেট কাউন্ট যদি ১ মিনিট পার হয়ে যায়
        if current_time - user_data['first_message'] > 60:
            user_data['count'] = 1
            user_data['first_message'] = current_time
            user_data['last_message'] = current_time
            return False
        
        # মেসেজ কাউন্ট আপডেট
        user_data['count'] += 1
        user_data['last_message'] = current_time
        
        # ফ্লাড ডিটেক্ট
        if user_data['count'] > self.max_messages_per_minute:
            user_data['warnings'] += 1
            return True
        
        return False
    
    def get_warnings(self, user_id: int) -> int:
        """ওয়ার্নিং কাউন্ট"""
        if user_id in self.flood_control:
            return self.flood_control[user_id]['warnings']
        return 0
    
    def reset_user(self, user_id: int):
        """ইউজার রিসেট"""
        if user_id in self.flood_control:
            del self.flood_control[user_id]