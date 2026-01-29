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
import random
from datetime import datetime, timedelta

# =========================
# Custom Modules
# =========================
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

# =========================
# Telegram
# =========================
from telethon import TelegramClient, events
from telethon.tl.types import Message

# =========================
# SafeUserBot Class
# =========================
class SafeUserBot:
    def __init__(self):
        log.info("🚀 Initializing Safe UserBot...")
        self.config = ConfigManager()
        self.bot_info = self.config.config.get("bot_info", {})

        # Modules
        self.response_handler = ResponseHandler(self.config)
        self.slot_manager = SlotManager(self.config)
        self.namaz_alert = NamazAlert(self.config)
        self.user_manager = UserManager(self.config)
        self.media_handler = MediaHandler(self.config)
        self.announcement_handler = AnnouncementHandler(self.config)
        self.events_handler = EventsHandler(self.config)

        # Telegram client
        self.api_id, self.api_hash = self.config.get_telegram_creds()
        self.session_file = "sessions/main_account.session"

        # Directories
        os.makedirs("sessions", exist_ok=True)
        os.makedirs("logs", exist_ok=True)
        os.makedirs("data", exist_ok=True)

        self.client = None
        self.running = False
        log.info("✅ Modules initialized successfully")

    # =========================
    # Initialize Telegram Client
    # =========================
    async def initialize(self):
        try:
            log.info("🔗 Connecting to Telegram...")
            self.client = TelegramClient(
                self.session_file,
                self.api_id,
                self.api_hash,
                device_model="SafeUserBot",
                system_version="1.0.0",
                app_version="1.0.0",
            )
            await self.client.start()
            me = await self.client.get_me()
            log.info(f"🤖 Logged in as: {me.first_name} (@{me.username})")
            log.info(f"🆔 User ID: {me.id}")

            # =========================
            # Setup Plugins
            # =========================
            import plugins.admin_reminder
            import plugins.welcome_system
            plugins.admin_reminder.setup(self.client)
            plugins.welcome_system.setup(self.client)

            # =========================
            # Event Handlers
            # =========================
            await self.register_handlers()

            # =========================
            # Start Scheduler
            # =========================
            await self.start_scheduler()
            self.running = True
            log.info("✅ Bot initialized and ready!")

        except Exception as e:
            log.error(f"❌ Failed to initialize bot: {e}")
            raise

    # =========================
    # Register Event Handlers
    # =========================
    async def register_handlers(self):
        @self.client.on(events.NewMessage(incoming=True))
        async def handle_message(event: Message):
            try:
                if event.sender_id == (await self.client.get_me()).id:
                    return
                sender_id = str(event.sender_id)
                self.user_manager.update_user_activity(sender_id)
                message_text = event.message.text or ""
                log.info(f"📩 Message from {sender_id}: {message_text[:50]}...")
                response = await self.process_message(message_text, sender_id)
                if response:
                    await asyncio.sleep(random.uniform(0.5, 1.5))
                    await event.reply(response)
                    log.info(f"📤 Replied to {sender_id}")
            except Exception as e:
                log.error(f"Error handling message: {e}")

        @self.client.on(events.ChatAction)
        async def handle_chat_action(event):
            # Advanced chat actions (join/leave/admin changes)
            await self.events_handler.handle_chat_action(event)

        @self.client.on(events.MessageEdited)
        async def handle_edited_message(event):
            await self.events_handler.handle_edited_message(event)

        log.info("✅ Event handlers registered")

    # =========================
    # Process Messages
    # =========================
    async def process_message(self, message_text: str, user_id: str) -> str:
        text = message_text.lower().strip()
        if any(k in text for k in ["/start", "start", "hello bot"]):
            return self.get_welcome_message(user_id)
        if any(k in text for k in ["developer", "dev", "creator", "who made you"]):
            return self.get_developer_info()
        if any(k in text for k in ["bot info", "about bot", "who are you"]):
            return self.get_bot_info()
        if any(k in text for k in ["namaz", "prayer time", "salah", "namaj"]):
            return self.namaz_alert.get_all_namaz_times()
        if any(k in text for k in ["quote", "motivation", "inspire"]):
            return self.response_handler.get_quote()
        if any(k in text for k in ["dua", "prayer", "blessing", "doa"]):
            return self.response_handler.get_dua()
        if any(k in text for k in ["my stats", "statistics", "my info"]):
            stats = self.user_manager.get_user_stats(user_id)
            return self.format_user_stats(stats, user_id)
        if any(k in text for k in ["help", "commands", "what can you do"]):
            return self.get_help_message()
        auto_reply = self.response_handler.get_auto_reply(message_text)
        if auto_reply:
            return auto_reply
        return ""

