from datetime import datetime
from typing import List, Dict
from utils.helpers import TimeHelper

class ReminderSystem:
    def __init__(self):
        self.reminders_file = 'data/reminders.json'
        self.reminders = {}
    
    def add_reminder(self, user_id: int, message: str, remind_time: str) -> bool:
        """রিমাইন্ডার যোগ"""
        from utils.helpers import JSONHelper
        
        if user_id not in self.reminders:
            self.reminders[user_id] = []
        
        reminder = {
            'id': len(self.reminders[user_id]) + 1,
            'message': message,
            'time': remind_time,
            'created': TimeHelper.get_current_time().isoformat(),
            'status': 'pending'
        }
        
        self.reminders[user_id].append(reminder)
        return self.save_reminders()
    
    def get_user_reminders(self, user_id: int) -> List[Dict]:
        """ইউজারের রিমাইন্ডার"""
        return self.reminders.get(user_id, [])
    
    def check_reminders(self) -> List[Dict]:
        """রিমাইন্ডার চেক"""
        current_time = TimeHelper.get_current_time()
        current_hour = TimeHelper.format_time(current_time)
        
        due_reminders = []
        
        for user_id, user_reminders in self.reminders.items():
            for reminder in user_reminders:
                if reminder['time'] == current_hour and reminder['status'] == 'pending':
                    due_reminders.append({
                        'user_id': user_id,
                        'reminder': reminder
                    })
                    reminder['status'] = 'sent'
        
        if due_reminders:
            self.save_reminders()
        
        return due_reminders
    
    def save_reminders(self) -> bool:
        """রিমাইন্ডার সেভ"""
        from utils.helpers import JSONHelper
        return JSONHelper.save_json(self.reminders_file, self.reminders)