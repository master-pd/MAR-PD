from typing import Dict, List, Optional
from utils.helpers import JSONHelper, TimeHelper
from config import ConfigManager
from datetime import datetime

class EventsHandler:
    def __init__(self, config_manager: ConfigManager):
        self.config = config_manager
        self.events_file = self.config.get_response_file("events")
        self.events = JSONHelper.load_json(self.events_file)
    
    def get_today_events(self) -> List[Dict]:
        """আজকের ইভেন্ট"""
        today = TimeHelper.get_current_time().strftime("%m-%d")
        today_events = []
        
        for event_id, event_data in self.events.items():
            if event_data.get('date', '').endswith(today):
                today_events.append({
                    'id': event_id,
                    **event_data
                })
        
        return today_events
    
    def add_event(self, event_data: Dict) -> bool:
        """নতুন ইভেন্ট যোগ"""
        import uuid
        event_id = str(uuid.uuid4())[:8]
        
        self.events[event_id] = event_data
        return JSONHelper.save_json(self.events_file, self.events)
    
    def delete_event(self, event_id: str) -> bool:
        """ইভেন্ট ডিলিট"""
        if event_id in self.events:
            del self.events[event_id]
            return JSONHelper.save_json(self.events_file, self.events)
        return False