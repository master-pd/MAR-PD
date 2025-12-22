"""
স্যাম্পল প্লাগিন - কিভাবে নতুন প্লাগিন তৈরি করবেন
"""

from typing import Dict, Any
from telethon import events

class SamplePlugin:
    def __init__(self, bot):
        self.bot = bot
        self.name = "Sample Plugin"
        self.version = "1.0.0"
        self.description = "একটি স্যাম্পল প্লাগিন"
        
        # রেজিস্টার ইভেন্ট হ্যান্ডলার
        self.register_handlers()
    
    def register_handlers(self):
        """ইভেন্ট হ্যান্ডলার রেজিস্টার"""
        
        @self.bot.client.on(events.NewMessage(pattern='(?i)/sample'))
        async def handle_sample_command(event):
            """স্যাম্পল কমান্ড হ্যান্ডল"""
            await event.reply("🎯 This is a sample plugin response!")
        
        @self.bot.client.on(events.NewMessage(pattern='(?i)plugin info'))
        async def handle_plugin_info(event):
            """প্লাগিন ইনফো"""
            info = f"""
🔌 **Plugin Information:**

📛 Name: {self.name}
📦 Version: {self.version}
📝 Description: {self.description}
📊 Status: Active ✅

This plugin demonstrates how to create new features.
            """
            await event.reply(info)
    
    def get_plugin_info(self) -> Dict[str, Any]:
        """প্লাগিন ইনফো"""
        return {
            "name": self.name,
            "version": self.version,
            "description": self.description,
            "author": "RANA",
            "enabled": True
        }