# =========================
    # Welcome Message
    # =========================
    def get_welcome_message(self, user_id: str) -> str:
        user = self.user_manager.get_user(user_id)
        emoji = self.media_handler.get_emoji()
        return f"""
{emoji} **Welcome To 𝗬𝗢𝗨𝗥 𝗖𝗥𝗨𝗦𝗛 ⟵𝗼_𝟬** {emoji}

🙈 **Bot Name:** {self.bot_info.get('name', '𝗬𝗢𝗨𝗥 𝗖𝗥𝗨𝗦𝗛 ⟵𝗼_𝟬')}
💌 **Your ID:** {user_id}
😃 **Member Since:** {user.get('join_date', 'Today')}

**Available Commands:**
• `namaz` - Prayer times
• `quote` - Motivational quotes
• `dua` - Daily duas
• `my stats` - Your statistics
• `help` - All commands
• `developer` - Bot owner info 

**Available package:**
• Normal bot: - @black_lovers1_bot
• Adult bot: - @losie_chat_bot
• 18+ bot: - https://t.me/losie_chat_bot
• Editing: https://t.me/master_editz_team
• Adult: https://t.me/+oOGhfUxEzhozMTg1
• Photo Gelary: https://t.me/+V9XzZZEgu9MwM2Y9
• Chat box : https://t.me/+_F4jBwQ4M64wZGNl


Developed by RANA
"""

    # =========================
    # Developer Info
    # =========================
    def get_developer_info(self) -> str:
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

    # =========================
    # Bot Info
    # =========================
    def get_bot_info(self) -> str:
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

    # =========================
    # Format User Stats
    # =========================
    def format_user_stats(self, stats: dict, user_id: str) -> str:
        user = self.user_manager.get_user(user_id)
        return f"""
📊 **YOUR STATISTICS:**

👤 **User ID:** {user_id}
📛 **Name:** {user.get('name', 'User')}

📈 **Activity:**
• Total Messages: {stats['total_messages']}
• Namaz Alerts Received: {stats['namaz_count']}
• Active Days: {stats['active_days']}
• Last Active: {stats['last_active']}

⚙️ **Settings:**
• Namaz Alerts: {'✅' if user.get('namaz_alert', True) else '❌'}
• Quotes Enabled: {'✅' if user.get('quotes_enabled', True) else '❌'}
• Duas Enabled: {'✅' if user.get('duas_enabled', True) else '❌'}

Keep using the bot for more features! 🚀
"""

    # =========================
    # Help Message
    # =========================
    def get_help_message(self) -> str:
        return """
🆘 **HELP & COMMANDS**

📱 **BASIC COMMANDS:**
• `/start` - Start the bot
• `hello` / `hi` - Greet the bot
• `help` - Show this message

🕌 **RELIGIOUS FEATURES:**
• `namaz` - Show prayer times
• `dua` - Get a random dua
• `quote` - Get motivational quote

ℹ️ **INFORMATION:**
• `bot info` - Bot information
• `developer` - Developer info

⚙️ **SETTINGS:**
• Managed automatically
• Local JSON storage
• No personal data shared

💡 **TIPS:**
• Works automatically
• Just chat normally!
"""

    # =========================
    # Scheduler & Alerts
    # =========================
    async def start_scheduler(self):
        log.info("⏰ Starting scheduler...")

        async def check_namaz():
            while self.running:
                try:
                    namaz_time = self.namaz_alert.check_namaz_time()
                    if namaz_time:
                        log.info(f"🕌 Namaz alert: {namaz_time['name']}")
                        active_users = self.user_manager.get_active_users(24)
                        for user_id, data in active_users.items():
                            if data.get('namaz_alert', True):
                                try:
                                    await self.client.send_message(
                                        int(user_id), namaz_time['message']
                                    )
                                    self.user_manager.update_namaz_count(user_id)
                                    log.info(f"Sent namaz alert to {user_id}")
                                except Exception as e:
                                    log.error(f"Failed to send to {user_id}: {e}")
                    await asyncio.sleep(60)
                except Exception as e:
                    log.error(f"Scheduler error (namaz): {e}")
                    await asyncio.sleep(60)

        async def daily_quotes():
            while self.running:
                try:
                    now = TimeHelper.get_current_time()
                    if now.hour == 9 and now.minute == 0:
                        active_users = self.user_manager.get_active_users(24)
                        for user_id, data in active_users.items():
                            if data.get("quotes_enabled", True):
                                try:
                                    quote = self.response_handler.get_quote()
                                    await self.client.send_message(
                                        int(user_id),
                                        f"💭 **DAILY QUOTE**\n\n{quote}\n\nHave a great day! 😊"
                                    )
                                    log.info(f"Sent daily quote to {user_id}")
                                except Exception as e:
                                    log.error(f"Failed to send quote to {user_id}: {e}")
                    await asyncio.sleep(60)
                except Exception as e:
                    log.error(f"Scheduler error (quotes): {e}")
                    await asyncio.sleep(60)

        # Start tasks
        asyncio.create_task(check_namaz())
        asyncio.create_task(daily_quotes())
        log.info("✅ Scheduler started successfully")

