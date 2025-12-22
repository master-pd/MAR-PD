"""
ভ্যালিডেশন ইউটিলিটি - Safe UserBot
"""

import re
from datetime import datetime
from typing import Dict, List, Any, Optional

class Validator:
    @staticmethod
    def validate_time(time_str: str) -> bool:
        """টাইম ভ্যালিডেশন (HH:MM ফরম্যাট)"""
        pattern = r'^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$'
        return bool(re.match(pattern, time_str))
    
    @staticmethod
    def validate_date(date_str: str) -> bool:
        """ডেট ভ্যালিডেশন (YYYY-MM-DD ফরম্যাট)"""
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            return True
        except ValueError:
            return False
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """ইমেইল ভ্যালিডেশন"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def validate_phone(phone: str) -> bool:
        """ফোন নম্বর ভ্যালিডেশন (বাংলাদেশ)"""
        pattern = r'^01[3-9]\d{8}$'
        return bool(re.match(pattern, phone))
    
    @staticmethod
    def validate_json_structure(data: Dict, required_keys: List[str]) -> bool:
        """JSON স্ট্রাকচার ভ্যালিডেশন"""
        return all(key in data for key in required_keys)
    
    @staticmethod
    def validate_user_id(user_id: Any) -> bool:
        """ইউজার আইডি ভ্যালিডেশন"""
        try:
            user_id_str = str(user_id)
            return user_id_str.isdigit() and len(user_id_str) >= 6
        except:
            return False
    
    @staticmethod
    def validate_message_length(message: str, max_length: int = 4000) -> bool:
        """মেসেজ লেংথ ভ্যালিডেশন"""
        return len(message) <= max_length
    
    @staticmethod
    def validate_slot_data(slot_data: Dict) -> List[str]:
        """স্লট ডেটা ভ্যালিডেশন"""
        errors = []
        
        required_fields = ['name', 'start', 'end', 'level1']
        for field in required_fields:
            if field not in slot_data:
                errors.append(f"Missing required field: {field}")
        
        if 'name' in slot_data and not isinstance(slot_data['name'], str):
            errors.append("Slot name must be a string")
        
        if 'start' in slot_data and not Validator.validate_time(slot_data['start']):
            errors.append("Invalid start time format (HH:MM)")
        
        if 'end' in slot_data and not Validator.validate_time(slot_data['end']):
            errors.append("Invalid end time format (HH:MM)")
        
        if 'start' in slot_data and 'end' in slot_data:
            if slot_data['start'] >= slot_data['end']:
                errors.append("Start time must be before end time")
        
        return errors
    
    @staticmethod
    def validate_namaz_time(time_str: str) -> bool:
        """নামাজের সময় ভ্যালিডেশন"""
        if not Validator.validate_time(time_str):
            return False
        
        # ভ্যালিড টাইম রেঞ্জ চেক
        try:
            hour, minute = map(int, time_str.split(':'))
            return 0 <= hour <= 23 and 0 <= minute <= 59
        except:
            return False
    
    @staticmethod
    def sanitize_input(text: str) -> str:
        """ইনপুট স্যানিটাইজেশন"""
        # বেসিক HTML/JS ইনজেকশন প্রোটেকশন
        replacements = {
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#x27;',
            '`': '&#x60;',
            '&': '&amp;'
        }
        
        for char, replacement in replacements.items():
            text = text.replace(char, replacement)
        
        # এক্সট্রা স্পেস রিমুভ
        text = ' '.join(text.split())
        
        return text.strip()
    
    @staticmethod
    def validate_file_extension(filename: str, allowed_extensions: List[str]) -> bool:
        """ফাইল এক্সটেনশন ভ্যালিডেশন"""
        return any(filename.lower().endswith(ext) for ext in allowed_extensions)
    
    @staticmethod
    def validate_file_size(file_path: str, max_size_mb: float) -> bool:
        """ফাইল সাইজ ভ্যালিডেশন"""
        try:
            import os
            size_bytes = os.path.getsize(file_path)
            size_mb = size_bytes / (1024 * 1024)
            return size_mb <= max_size_mb
        except:
            return False