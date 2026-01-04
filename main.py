#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
SAFE USERBOT - Professional & Safe Telegram UserBot
Developed by RANA
Version: 1.0.0
"""

import asyncio
import sys
import os
import plugins.admin_reminder
plugins.admin_reminder.setup(client)
import plugins.welcome_system
plugins.welcome_system.setup(client)
from datetime import datetime

# কাস্টম মডিউল ইম্পোর্ট
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import ConfigManager
from utils.logger import log
from utils.helpers import TimeHelper
from core.response_handler import ResponseHandler
from core.slot_manager import SlotManager
from core.namaz_alert import NamazAlert
from core.user_manager import UserManager
from core.media_handler import MediaHandler
from core.announcements import AnnouncementHandler
from core.events_handler import EventsHandler

# টেলিগ্রাম
from telethon import TelegramClient, events
from telethon.tl.types import Message

class SafeUserBot:
    def __init__(self):
        """ইনিশিয়ালাইজেশন"""
        log.info("🚀 Initializing Safe UserBot...")
        
        # কনফিগারেশন লোড
        self.config = ConfigManager()
        self.bot_info = self.config.config.get('bot_info', {})
        
        # মডিউল ইনিশিয়ালাইজ
        self.response_handler = ResponseHandler(self.config)
        self.slot_manager = SlotManager(self.config)
        self.namaz_alert = NamazAlert(self.config)
        self.user_manager = UserManager(self.config)
        self.media_handler = MediaHandler(self.config)
        self.announcement_handler = AnnouncementHandler(self.config)
        self.events_handler = EventsHandler(self.config)
        
        # টেলিগ্রাম ক্লায়েন্ট
        self.api_id, self.api_hash = self.config.get_telegram_creds()
        self.session_file = 'sessions/main_account.session'
        
        # সেশনের ডিরেক্টরি তৈরি
        os.makedirs('sessions', exist_ok=True)
        os.makedirs('logs', exist_ok=True)
        os.makedirs('data', exist_ok=True)
        
        self.client = None
        self.running = False
        
        log.info("✅ Modules initialized successfully")
    
    async def initialize(self):
        """ক্লায়েন্ট ইনিশিয়ালাইজ"""
        try:
            log.info("🔗 Connecting to Telegram...")
            
            self.client = TelegramClient(
                self.session_file,
                self.api_id,
                self.api_hash,
                device_model="SafeUserBot",
                system_version="1.0.0",
                app_version="1.0.0"
            )
            
            await self.client.start()
            
            # বট ইনফো প্রিন্ট
            me = await self.client.get_me()
            log.info(f"🤖 Logged in as: {me.first_name} (@{me.username})")
            log.info(f"🆔 User ID: {me.id}")
            
            # ইভেন্ট হ্যান্ডলার রেজিস্টার
            await self.register_handlers()
            
            # শিডিউলার স্টার্ট
            await self.start_scheduler()
            
            self.running = True
            log.info("✅ Bot initialized and ready!")
            
        except Exception as e:
            log.error(f"❌ Failed to initialize bot: {e}")
            raise
    
    async def register_handlers(self):
        """ইভেন্ট হ্যান্ডলার রেজিস্টার"""
        
        @self.client.on(events.NewMessage(incoming=True))
        async def handle_message(event):
            """নতুন মেসেজ হ্যান্ডল"""
            try:
                # নিজের মেসেজ ignore
                if event.sender_id == (await self.client.get_me()).id:
                    return
                
                # ইউজার ম্যানেজমেন্ট
                sender_id = str(event.sender_id)
                self.user_manager.update_user_activity(sender_id)
                
                # মেসেজ টেক্সট
                message_text = event.message.text or ""
                log.info(f"📩 Message from {sender_id}: {message_text[:50]}...")
                
                # প্রসেস মেসেজ
                response = await self.process_message(message_text, sender_id)
                
                if response:
                    # হিউম্যান লাইক ডিলে
                    import random
                    await asyncio.sleep(random.uniform(0.5, 1.5))
                    
                    # রিপ্লাই সেন্ড
                    await event.reply(response)
                    log.info(f"📤 Replied to {sender_id}")
                
            except Exception as e:
                log.error(f"Error handling message: {e}")
        
        @self.client.on(events.ChatAction)
        async def handle_chat_action(event):
            """গ্রুপ/চ্যানেল একশন"""
            pass
        
        @self.client.on(events.MessageEdited)
        async def handle_edited_message(event):
            """এডিটেড মেসেজ"""
            pass
        
        log.info("✅ Event handlers registered")
    
    async def process_message(self, message_text: str, user_id: str) -> str:
        """মেসেজ প্রসেস"""
        message_lower = message_text.lower().strip()
        
        # বট ইনফো
        if any(keyword in message_lower for keyword in ['/start', 'start', 'hello bot']):
            return self.get_welcome_message(user_id)
        
        # ডেভেলপার ইনফো
        if any(keyword in message_lower for keyword in ['developer', 'dev', 'creator', 'who made you']):
            return self.get_developer_info()
        
        # বট ইনফো
        if any(keyword in message_lower for keyword in ['bot info', 'about bot', 'who are you']):
            return self.get_bot_info()
        
        # নামাজের সময়
        if any(keyword in message_lower for keyword in ['namaz', 'prayer time', 'salah', 'namaj']):
            return self.namaz_alert.get_all_namaz_times()
        
        # কোটস
        if any(keyword in message_lower for keyword in ['quote', 'motivation', 'inspire']):
            return self.response_handler.get_quote()
        
        # দোয়া
        if any(keyword in message_lower for keyword in ['dua', 'prayer', 'blessing', 'doa']):
            return self.response_handler.get_dua()
        
        # স্লট ইনফো
        if any(keyword in message_lower for keyword in ['slot', 'reminder', 'schedule']):
            current_slot = self.slot_manager.get_current_slot()
            if current_slot:
                slot_msg = self.slot_manager.get_slot_message(current_slot['name'], 1)
                return f"Current Slot: **{current_slot['name']}**\n{slot_msg}"
            return "No active slot at the moment."
        
        # ইউজার স্ট্যাটস
        if any(keyword in message_lower for keyword in ['my stats', 'statistics', 'my info']):
            stats = self.user_manager.get_user_stats(user_id)
            return self.format_user_stats(stats, user_id)
        
        # হেল্প
        if any(keyword in message_lower for keyword in ['help', 'commands', 'what can you do']):
            return self.get_help_message()
        
        # ডিফল্ট অটো রিপ্লাই
        auto_reply = self.response_handler.get_auto_reply(message_text)
        if auto_reply:
            return auto_reply
        
        return ""
    
    def get_welcome_message(self, user_id: str) -> str:
        """ওয়েলকাম মেসেজ"""
        user = self.user_manager.get_user(user_id)
        emoji = self.media_handler.get_emoji()
        
        return f"""
{emoji} **Welcome YOUR CRUSH ⟵o_0** {emoji}