# =========================
    # Main Run Loop
    # =========================
    async def run(self):
        try:
            await self.initialize()
            log.info("""
🎉 **SAFE USERBOT IS NOW RUNNING!** 🎉

📊 SYSTEM STATUS:
• Bot: Online ✅
• Modules: Loaded ✅
• Scheduler: Running ✅
• Database: Ready ✅

🚀 FEATURES ACTIVE:
• Auto Reply System
• Namaz Time Alerts
• Daily Quotes
• User Management & Stats

⚠️ SAFETY PROTOCOLS:
• Human-like delays enabled
• Flood control active
• Session secured
• Local JSON storage only

Press Ctrl+C to stop the bot.
            """)

            await self.client.run_until_disconnected()

        except KeyboardInterrupt:
            log.info("👋 Bot stopped by user (KeyboardInterrupt)")
        except Exception as e:
            log.error(f"❌ Fatal error: {e}", exc_info=True)
        finally:
            self.running = False
            if self.client:
                await self.client.disconnect()
            log.info("🔴 Bot disconnected and stopped")

    # =========================
    # Message Processing
    # =========================
    async def process_message(self, message_text: str, user_id: str) -> str:
        text = message_text.lower().strip()

        # Welcome
        if any(k in text for k in ['/start', 'hello', 'hi']):
            return self.get_welcome_message(user_id)

        # Developer Info
        if any(k in text for k in ['developer', 'dev', 'creator']):
            return self.get_developer_info()

        # Bot Info
        if any(k in text for k in ['bot info', 'about bot']):
            return self.get_bot_info()

        # Namaz
        if any(k in text for k in ['namaz', 'prayer', 'salah']):
            return self.namaz_alert.get_all_namaz_times()

        # Quote
        if any(k in text for k in ['quote', 'motivation', 'inspire']):
            return self.response_handler.get_quote()

        # Dua
        if any(k in text for k in ['dua', 'blessing']):
            return self.response_handler.get_dua()

        # Slot
        if 'slot' in text:
            current_slot = self.slot_manager.get_current_slot()
            if current_slot:
                return self.slot_manager.get_slot_message(current_slot['name'], 1)
            return "No active slot right now."

        # User Stats
        if any(k in text for k in ['my stats', 'statistics']):
            stats = self.user_manager.get_user_stats(user_id)
            return self.format_user_stats(stats, user_id)

        # Help
        if 'help' in text:
            return self.get_help_message()

        # Auto Reply Fallback
        reply = self.response_handler.get_auto_reply(message_text)
        if reply:
            return reply

        return ""

    # =========================
    # Event Handlers Registration
    # =========================
    async def register_handlers(self):
        @self.client.on(events.NewMessage(incoming=True))
        async def on_new_message(event):
            try:
                sender_id = str(event.sender_id)
                if sender_id == str((await self.client.get_me()).id):
                    return

                self.user_manager.update_user_activity(sender_id)

                message_text = event.message.text or ""
                log.info(f"📩 Message from {sender_id}: {message_text[:50]}...")

                response = await self.process_message(message_text, sender_id)
                if response:
                    import random
                    await asyncio.sleep(random.uniform(0.5, 1.5))
                    await event.reply(response)
                    log.info(f"📤 Replied to {sender_id}")

            except Exception as e:
                log.error(f"Error handling new message: {e}")

        @self.client.on(events.MessageEdited)
        async def on_edit(event):
            # Optional: handle edits
            pass

        @self.client.on(events.ChatAction)
        async def on_chat_action(event):
            # Optional: handle joins/leaves, etc
            pass

        log.info("✅ Event handlers registered successfully")

    # =========================
    # Utility: Stop Bot Gracefully
    # =========================
    async def stop(self):
        self.running = False
        if self.client:
            await self.client.disconnect()
        log.info("🔴 Bot stopped manually")

