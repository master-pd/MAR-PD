import json
import os
from typing import Dict, List
from utils.helpers import JSONHelper

class AdminPanel:
    def __init__(self):
        self.admins_file = 'data/admins.json'
        self.blacklist_file = 'data/blacklist.json'
        self.load_admins()
    
    def load_admins(self):
        """অ্যাডমিন লোড"""
        if not os.path.exists(self.admins_file):
            default_admins = {
                "admins": [123456789],  # আপনার Telegram ID দিন
                "permissions": {
                    "can_edit_responses": True,
                    "can_edit_times": True,
                    "can_manage_users": True,
                    "can_view_logs": True
                }
            }
            JSONHelper.save_json(self.admins_file, default_admins)
            self.admins = default_admins
        else:
            self.admins = JSONHelper.load_json(self.admins_file)
    
    def is_admin(self, user_id: int) -> bool:
        """চেক অ্যাডমিন"""
        return user_id in self.admins.get('admins', [])
    
    def add_admin(self, admin_id: int) -> bool:
        """নতুন অ্যাডমিন যোগ"""
        if admin_id not in self.admins.get('admins', []):
            self.admins['admins'].append(admin_id)
            return JSONHelper.save_json(self.admins_file, self.admins)
        return False
    
    def remove_admin(self, admin_id: int) -> bool:
        """অ্যাডমিন রিমুভ"""
        if admin_id in self.admins.get('admins', []):
            self.admins['admins'].remove(admin_id)
            return JSONHelper.save_json(self.admins_file, self.admins)
        return False
    
    def get_admin_commands(self) -> List[str]:
        """অ্যাডমিন কমান্ড লিস্ট"""
        return [
            "/add_response [keyword] [response] - নতুন রেসপন্স যোগ",
            "/edit_namaz [namaz] [time] - নামাজের সময় এডিট",
            "/add_slot [name] [start] [end] [message] - নতুন স্লট যোগ",
            "/view_logs [days] - লগ দেখা",
            "/user_stats [user_id] - ইউজার স্ট্যাটস",
            "/broadcast [message] - ব্রডকাস্ট মেসেজ",
            "/backup - ব্যাকআপ নিন",
            "/restart - বট রিস্টার্ট"
        ]