"""
কমান্ড হ্যান্ডলার - Safe UserBot
"""

import re
from typing import Dict, List, Optional, Callable, Any
from telethon import events

class CommandHandler:
    def __init__(self, bot):
        self.bot = bot
        self.commands: Dict[str, Dict] = {}
        self.register_default_commands()
    
    def register_default_commands(self):
        """ডিফল্ট কমান্ড রেজিস্টার"""
        self.commands = {
            'start': {
                'handler': self.handle_start,
                'description': 'Start the bot',
                'usage': '/start',
                'admin_only': False
            },
            'help': {
                'handler': self.handle_help,
                'description': 'Show help message',
                'usage': '/help',
                'admin_only': False
            },
            'namaz': {
                'handler': self.handle_namaz,
                'description': 'Show prayer times',
                'usage': '/namaz',
                'admin_only': False
            },
            'quote': {
                'handler': self.handle_quote,
                'description': 'Get Islamic quote',
                'usage': '/quote',
                'admin_only': False
            },
            'dua': {
                'handler': self.handle_dua,
                'description': 'Get daily dua',
                'usage': '/dua',
                'admin_only': False
            },
            'slot': {
                'handler': self.handle_slot,
                'description': 'Current time slot',
                'usage': '/slot',
                'admin_only': False
            },
            'stats': {
                'handler': self.handle_stats,
                'description': 'Your statistics',
                'usage': '/stats',
                'admin_only': False
            },
            'settings': {
                'handler': self.handle_settings,
                'description': 'Bot settings',
                'usage': '/settings',
                'admin_only': False
            }
        }
    
    def register_command(self, command: str, handler: Callable, 
                        description: str = '', usage: str = '', 
                        admin_only: bool = False):
        """নতুন কমান্ড রেজিস্টার"""
        self.commands[command.lower()] = {
            'handler': handler,
            'description': description,
            'usage': usage or f'/{command}',
            'admin_only': admin_only
        }
    
    async def handle_message(self, event, message_text: str):
        """মেসেজ হ্যান্ডল"""
        # কমান্ড চেক
        if message_text.startswith('/'):
            command_parts = message_text[1:].split()
            command = command_parts[0].lower()
            args = command_parts[1:] if len(command_parts) > 1 else []
            
            if command in self.commands:
                cmd_info = self.commands[command]
                
                # অ্যাডমিন চেক
                if cmd_info['admin_only']:
                    from admin.admin_panel import AdminPanel
                    admin_panel = AdminPanel()
                    if not admin_panel.is_admin(event.sender_id):
                        await event.reply("❌ এই কমান্ড শুধুমাত্র অ্যাডমিনদের জন্য।")
                        return
                
                # কমান্ড হ্যান্ডল
                try:
                    await cmd_info['handler'](event, *args)
                except Exception as e:
                    await event.reply(f"❌ কমান্ড এক্সিকিউট করতে সমস্যা: {str(e)}")
            else:
                await event.reply("❌ অজানা কমান্ড। /help ব্যবহার করে দেখুন।")
    
    async def handle_start(self, event, *args):
        """স্টার্ট কমান্ড"""
        welcome_msg = self.bot.get_welcome_message(str(event.sender_id))
        await event.reply(welcome_msg)
    
    async def handle_help(self, event, *args):
        """হেল্প কমান্ড"""
        help_msg = self.bot.get_help_message()
        await event.reply(help_msg)
    
    async def handle_namaz(self, event, *args):
        """নামাজ কমান্ড"""
        namaz_times = self.bot.namaz_alert.get_all_namaz_times()
        await event.reply(namaz_times)
    
    async def handle_quote(self, event, *args):
        """কোট কমান্ড"""
        quote = self.bot.response_handler.get_quote()
        await event.reply(f"💭 **Islamic Quote:**\n\n{quote}")
    
    async def handle_dua(self, event, *args):
        """দোয়া কমান্ড"""
        dua = self.bot.response_handler.get_dua()
        await event.reply(f"🤲 **Daily Dua:**\n\n{dua}")
    
    async def handle_slot(self, event, *args):
        """স্লট কমান্ড"""
        current_slot = self.bot.slot_manager.get_current_slot()
        if current_slot:
            slot_msg = self.bot.slot_manager.get_slot_message(current_slot['name'], 1)
            response = f"⏰ **Current Slot:** {current_slot['name'].upper()}\n\n{slot_msg}"
        else:
            response = "No active slot at the moment."
        await event.reply(response)
    
    async def handle_stats(self, event, *args):
        """স্ট্যাটস কমান্ড"""
        stats = self.bot.user_manager.get_user_stats(str(event.sender_id))
        formatted_stats = self.bot.format_user_stats(stats, str(event.sender_id))
        await event.reply(formatted_stats)
    
    async def handle_settings(self, event, *args):
        """সেটিংস কমান্ড"""
        user = self.bot.user_manager.get_user(str(event.sender_id))
        
        settings_msg = f"""⚙️ **Your Settings:**

🔔 **Notifications:**
• Namaz Alerts: {'✅' if user.get('namaz_alert', True) else '❌'}
• Slot Reminders: {'✅' if user.get('slot_reminder', True) else '❌'}
• Daily Quotes: {'✅' if user.get('quotes_enabled', True) else '❌'}
• Daily Duas: {'✅' if user.get('duas_enabled', True) else '❌'}

🌐 **Preferences:**
• Language: {user.get('settings', {}).get('language', 'bn')}
• Timezone: {user.get('settings', {}).get('timezone', 'Asia/Dhaka')}

💡 **To change settings, contact admin.**
"""
        await event.reply(settings_msg)
    
    def get_commands_list(self, for_admin: bool = False) -> List[Dict]:
        """কমান্ড লিস্ট"""
        commands_list = []
        for cmd, info in self.commands.items():
            if not info['admin_only'] or for_admin:
                commands_list.append({
                    'command': cmd,
                    'description': info['description'],
                    'usage': info['usage']
                })
        return commands_list