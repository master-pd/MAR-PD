from datetime import datetime
from typing import List, Dict
from utils.helpers import JSONHelper, TimeHelper

class EventNotifier:
    def __init__(self):
        self.events_file = 'data/events.json'
        self.events = JSONHelper.load_json(self.events_file)
    
    def check_today_events(self) -> List[Dict]:
        """আজকের ইভেন্ট চেক"""
        today = TimeHelper.get_current_time().strftime("%Y-%m-%d")
        today_events = []
        
        for event_id, event_data in self.events.items():
            if event_data.get('date') == today:
                today_events.append({
                    'id': event_id,
                    **event_data
                })
        
        return today_events
    
    def get_upcoming_events(self, days: int = 7) -> List[Dict]:
        """আপকামিং ইভেন্ট"""
        current_date = TimeHelper.get_current_time()
        upcoming_events = []
        
        for event_id, event_data in self.events.items():
            event_date_str = event_data.get('date')
            if event_date_str:
                try:
                    event_date = datetime.fromisoformat(event_date_str)
                    days_diff = (event_date.date() - current_date.date()).days
                    if 0 <= days_diff <= days:
                        upcoming_events.append({
                            'id': event_id,
                            'days_until': days_diff,
                            **event_data
                        })
                except:
                    continue
        
        # সর্ট বাই ডেট
        upcoming_events.sort(key=lambda x: x.get('date', ''))
        return upcoming_events