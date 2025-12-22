from datetime import datetime, timedelta
from core.namaz_alert import NamazAlert

class PrayerNotifier:
    def __init__(self, namaz_alert: NamazAlert):
        self.namaz_alert = namaz_alert
        self.sent_alerts = {}
    
    def check_and_notify(self) -> Dict:
        """নামাজের সময় চেক এবং নোটিফাই"""
        current_date = datetime.now().date().isoformat()
        
        if current_date not in self.sent_alerts:
            self.sent_alerts[current_date] = []
        
        namaz_check = self.namaz_alert.check_namaz_time(minutes_before=5)
        
        if namaz_check and namaz_check['name'] not in self.sent_alerts[current_date]:
            self.sent_alerts[current_date].append(namaz_check['name'])
            return namaz_check
        
        return None
    
    def get_daily_summary(self) -> str:
        """ডেইলি সামারি"""
        status = self.namaz_alert.get_namaz_status()
        
        summary = f"📊 **আজকের নামাজ স্ট্যাটাস:**\n\n"
        summary += f"✅ সম্পন্ন: {status['completed']}/{status['total']}\n"
        summary += f"⏳ বাকি: {status['remaining']}\n"
        summary += f"📈 অগ্রগতি: {status['percentage']:.1f}%\n"
        
        next_namaz = self.namaz_alert.get_next_namaz()
        summary += f"\n👉 পরের নামাজ: **{next_namaz['name']}** - {next_namaz['time']}"
        
        return summary