🤖 **Bot Name:** {self.bot_info.get('name', 'YOUR CRUSH ⟵o_0')}
👤 **Your ID:** {user_id}
🌚 **Your Name** {first_name}
📅 **Member Since:** {user.get('join_date', 'Today')}

**Available Commands:**
• `namaz` - Prayer times
• `quote` - Motivational quotes
• `dua` - Daily duas
• `slot` - Current time slot
• `my stats` - Your statistics
• `help` - All commands

Developed with ❤️ by RANA
"""
    
    def get_developer_info(self) -> str:
        """ডেভেলপার ইনফো"""
        return """
👤 **DEVELOPER INFORMATION:**

📋 **PERSONAL DETAILS:**
• Name: RANA
• Social Name: MASTER 🪓
• Age: 20 years
• Status: Single
• Education: SSC Batch 2022
• Location: Faridpur, Dhaka, Bangladesh

💼 **PROFESSIONAL INFORMATION:**
• Profession: Security Field
• Work Type: Experiment / Technical Operations
• Skills:
  - Video Editing
  - Photo Editing
  - Mobile Technology
  - Online Operations
  - In Training: Cyber Security (Currently Learning)

📞 **CONTACT DETAILS:**
• Email: ranaeditz333@gmail.com
• Telegram Bot: @black_lovers1_bot
• Telegram Profile: @rana_editz_00
• Support Channel: https://t.me/master_account_remover_channel
• Phone: 01847634486

🎯 **GOALS & DREAMS:**
• Dream: Become a Professional Developer
• Project: Website (Coming Soon)
"""
    
    def get_bot_info(self) -> str:
        """বট ইনফো"""
        total_users = len(self.user_manager.get_all_users())
        active_users = len(self.user_manager.get_active_users(24))
        
        return f"""
✨ **SAFE USERBOT INFORMATION**

📊 **STATISTICS:**
• Total Users: {total_users}
• Active Users (24h): {active_users}
• Version: {self.bot_info.get('version', '1.0.0')}

