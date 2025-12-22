from typing import Dict, List, Optional
from utils.helpers import JSONHelper, TimeHelper
from config import ConfigManager

class SlotManager:
    def __init__(self, config_manager: ConfigManager):
        self.config = config_manager
        self.slots_file = self.config.get_response_file("slot")
        self.slots = self.load_slots()
    
    def load_slots(self) -> List[Dict]:
        """স্লট লোড"""
        data = JSONHelper.load_json(self.slots_file)
        return data.get('slots', [])
    
    def save_slots(self) -> bool:
        """স্লট সেভ"""
        data = {"slots": self.slots}
        return JSONHelper.save_json(self.slots_file, data)
    
    def get_current_slot(self) -> Optional[Dict]:
        """কারেন্ট স্লট চেক"""
        current_time = TimeHelper.get_current_time()
        current_hour = TimeHelper.format_time(current_time)
        
        for slot in self.slots:
            if slot['start'] <= current_hour <= slot['end']:
                return slot
        
        return None
    
    def get_slot_by_name(self, slot_name: str) -> Optional[Dict]:
        """নামে স্লট খুঁজুন"""
        for slot in self.slots:
            if slot['name'] == slot_name:
                return slot
        return None
    
    def get_slot_message(self, slot_name: str, level: int = 1) -> Optional[str]:
        """স্লট মেসেজ"""
        slot = self.get_slot_by_name(slot_name)
        if slot:
            level_key = f'level{level}'
            return slot.get(level_key)
        return None
    
    def add_slot(self, slot_data: Dict) -> bool:
        """নতুন স্লট যোগ"""
        # ভ্যালিডেশন
        required_fields = ['name', 'start', 'end', 'level1']
        for field in required_fields:
            if field not in slot_data:
                return False
        
        # ডুপ্লিকেট চেক
        for slot in self.slots:
            if slot['name'] == slot_data['name']:
                return False
        
        self.slots.append(slot_data)
        return self.save_slots()
    
    def remove_slot(self, slot_name: str) -> bool:
        """স্লট রিমুভ"""
        for i, slot in enumerate(self.slots):
            if slot['name'] == slot_name:
                self.slots.pop(i)
                return self.save_slots()
        return False
    
    def update_slot(self, slot_name: str, new_data: Dict) -> bool:
        """স্লট আপডেট"""
        for i, slot in enumerate(self.slots):
            if slot['name'] == slot_name:
                self.slots[i] = {**slot, **new_data}
                return self.save_slots()
        return False
    
    def get_all_slots(self) -> List[Dict]:
        """সব স্লট"""
        return self.slots
    
    def get_upcoming_slot(self) -> Optional[Dict]:
        """আপকামিং স্লট"""
        current_time = TimeHelper.get_current_time()
        current_hour = TimeHelper.format_time(current_time)
        
        upcoming_slots = []
        for slot in self.slots:
            if slot['start'] > current_hour:
                upcoming_slots.append(slot)
        
        if upcoming_slots:
            # সবচেয়ে আগের স্লট
            upcoming_slots.sort(key=lambda x: x['start'])
            return upcoming_slots[0]
        
        return None