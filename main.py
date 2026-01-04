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
from datetime import datetime
from telethon import TelegramClient, events

# =========================
# Custom modules
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
# SafeUserBot Class
# =========================
class SafeUserBot:
    def __init__(self):
        log.info("🚀 Initializing Safe UserBot...")
        # Config
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
        # Telegram Client
        self.api_id, self.api_hash = self.config.get_telegram_creds()
        self.session_file = "sessions/main_account.session"
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
        async def handle_message(event):
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
            # Placeholder for chat action events
            pass

        @self.client.on(events.MessageEdited)
        async def handle_edited_message(event):
            # Placeholder for edited message events
            pass

        log.info("✅ Event handlers registered")

    # =========================
    # Process Incoming Message
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
        if any(k in text for k in ["slot", "reminder", "schedule"]):
            current_slot = self.slot_manager.get_current_slot()
            if current_slot:
                slot_msg = self.slot_manager.get_slot_message(current_slot["name"], 1)
                return f"Current Slot: **{current_slot['name']}**\n{slot_msg}"
            return "No active slot at the moment."
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
        first_name = user.get("name", "User")
        return f"""
{emoji} **Welcome YOUR CRUSH ⟵o_0** {emoji}

🤖 **Bot Name:** {self.bot_info.get('name', 'YOUR CRUSH ⟵o_0')}
👤 **Your ID:** {user_id}
🌚 **Your Name:** {first_name}
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
• Skills:
  - Video Editing
  - Photo Editing
  - Mobile Technology
  - Online Operations
  - Cyber Security (Learning)

📞 **CONTACT DETAILS:**
• Email: ranaeditz333@gmail.com
• Telegram Bot: @black_lovers1_bot
• Telegram Profile: @rana_editz_00
• Support Channel: https://t.me/master_account_remover_channel
• Phone: 01847634486
"""

# =========================
# Bot Info
# =========================
    def get_bot_info(self) -> str:
        total_users = len(self.user_manager.get_all_users())
        active_users = len(self.user_manager.get_active_users(24))
        cfg = self.config.config["features"]
        return f"""
✨ **SAFE USERBOT INFORMATION**

📊 **STATISTICS:**
• Total Users: {total_users}
• Active Users (24h): {active_users}
• Version: {self.bot_info.get('version', '1.0.0')}

⚙️ **FEATURES:**
• Auto Reply: {'✅' if cfg['auto_reply'] else '❌'}
• Namaz Alerts: {'✅' if cfg['namaz_alert'] else '❌'}
• Slot Reminders: {'✅' if cfg['slot_reminders'] else '❌'}
• Quotes: {'✅' if cfg['quotes_enabled'] else '❌'}
• Duas: {'✅' if cfg['duas_enabled'] else '❌'}
"""

# =========================
# User Stats
# =========================
    def format_user_stats(self, stats: dict, user_id: str) -> str:
        user = self.user_manager.get_user(user_id)
        first_name = user.get("name", "User")
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
• `quote` - Get Islamic quote

⏰ **REMINDERS:**
• `slot` - Current time slot
• `my stats` - Your statistics

ℹ️ **INFORMATION:**
• `bot info` - Bot information
• `developer` - Developer info
• `features` - Available features
"""

# =========================
# Scheduler
# =========================
    async def start_scheduler(self):
        log.info("⏰ Starting scheduler...")

        async def check_namaz():
            while self.running:
                try:
                    alert = self.namaz_alert.check_namaz_time()
                    if alert:
                        log.info(f"🕌 Namaz alert: {alert['name']}")
                        users = self.user_manager.get_active_users(24)
                        for uid, udata in users.items():
                            if udata.get("namaz_alert", True):
                                try:
                                    await self.client.send_message(int(uid), alert["message"])
                                    self.user_manager.update_namaz_count(uid)
                                    log.info(f"Sent namaz alert to {uid}")
                                except Exception as e:
                                    log.error(f"Failed to send to {uid}: {e}")
                    await asyncio.sleep(60)
                except Exception as e:
                    log.error(f"Scheduler error (namaz): {e}")
                    await asyncio.sleep(60)

        async def check_slots():
            while self.running:
                try:
                    slot = self.slot_manager.get_current_slot()
                    if slot:
                        msg = self.slot_manager.get_slot_message(slot["name"], 1)
                        users = self.user_manager.get_active_users(1)
                        for uid, udata in users.items():
                            if udata.get("slot_reminder", True):
                                try:
                                    await self.client.send_message(int(uid), f"⏰ **{slot['name'].upper()} REMINDER**\n{msg}")
                                    self.user_manager.update_slot_count(uid, slot["name"])
                                    log.info(f"Sent slot reminder to {uid}")
                                except:
                                    pass
                    await asyncio.sleep(300)
                except Exception as e:
                    log.error(f"Scheduler error (slot): {e}")
                    await asyncio.sleep(300)

        async def daily_quotes():
            while self.running:
                try:
                    now = TimeHelper.get_current_time()
                    if now.hour == 9 and now.minute == 0:
                        users = self.user_manager.get_active_users(24)
                        for uid, udata in users.items():
                            if udata.get("quotes_enabled", True):
                                try:
                                    quote = self.response_handler.get_quote()
                                    await self.client.send_message(int(uid), f"💭 **DAILY QUOTE**\n\n{quote}\n\nHave a great day! 😊")
                                    log.info(f"Sent daily quote to {uid}")
                                except:
                                    pass
                    await asyncio.sleep(60)
                except Exception as e:
                    log.error(f"Scheduler error (quotes): {e}")
                    await asyncio.sleep(60)

        asyncio.create_task(check_namaz())
        asyncio.create_task(check_slots())
        asyncio.create_task(daily_quotes())
        log.info("✅ Scheduler started successfully")

# =========================
# Run Bot
# =========================
    async def run(self):
        try:
            await self.initialize()
            log.info("🎉 **MAR PD IS NOW RUNNING!** 🎉")
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

# =========================
# Main Entry
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
    print("📧 Contact: ranaeditz333@gmail.com")
    print("=" * 60)
    bot = SafeUserBot()
    try:
        asyncio.run(bot.run())
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