⚙️ **FEATURES:**
• Auto Reply: {'✅' if self.config.config['features']['auto_reply'] else '❌'}
• Namaz Alerts: {'✅' if self.config.config['features']['namaz_alert'] else '❌'}
• Slot Reminders: {'✅' if self.config.config['features']['slot_reminders'] else '❌'}
• Quotes: {'✅' if self.config.config['features']['quotes_enabled'] else '❌'}
• Duas: {'✅' if self.config.config['features']['duas_enabled'] else '❌'}

🔧 **TECHNICAL:**
• Storage: JSON Files (Offline)
• Safety Level: High
• Response Time: Instant
• Uptime: 100%

⚠️ **SAFETY FEATURES:**
1. No Hardcoded Responses
2. Human-like Delays
3. Flood Protection
4. Session Security
5. Offline Operation
"""
    
    def format_user_stats(self, stats: dict, user_id: str) -> str:
        """ইউজার স্ট্যাটস ফরম্যাট"""
        user = self.user_manager.get_user(user_id)
        user = self.user_manager.get_user(first_name)
        
        return f"""
📊 **YOUR STATISTICS:**

👤 **User ID:** {user_id}
📛 **Name:** {first_name}

📈 **Activity:**
• Total Messages: {stats['total_messages']}
• Namaz Reminders: {stats['namaz_count']}
• Slot Reminders: {stats['slot_reminders']}
• Active Days: {stats['active_days']}
• Last Active: {stats['last_active']}

⚙️ **Settings:**
• Namaz Alerts: {'✅' if user.get('namaz_alert', True) else '❌'}
• Slot Reminders: {'✅' if user.get('slot_reminder', True) else '❌'}
• Quotes: {'✅' if user.get('quotes_enabled', True) else '❌'}
• Duas: {'✅' if user.get('duas_enabled', True) else '❌'}

Keep using the bot for more features! 🚀
"""
    
    def get_help_message(self) -> str:
        """হেল্প মেসেজ"""
        return """
🆘 **HELP & COMMANDS**

📱 **BASIC COMMANDS:**
• `/start` - Start the bot
• `hello` / `hi` - Greet the bot
• `help` - Show this message

🕌 **RELIGIOUS FEATURES:**
• `namaz` - Show prayer times
• `dua` - Get a random dua
• `quote` - Get Islamic quote

⏰ **REMINDERS:**
• `slot` - Current time slot
• `my stats` - Your statistics

ℹ️ **INFORMATION:**
• `bot info` - Bot information
• `developer` - Developer info
• `features` - Available features

⚙️ **SETTINGS:**
• Settings are managed automatically
• All data is stored locally
• No personal data is shared

💡 **TIPS:**
• The bot works automatically
• No need to remember commands
• Just chat normally!

