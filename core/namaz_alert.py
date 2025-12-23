from typing import Dict, Optional
from utils.helpers import JSONHelper, TimeHelper
from config import ConfigManager
from datetime import datetime, timedelta

class NamazAlert:
    def __init__(self, config_manager: ConfigManager):
        self.config = config_manager
        self.namaz_file = self.config.get_response_file("namaz")
        self.namaz_times = self.load_namaz_times()
        self.namaz_order = ['Fajr', 'Dhuhr', 'Asr', 'Maghrib', 'Isha']
    
    def load_namaz_times(self) -> Dict:
        """নামাজের সময় লোড"""
        return JSONHelper.load_json(self.namaz_file)
    
    def save_namaz_times(self) -> bool:
        """নামাজের সময় সেভ"""
        return JSONHelper.save_json(self.namaz_file, self.namaz_times)
    
    def update_namaz_time(self, namaz_name: str, time_str: str) -> bool:
        """নামাজের সময় আপডেট"""
        if namaz_name in self.namaz_order:
            self.namaz_times[namaz_name] = time_str
            return self.save_namaz_times()
        return False
    
    def get_next_namaz(self) -> Dict:
        """পরের নামাজের সময়"""
        current_time = TimeHelper.get_current_time()
        current_hour = TimeHelper.format_time(current_time)
        
        for namaz in self.namaz_order:
            if namaz in self.namaz_times:
                namaz_time = self.namaz_times[namaz]
                if namaz_time > current_hour:
                    return {
                        'name': namaz,
                        'time': namaz_time,
                        'message': f"🕌 এরপরের নামাজ: **{namaz}** - {namaz_time}\nপ্রস্তুত হওয়ার সময় এখনই! 🤲"
                    }
        
        # যদি সব নামাজ পার হয়ে যায়, কালকের ফজর দেখাও
        next_fajr = self.namaz_times.get('Fajr', '05:00')
        return {
            'name': 'Fajr',
            'time': next_fajr,
            'message': f"আজকের সব নামাজ শেষ! 🎉\nপরের নামাজ কাল সকাল **ফজর** - {next_fajr}"
        }
    
    def check_namaz_time(self, minutes_before: int = 5) -> Optional[Dict]:
        """নামাজের সময় চেক (মিনিট আগে এলার্ট)"""
        current_time = TimeHelper.get_current_time()
        current_hour = TimeHelper.format_time(current_time)
        
        for namaz, time_str in self.namaz_times.items():
            namaz_time = TimeHelper.parse_time(time_str)
            if namaz_time:
                # এলার্ট টাইম (মিনিট আগে)
                alert_time = namaz_time - timedelta(minutes=minutes_before)
                alert_time_str = TimeHelper.format_time(alert_time)
                
                if current_hour == alert_time_str:
                    return {
                        'name': namaz,
                        'time': time_str,
                        'message': f"⏰ {namaz} নামাজ {minutes_before} মিনিট পর!\nসময়: {time_str}\nওজু করে প্রস্তুত হোন 🤲"
                    }
                
                # এক্সাক্ট টাইম
                if current_hour == time_str:
                    return {
                        'name': namaz,
                        'time': time_str,
                        'message': f"🕌 {namaz} নামাজের সময় এখন!\n{time_str}\nদ্রুত নামাজ পড়ে নিন! 🕌"
                    }
        
        return None
    
    def get_all_namaz_times(self) -> str:
        """সব নামাজের সময়"""
        result = "🕌 আজকের নামাজের সময়সূচি:\n\n"
        for namaz in self.namaz_order:
            if namaz in self.namaz_times:
                result += f"• {namaz}: {self.namaz_times[namaz]}\n"
        
        next_namaz = self.get_next_namaz()
        result += f"\n👉 পরের নামাজ: {next_namaz['name']} - {next_namaz['time']}"
        
        return result
    
    def get_namaz_status(self) -> Dict:
        """নামাজ স্ট্যাটাস"""
        completed = 0
        total = len(self.namaz_times)
        
        current_time = TimeHelper.get_current_time()
        current_hour = TimeHelper.format_time(current_time)
        
        for namaz, time_str in self.namaz_times.items():
            if current_hour > time_str:
                completed += 1
        
        return {
            'completed': completed,
            'total': total,
            'remaining': total - completed,
            'percentage': (completed / total) * 100 if total > 0 else 0
        }