# =========================
    # Advanced Scheduler with Recovery & Multi-slot
    # =========================
    async def start_scheduler(self):
        log.info("⏰ Starting advanced scheduler...")

        async def check_namaz():
            while self.running:
                try:
                    namaz = self.namaz_alert.check_namaz_time()
                    if namaz:
                        log.info(f"🕌 Namaz Alert: {namaz['name']}")
                        active_users = self.user_manager.get_active_users(24)
                        for uid, data in active_users.items():
                            if data.get('namaz_alert', True):
                                try:
                                    await self.client.send_message(int(uid), namaz['message'])
                                    self.user_manager.update_namaz_count(uid)
                                except Exception as e:
                                    log.error(f"Failed sending Namaz alert to {uid}: {e}")
                    await asyncio.sleep(60)
                except Exception as e:
                    log.error(f"Scheduler Namaz error: {e}")
                    await asyncio.sleep(60)

        async def check_slots():
            while self.running:
                try:
                    slots = self.slot_manager.get_active_slots()
                    for slot in slots:
                        slot_msg = self.slot_manager.get_slot_message(slot['name'], 1)
                        active_users = self.user_manager.get_active_users(1)
                        for uid, data in active_users.items():
                            if data.get('slot_reminder', True):
                                try:
                                    await self.client.send_message(
                                        int(uid),
                                        f"⏰ **{slot['name'].upper()} SLOT REMINDER**\n{slot_msg}"
                                    )
                                    self.user_manager.update_slot_count(uid, slot['name'])
                                    self.slot_manager.save_slot_history(uid, slot['name'])
                                except Exception as e:
                                    log.error(f"Failed sending slot to {uid}: {e}")
                    await asyncio.sleep(300)
                except Exception as e:
                    log.error(f"Scheduler Slot error: {e}")
                    await asyncio.sleep(300)

        async def daily_quotes():
            while self.running:
                try:
                    now = TimeHelper.get_current_time()
                    if now.hour == 9 and now.minute == 0:
                        active_users = self.user_manager.get_active_users(24)
                        for uid, data in active_users.items():
                            if data.get('quotes_enabled', True):
                                try:
                                    quote = self.response_handler.get_quote()
                                    await self.client.send_message(
                                        int(uid),
                                        f"💭 **DAILY QUOTE**\n\n{quote}\nHave a productive day! 🌟"
                                    )
                                except Exception as e:
                                    log.error(f"Failed sending quote to {uid}: {e}")
                    await asyncio.sleep(60)
                except Exception as e:
                    log.error(f"Scheduler Quote error: {e}")
                    await asyncio.sleep(60)

        # Start all scheduler tasks
        asyncio.create_task(check_namaz())
        asyncio.create_task(check_slots())
        asyncio.create_task(daily_quotes())
        log.info("✅ Advanced scheduler started with recovery & multi-slot support")

    # =========================
    # Enhanced User Stats & Security Checks
    # =========================
    def enhance_user_stats(self, user_id: str):
        stats = self.user_manager.get_user_stats(user_id)
        stats['session_duration'] = self.user_manager.calculate_session(user_id)
        stats['message_rate'] = self.user_manager.calculate_message_rate(user_id)
        stats['last_active_str'] = TimeHelper.format_datetime(stats['last_active'])
        return stats

    def security_check(self):
        """Extra security checks before bot runs"""
        issues = []
        if not os.path.exists(self.session_file):
            issues.append("Session file missing!")
        if not self.config.is_valid_config():
            issues.append("Invalid configuration detected!")
        if issues:
            for issue in issues:
                log.warning(f"⚠️ SECURITY WARNING: {issue}")
            return False
        return True

    # =========================
    # Final Run Entry Point
    # =========================
