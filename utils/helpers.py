import json
import random
import time
import os
from datetime import datetime
import pytz
from typing import Dict, List, Any, Optional

class JSONHelper:
    @staticmethod
    def load_json(file_path: str) -> Dict:
        """JSON ফাইল লোড"""
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            print(f"❌ Error loading {file_path}: {e}")
            return {}
    
    @staticmethod
    def save_json(file_path: str, data: Dict) -> bool:
        """JSON ফাইল সেভ"""
        try:
            # ডিরেক্টরি তৈরি যদি না থাকে
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"❌ Error saving {file_path}: {e}")
            return False
    
    @staticmethod
    def get_random_response(responses: Any) -> str:
        """র্যান্ডম রেসপন্স সিলেক্ট"""
        if isinstance(responses, list) and responses:
            return random.choice(responses)
        elif isinstance(responses, str):
            return responses
        return ""
    
    @staticmethod
    def update_json(file_path: str, key: str, value: Any) -> bool:
        """JSON ফাইল আপডেট"""
        try:
            data = JSONHelper.load_json(file_path)
            data[key] = value
            return JSONHelper.save_json(file_path, data)
        except Exception as e:
            print(f"Error updating JSON: {e}")
            return False

class TimeHelper:
    @staticmethod
    def get_current_time(timezone: str = "Asia/Dhaka") -> datetime:
        """কারেন্ট টাইম গেট"""
        tz = pytz.timezone(timezone)
        return datetime.now(tz)
    
    @staticmethod
    def format_time(time_obj: datetime) -> str:
        """টাইম ফরম্যাট"""
        return time_obj.strftime("%H:%M")
    
    @staticmethod
    def format_datetime(time_obj: datetime) -> str:
        """ডেটটাইম ফরম্যাট"""
        return time_obj.strftime("%Y-%m-%d %H:%M:%S")
    
    @staticmethod
    def human_delay(min_seconds: float = 1.0, max_seconds: float = 2.5) -> None:
        """হিউম্যান লাইক ডিলে"""
        delay = random.uniform(min_seconds, max_seconds)
        time.sleep(delay)
    
    @staticmethod
    def parse_time(time_str: str) -> Optional[datetime]:
        """টাইম স্ট্রিং পার্স"""
        try:
            today = datetime.now().date()
            time_obj = datetime.strptime(time_str, "%H:%M").time()
            return datetime.combine(today, time_obj)
        except:
            return None

class TextHelper:
    @staticmethod
    def clean_text(text: str) -> str:
        """টেক্সট ক্লিন"""
        return text.lower().strip()
    
    @staticmethod
    def contains_keyword(text: str, keywords: List[str]) -> bool:
        """কীওয়ার্ড চেক"""
        text_lower = text.lower()
        return any(keyword.lower() in text_lower for keyword in keywords)
    
    @staticmethod
    def format_message(message: str, **kwargs) -> str:
        """মেসেজ ফরম্যাট"""
        for key, value in kwargs.items():
            message = message.replace(f"{{{key}}}", str(value))
        return message

class FileHelper:
    @staticmethod
    def ensure_directory(path: str) -> None:
        """ডিরেক্টরি নিশ্চিত"""
        os.makedirs(path, exist_ok=True)
    
    @staticmethod
    def file_exists(path: str) -> bool:
        """ফাইল এক্সিস্ট চেক"""
        return os.path.exists(path)
    
    @staticmethod
    def create_file_if_not_exists(path: str, default_content: Any = None) -> None:
        """ফাইল তৈরি যদি না থাকে"""
        if not os.path.exists(path):
            directory = os.path.dirname(path)
            if directory:
                os.makedirs(directory, exist_ok=True)
            
            if default_content is not None:
                if isinstance(default_content, (dict, list)):
                    with open(path, 'w', encoding='utf-8') as f:
                        json.dump(default_content, f, indent=4, ensure_ascii=False)
                else:
                    with open(path, 'w', encoding='utf-8') as f:
                        f.write(str(default_content))