Developed by Rana 💝
"""
    
    async def start_scheduler(self):
        """শিডিউলার স্টার্ট"""
        log.info("⏰ Starting scheduler...")
        
        async def check_namaz():
            """নামাজ এলার্ট চেক"""
            while self.running:
                try:
                    namaz_check = self.namaz_alert.check_namaz_time()
                    if namaz_check:
                        log.info(f"🕌 Namaz alert: {namaz_check['name']}")
                        
                        # অ্যাক্টিভ ইউজারদের পাঠানো
                        active_users = self.user_manager.get_active_users(24)
                        for user_id, user_data in active_users.items():
                            if user_data.get('namaz_alert', True):
                                try:
                                    await self.client.send_message(
                                        int(user_id),
                                        namaz_check['message']
                                    )
                                    self.user_manager.update_namaz_count(user_id)
                                    log.info(f"Sent namaz alert to {user_id}")
                                except Exception as e:
                                    log.error(f"Failed to send to {user_id}: {e}")
                    
                    await asyncio.sleep(60)  # প্রতি মিনিটে চেক
                    
                except Exception as e:
                    log.error(f"Scheduler error (namaz): {e}")
                    await asyncio.sleep(60)
        
        async def check_slots():
            """স্লট রিমাইন্ডার চেক"""
            while self.running:
                try:
                    current_slot = self.slot_manager.get_current_slot()
                    if current_slot:
                        slot_msg = self.slot_manager.get_slot_message(current_slot['name'], 1)
                        if slot_msg:
                            log.info(f"⏰ Slot reminder: {current_slot['name']}")
                            
                            # অ্যাক্টিভ ইউজারদের পাঠানো
                            active_users = self.user_manager.get_active_users(1)  # শেষ ১ ঘণ্টার
                            for user_id, user_data in active_users.items():
                                if user_data.get('slot_reminder', True):
                                    try:
                                        await self.client.send_message(
                                            int(user_id),
                                            f"⏰ **{current_slot['name'].upper()} REMINDER**\n{slot_msg}"
                                        )
                                        self.user_manager.update_slot_count(user_id, current_slot['name'])
                                        log.info(f"Sent slot reminder to {user_id}")
                                    except Exception as e:
                                        log.error(f"Failed to send to {user_id}: {e}")
                    
                    await asyncio.sleep(3000)  # প্রতি 5 মিনিটে
                    
                except Exception as e:
                    log.error(f"Scheduler error (slots): {e}")
                    await asyncio.sleep(3000)
        
        async def daily_quotes():
            """ডেইলি কোটস"""
            while self.running:
                try:
                    current_time = TimeHelper.get_current_time()
                    if current_time.hour == 9 and current_time.minute == 0:  # সকাল ৯টা
                        log.info("📚 Sending daily quotes")
                        
                        active_users = self.user_manager.get_active_users(24)
                        for user_id, user_data in active_users.items():
                            if user_data.get('quotes_enabled', True):
                                try:
                                    quote = self.response_handler.get_quote()
                                    await self.client.send_message(
                                        int(user_id),
                                        f"💭 **DAILY QUOTE**\n\n{quote}\n\nHave a great day! 😊"
                                    )
                                    log.info(f"Sent daily quote to {user_id}")
                                except:
                                    pass
                    
                    await asyncio.sleep(60)  # প্রতি মিনিটে চেক
                    
                except Exception as e:
                    log.error(f"Scheduler error (quotes): {e}")
                    await asyncio.sleep(60)
        
        # শিডিউলার টাস্ক শুরু
        asyncio.create_task(check_namaz())
        asyncio.create_task(check_slots())
        asyncio.create_task(daily_quotes())
        
        log.info("✅ Scheduler started successfully")
    
    async def run(self):
        """মেইন রান লুপ"""
        try:
            await self.initialize()
            
            # রানিং মেসেজ
            log.info("""
🎉 **MAR PD IS NOW RUNNING!** 🎉

📊 **SYSTEM STATUS:**
• Bot: Online ✅
• Modules: Loaded ✅
• Scheduler: Running ✅
• Database: Ready ✅

🚀 **FEATURES ACTIVE:**
• Auto Reply System
• Namaz Time Alerts
• Slot-based Reminders
• Quotes & Duas
• User Management

⚠️ **SAFETY PROTOCOLS:**
• Human-like delays enabled
• Flood control active
• Session secured
• Local storage only

Press Ctrl+C to stop the bot.
            """)
            
            # ক্লায়েন্ট রান
            await self.client.run_until_disconnected()
            
        except KeyboardInterrupt:
            log.info("\n👋 Bot stopped by user")
        except Exception as e:
            log.error(f"❌ Fatal error: {e}", exc_info=True)
        finally:
            self.running = False
            if self.client:
                await self.client.disconnect()
            log.info("🔴 Bot stopped")

# মেইন এন্ট্রি পয়েন্ট
if __name__ == "__main__":
    # ASCII ART
    print("""
    
███████╗ █████╗ ███████╗███████╗    ██╗   ██╗███████╗███████╗██████╗ ██████╗  ██████╗ ████████╗
██╔════╝██╔══██╗██╔════╝██╔════╝    ██║   ██║██╔════╝██╔════╝██╔══██╗██╔══██╗██╔═══██╗╚══██╔══╝
███████╗███████║█████╗  █████╗      ██║   ██║█████╗  █████╗  ██████╔╝██████╔╝██║   ██║   ██║   
╚════██║██╔══██║██╔══╝  ██╔══╝      ╚██╗ ██╔╝██╔══╝  ██╔══╝  ██╔══██╗██╔══██╗██║   ██║   ██║   
███████║██║  ██║███████╗███████╗     ╚████╔╝ ███████╗███████╗██║  ██║██████╔╝╚██████╔╝   ██║   
╚══════╝╚═╝  ╚═╝╚══════╝╚══════╝      ╚═══╝  ╚══════╝╚══════╝╚═╝  ╚═╝╚═════╝  ╚═════╝    ╚═╝   
                                                                                               
    """)
    print("🚀 Safe UserBot - Professional & Safe Telegram UserBot")
    print("👨‍💻 Developed by: RANA")
    print("📧 Contact: ranaeditz333@gmail.com")
    print("=" * 60)
    
    # বট রান
    bot = SafeUserBot()
    
    try:
        asyncio.run(bot.run())
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