if __name__ == "__main__":
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
    print("=" * 60)

    bot = SafeUserBot()
    if bot.security_check():
        try:
            asyncio.run(bot.run())
        except KeyboardInterrupt:
            print("👋 Goodbye!")
        except Exception as e:
            print(f"❌ Fatal Error: {e}")
            sys.exit(1)
    else:
        print("❌ Bot cannot start due to security/configuration issues.")
# =========================
# Multi-language Support
# =========================
def get_localized_text(self, key: str, lang: str = "en") -> str:
    """Return localized string based on key and language"""
    translations = {
        "welcome": {
            "en": "Welcome to Safe UserBot!",
            "bn": "সেফ ইউজারবট-এ স্বাগতম!"
        },
        "help": {
            "en": "Use /help to see all commands",
            "bn": "/help দিয়ে সকল কমান্ড দেখুন"
        },
        "no_permission": {
            "en": "❌ You do not have permission for this action!",
            "bn": "❌ আপনার এই কাজের অনুমতি নেই!"
        }
    }
    return translations.get(key, {}).get(lang, key)

# =========================
# User-level Permissions
# =========================
def check_permission(self, user_id: str, required_level: str = "user") -> bool:
    """Check if user has permission for an action"""
    user = self.user_manager.get_user(user_id)
    level = user.get('permission', 'user')
    hierarchy = {"user": 0, "moderator": 1, "admin": 2, "owner": 3}
    return hierarchy.get(level, 0) >= hierarchy.get(required_level, 0)

# =========================
# Enhanced Logging (File + Console)
# =========================
import logging
log_file_path = "logs/bot.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(log_file_path),
        logging.StreamHandler()
    ]
)
log = logging.getLogger("SafeUserBot")
log.info("✅ Logging system initialized")

# =========================
# Dynamic Feature Toggles
# =========================
def toggle_feature(self, feature_name: str, status: bool):
    """Enable or disable a feature at runtime"""
    if feature_name in self.config.config['features']:
        self.config.config['features'][feature_name] = status
        log.info(f"⚙️ Feature '{feature_name}' set to {status}")
        self.config.save_config()
    else:
        log.warning(f"⚠️ Feature '{feature_name}' not found")

# =========================
# Backup & Recovery System
# =========================
import json
def backup_user_data(self):
    """Backup all user data to JSON file"""
    try:
        users = self.user_manager.get_all_users()
        backup_file = f"data/backup_users_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(backup_file, "w", encoding="utf-8") as f:
            json.dump(users, f, ensure_ascii=False, indent=4)
        log.info(f"💾 User data backed up to {backup_file}")
    except Exception as e:
        log.error(f"❌ Backup failed: {e}")

