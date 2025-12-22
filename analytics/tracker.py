import json
from datetime import datetime, timedelta
from typing import Dict, List
from utils.helpers import JSONHelper, TimeHelper

class AnalyticsTracker:
    def __init__(self):
        self.analytics_file = 'data/analytics.json'
        self.analytics = self.load_analytics()
    
    def load_analytics(self) -> Dict:
        """অ্যানালিটিক্স লোড"""
        if not os.path.exists(self.analytics_file):
            default_analytics = {
                "daily_stats": {},
                "user_activity": {},
                "message_stats": {
                    "total_messages": 0,
                    "auto_replies": 0,
                    "commands_used": {}
                },
                "reminder_stats": {
                    "namaz_alerts_sent": 0,
                    "slot_reminders_sent": 0,
                    "total_reminders": 0
                },
                "system_stats": {
                    "uptime": 0,
                    "errors": 0,
                    "restarts": 0
                }
            }
            JSONHelper.save_json(self.analytics_file, default_analytics)
            return default_analytics
        return JSONHelper.load_json(self.analytics_file)
    
    def track_message(self, user_id: str, message_type: str = "regular"):
        """মেসেজ ট্র্যাক"""
        today = TimeHelper.get_current_time().strftime("%Y-%m-%d")
        
        # ডেইলি স্ট্যাটস
        if today not in self.analytics["daily_stats"]:
            self.analytics["daily_stats"][today] = {
                "messages": 0,
                "users": set(),
                "start_time": TimeHelper.get_current_time().isoformat()
            }
        
        self.analytics["daily_stats"][today]["messages"] += 1
        self.analytics["daily_stats"][today]["users"].add(user_id)
        
        # টোটাল মেসেজ
        self.analytics["message_stats"]["total_messages"] += 1
        
        # মেসেজ টাইপ
        if message_type != "regular":
            if message_type not in self.analytics["message_stats"]["commands_used"]:
                self.analytics["message_stats"]["commands_used"][message_type] = 0
            self.analytics["message_stats"]["commands_used"][message_type] += 1
        
        self.save_analytics()
    
    def track_reminder(self, reminder_type: str):
        """রিমাইন্ডার ট্র্যাক"""
        if reminder_type == "namaz":
            self.analytics["reminder_stats"]["namaz_alerts_sent"] += 1
        elif reminder_type == "slot":
            self.analytics["reminder_stats"]["slot_reminders_sent"] += 1
        
        self.analytics["reminder_stats"]["total_reminders"] += 1
        self.save_analytics()
    
    def get_daily_report(self, date: str = None) -> Dict:
        """ডেইলি রিপোর্ট"""
        if not date:
            date = TimeHelper.get_current_time().strftime("%Y-%m-%d")
        
        if date in self.analytics["daily_stats"]:
            day_stats = self.analytics["daily_stats"][date]
            return {
                "date": date,
                "total_messages": day_stats["messages"],
                "unique_users": len(day_stats.get("users", [])),
                "start_time": day_stats.get("start_time", "")
            }
        
        return {"date": date, "total_messages": 0, "unique_users": 0}
    
    def save_analytics(self) -> bool:
        """অ্যানালিটিক্স সেভ"""
        # Convert set to list for JSON serialization
        for date, stats in self.analytics["daily_stats"].items():
            if "users" in stats and isinstance(stats["users"], set):
                stats["users"] = list(stats["users"])
        
        return JSONHelper.save_json(self.analytics_file, self.analytics)