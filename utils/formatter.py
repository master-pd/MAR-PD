"""
ফরম্যাটার ইউটিলিটি - Safe UserBot
"""

from datetime import datetime
from typing import Dict, List, Any
import textwrap

class Formatter:
    @staticmethod
    def format_time_delta(seconds: int) -> str:
        """সেকেন্ডকে রিডেবল টাইমে ফরম্যাট"""
        if seconds < 60:
            return f"{seconds} seconds"
        elif seconds < 3600:
            minutes = seconds // 60
            return f"{minutes} minute{'s' if minutes > 1 else ''}"
        elif seconds < 86400:
            hours = seconds // 3600
            return f"{hours} hour{'s' if hours > 1 else ''}"
        else:
            days = seconds // 86400
            return f"{days} day{'s' if days > 1 else ''}"
    
    @staticmethod
    def format_file_size(bytes_size: int) -> str:
        """বাইটসকে রিডেবল সাইজে ফরম্যাট"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if bytes_size < 1024.0:
                return f"{bytes_size:.2f} {unit}"
            bytes_size /= 1024.0
        return f"{bytes_size:.2f} TB"
    
    @staticmethod
    def format_number(number: int) -> str:
        """সংখ্যা ফরম্যাট (১,০০০ কমা সহ)"""
        return f"{number:,}"
    
    @staticmethod
    def format_percentage(value: float, total: float) -> str:
        """পারসেন্টেজ ফরম্যাট"""
        if total == 0:
            return "0%"
        percentage = (value / total) * 100
        return f"{percentage:.1f}%"
    
    @staticmethod
    def format_message(message: str, width: int = 50) -> str:
        """মেসেজ র্যাপ ফরম্যাট"""
        return textwrap.fill(message, width=width)
    
    @staticmethod
    def format_list(items: List[str], bullet: str = "•") -> str:
        """লিস্ট ফরম্যাট"""
        return "\n".join(f"{bullet} {item}" for item in items)
    
    @staticmethod
    def format_table(headers: List[str], rows: List[List[str]]) -> str:
        """টেবিল ফরম্যাট"""
        if not headers or not rows:
            return ""
        
        # কলাম প্রস্থ ক্যালকুলেট
        col_widths = [len(str(h)) for h in headers]
        for row in rows:
            for i, cell in enumerate(row):
                if i < len(col_widths):
                    col_widths[i] = max(col_widths[i], len(str(cell)))
        
        # হেডার তৈরি
        header_line = " | ".join(str(h).ljust(col_widths[i]) for i, h in enumerate(headers))
        separator = "-+-".join("-" * w for w in col_widths)
        
        # টেবিল তৈরি
        table_lines = [header_line, separator]
        for row in rows:
            row_line = " | ".join(str(cell).ljust(col_widths[i]) for i, cell in enumerate(row))
            table_lines.append(row_line)
        
        return "\n".join(table_lines)
    
    @staticmethod
    def format_json_pretty(data: Dict) -> str:
        """JSON প্রিটি প্রিন্ট"""
        import json
        return json.dumps(data, indent=2, ensure_ascii=False)
    
    @staticmethod
    def format_duration(start_time: datetime, end_time: datetime = None) -> str:
        """ডিউরেশন ফরম্যাট"""
        if not end_time:
            end_time = datetime.now()
        
        delta = end_time - start_time
        total_seconds = int(delta.total_seconds())
        
        if total_seconds < 60:
            return f"{total_seconds} seconds"
        elif total_seconds < 3600:
            minutes = total_seconds // 60
            seconds = total_seconds % 60
            return f"{minutes}m {seconds}s"
        elif total_seconds < 86400:
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            return f"{hours}h {minutes}m"
        else:
            days = total_seconds // 86400
            hours = (total_seconds % 86400) // 3600
            return f"{days}d {hours}h"
    
    @staticmethod
    def format_progress_bar(percentage: float, width: int = 20) -> str:
        """প্রোগ্রেস বার ফরম্যাট"""
        filled = int(width * percentage / 100)
        bar = "█" * filled + "░" * (width - filled)
        return f"[{bar}] {percentage:.1f}%"
    
    @staticmethod
    def format_user_mention(user_id: int, username: str = None, name: str = None) -> str:
        """ইউজার মেনশন ফরম্যাট"""
        if username:
            return f"@{username}"
        elif name:
            return f"[{name}](tg://user?id={user_id})"
        else:
            return f"User {user_id}"