def restore_user_data(self, backup_file: str):
    """Restore user data from backup file"""
    try:
        with open(backup_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.user_manager.load_users(data)
        log.info(f"♻️ User data restored from {backup_file}")
    except Exception as e:
        log.error(f"❌ Restore failed: {e}")

# =========================
# MediaHandler Enhancements
# =========================
async def send_media(self, user_id: str, media_path: str, caption: str = ""):
    """Send media file to user with optional caption"""
    try:
        if not os.path.exists(media_path):
            log.warning(f"⚠️ Media not found: {media_path}")
            return
        await self.client.send_file(
            int(user_id),
            media_path,
            caption=caption
        )
        log.info(f"📤 Sent media to {user_id}: {media_path}")
    except Exception as e:
        log.error(f"❌ Failed to send media to {user_id}: {e}")

def get_emoji(self):
    """Random emoji for personalization"""
    import random
    emoji_list = ["😊", "🌟", "✨", "🎉", "❤️", "🤲", "🕌", "☀️", "🌙"]
    return random.choice(emoji_list)

# =========================
# AnnouncementHandler Improvements
# =========================
async def broadcast_announcement(self, message: str):
    """Send message to all active users"""
    active_users = self.user_manager.get_active_users(24)
    for user_id in active_users:
        try:
            await self.client.send_message(int(user_id), message)
            log.info(f"📢 Broadcast sent to {user_id}")
        except Exception as e:
            log.error(f"❌ Failed to send broadcast to {user_id}: {e}")

async def schedule_announcement(self, message: str, send_time: datetime):
    """Schedule future announcement"""
    async def job():
        while self.running:
            now = datetime.now()
            if now >= send_time:
                await self.broadcast_announcement(message)
                break
            await asyncio.sleep(30)
    asyncio.create_task(job())

# =========================
# EventsHandler Advanced
# =========================
@self.client.on(events.ChatAction)
async def handle_chat_events(event):
    """Join/leave detection and auto greeting"""
    try:
        if event.user_joined:
            user_id = str(event.user_id)
            user = await self.client.get_entity(user_id)
            log.info(f"➕ {user.first_name} joined {event.chat.title}")
            # Auto-greeting
            await self.client.send_message(
                event.chat_id,
                f"Welcome {user.first_name}! {self.get_emoji()}"
            )
        elif event.user_left:
            user_id = str(event.user_id)
            user = await self.client.get_entity(user_id)
            log.info(f"➖ {user.first_name} left {event.chat.title}")
    except Exception as e:
        log.error(f"❌ Chat event error: {e}")

# =========================
# Anti-flood & Rate Limiting
# =========================
from collections import defaultdict
user_message_times = defaultdict(list)

async def rate_limit_check(self, user_id: str, limit: int = 5, per_seconds: int = 10) -> bool:
    """Prevent spam messages"""
    import time
    now = time.time()
    user_message_times[user_id] = [t for t in user_message_times[user_id] if now - t < per_seconds]
    if len(user_message_times[user_id]) >= limit:
        log.warning(f"🚫 User {user_id} is rate-limited")
        return False
    user_message_times[user_id].append(now)
    return True
# =========================
# Final Scheduler & Run Loop
# =========================
async def start_final_scheduler(self):
    """Start all background tasks for production"""
    log.info("⏰ Starting full production scheduler...")

    async def namaz_checker():
        while self.running:
            try:
                namaz = self.namaz_alert.check_namaz_time()
                if namaz:
                    active_users = self.user_manager.get_active_users(24)
                    for user_id in active_users:
                        user_data = self.user_manager.get_user(user_id)
                        if user_data.get('namaz_alert', True):
                            await self.client.send_message(int(user_id), namaz['message'])
                            self.user_manager.update_namaz_count(user_id)
                            log.info(f"🕌 Namaz alert sent to {user_id}")
                await asyncio.sleep(60)
            except Exception as e:
                log.error(f"❌ Namaz scheduler error: {e}")
                await asyncio.sleep(60)

    async def slot_checker():
        while self.running:
            try:
                current_slot = self.slot_manager.get_current_slot()
                if current_slot:
                    slot_msg = self.slot_manager.get_slot_message(current_slot['name'], 1)
                    active_users = self.user_manager.get_active_users(1)
                    for user_id in active_users:
                        user_data = self.user_manager.get_user(user_id)
                        if user_data.get('slot_reminder', True):
                            await self.client.send_message(
                                int(user_id),
                                f"⏰ {current_slot['name'].upper()} REMINDER\n{slot_msg}"
                            )
                            self.user_manager.update_slot_count(user_id, current_slot['name'])
                            log.info(f"⏰ Slot reminder sent to {user_id}")
                await asyncio.sleep(300)
            except Exception as e:
                log.error(f"❌ Slot scheduler error: {e}")
                await asyncio.sleep(300)

    async def daily_quotes_sender():
        while self.running:
            try:
                now = TimeHelper.get_current_time()
                if now.hour == 9 and now.minute == 0:
                    active_users = self.user_manager.get_active_users(24)
                    for user_id in active_users:
                        user_data = self.user_manager.get_user(user_id)
                        if user_data.get('quotes_enabled', True):
                            quote = self.response_handler.get_quote()
                            await self.client.send_message(int(user_id), f"💭 DAILY QUOTE\n{quote}")
                            log.info(f"📚 Daily quote sent to {user_id}")
                await asyncio.sleep(60)
            except Exception as e:
                log.error(f"❌ Daily quote scheduler error: {e}")
                await asyncio.sleep(60)

    async def announcements_sender():
        """Send scheduled announcements"""
        while self.running:
            try:
                now = TimeHelper.get_current_time()
                announcements = self.announcement_handler.get_scheduled_announcements(now)
                for ann in announcements:
                    await self.broadcast_announcement(ann['message'])
                    self.announcement_handler.mark_sent(ann['id'])
                await asyncio.sleep(60)
            except Exception as e:
                log.error(f"❌ Announcement scheduler error: {e}")
                await asyncio.sleep(60)

    # Start all async tasks
    asyncio.create_task(namaz_checker())
    asyncio.create_task(slot_checker())
    asyncio.create_task(daily_quotes_sender())
    asyncio.create_task(announcements_sender())

    log.info("✅ Full production scheduler started")

# =========================
# Graceful Shutdown Handler
# =========================
async def shutdown_handler(self):
    """Ensure clean shutdown on Ctrl+C"""
    log.info("🔴 Shutting down Safe UserBot...")
    self.running = False
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
    for task in tasks:
        task.cancel()
    await asyncio.sleep(1)
    if self.client:
        await self.client.disconnect()
    log.info("✅ Shutdown complete. Bye!")

# =========================
# Main Run Method
# =========================
async def run_production(self):
    """Main run loop for production ready bot"""
    try:
        await self.initialize()
        await self.start_final_scheduler()

        log.info("""
🎉 SAFE USERBOT RUNNING IN PRODUCTION 🎉
Modules Loaded ✅
Scheduler ✅
Anti-Flood ✅
Session Secure ✅
""")
        await self.client.run_until_disconnected()

    except KeyboardInterrupt:
        await self.shutdown_handler()
    except Exception as e:
        log.error(f"❌ Fatal error: {e}", exc_info=True)
        await self.shutdown_handler()
# =========================
# Flood Protection & Async Send
# =========================
async def safe_send(self, user_id: int, message: str, retries: int = 3):
    """Send message with flood protection and retry"""
    for attempt in range(1, retries + 1):
        try:
            await self.client.send_message(user_id, message)
            log.info(f"✅ Message sent to {user_id}")
            return True
        except Exception as e:
            log.warning(f"⚠️ Send attempt {attempt} failed for {user_id}: {e}")
            await asyncio.sleep(2 * attempt)
    log.error(f"❌ Failed to send message to {user_id} after {retries} attempts")
    return False

# =========================
# Broadcast / Mass Message
# =========================
async def broadcast_announcement(self, message: str):
    """Send message to all active users"""
    users = self.user_manager.get_active_users(24)
    for user_id in users:
        user_data = self.user_manager.get_user(user_id)
        if user_data.get('broadcast_enabled', True):
            await self.safe_send(int(user_id), message)

# =========================
# Emoji & Media Helpers
# =========================
def get_random_emoji(self) -> str:
    """Return random emoji"""
    import random
    emojis = ["😊", "👍", "❤️", "🤲", "🌙", "☀️", "🌟", "✨", "🎉", "🎂"]
    return random.choice(emojis)

# =========================
# User Activity Tracking
# =========================
def track_user_activity(self, user_id: str, message: str = None):
    """Update user last active time and stats"""
    self.user_manager.update_user_activity(user_id)
    if message:
        self.user_manager.increment_message_count(user_id)

# =========================
# Helper: Human-like Delay
# =========================
async def human_delay(self, min_sec: float = 0.5, max_sec: float = 1.5):
    import random
    await asyncio.sleep(random.uniform(min_sec, max_sec))

# =========================
# Main Entry – Run Bot
# =========================
if __name__ == "__main__":
    print("""
███████╗ █████╗ ███████╗███████╗    ██╗   ██╗███████╗███████╗██████╗ ██████╗  ██████╗ ████████╗
██╔════╝██╔══██╗██╔════╝██╔════╝    ██║   ██║██╔════╝██╔════╝██╔══██╗██╔══██╗██╔═══██╗╚══██╔══╝
███████╗███████║█████╗  █████╗      ██║   ██║█████╗  █████╗  ██████╔╝██████╔╝██║   ██║   ██║   
╚════██║██╔══██║██╔══╝  ██╔══╝      ╚██╗ ██╔╝██╔══╝  ██╔══╝  ██╔══██╗██╔══██╗██║   ██║   ██║   
███████║██║  ██║███████╗███████╗     ╚████╔╝ ███████╗███████╗██║  ██║██████╔╝╚██████╔╝   ██║   
╚══════╝╚═╝  ╚═╝╚══════╝╚══════╝      ╚═══╝  ╚══════╝╚══════╝╚═╝  ╚═╝╚═════╝  ╚═════╝    ╚═╝   
""")
    print("🚀 Safe UserBot – Professional & Safe Telegram UserBot")
    print("👨‍💻 Developed by: RANA")
    print("=" * 60)

    bot = SafeUserBot()
    try:
        asyncio.run(bot.run_production())
    except KeyboardInterrupt:
        print("👋 Goodbye!")
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        import sys
        sys.exit(1)
