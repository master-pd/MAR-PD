import asyncio
from telethon import events, Button
from utils.admin_checker import is_admin
from utils.reminder_store import can_send, clear

REMINDER_TEXT = (
    "🔐 **Admin Permission Required | এডমিন পারমিশন প্রয়োজন**\n\n"

    "🇧🇩 **বাংলা:**\n"
    "এই বটটি গ্রুপের সম্পূর্ণ সিকিউরিটি ও অটোমেশন চালু করার জন্য "
    "**এডমিন পারমিশন** প্রয়োজন।\n\n"
    "দয়া করে নিচের যেকোনো একটি পদ্ধতিতে বটটিকে এডমিন করুন:\n"
    "• Manually admin দিন\n"
    "• অথবা Admin Invite Link তৈরি করে পাঠান\n\n"

    "🇺🇸 **English:**\n"
    "To enable full security and automation features, "
    "this bot requires **Admin permission**.\n\n"
    "Please do one of the following:\n"
    "• Add the bot as an admin manually\n"
    "• Or create an Admin Invite Link and send it here\n\n"

    "⏱️ _Reminder policy:_\n"
    "• Sent after 12 hours\n"
    "• Max 2 times per day\n"
    "• Automatically stops once admin access is granted"
)

BUTTONS = [
    [
        Button.url("👑 Bot Owner", "https://t.me/rana_editz_00"),
        Button.url("📢 Channel", "https://t.me/master_editz_team")
    ],
    [
        Button.url("🆘 Support", "https://t.me/master_team_00")
    ]
]

def setup(client):

    @client.on(events.ChatAction())
    async def admin_reminder_handler(event):

        if not event.is_group:
            return

        me = await client.get_me()

        # Already admin → clear & stop
        if await is_admin(client, event.chat_id, me.id):
            clear(event.chat_id)
            return

        # Wait 12 hours
        await asyncio.sleep(43200)

        # Check again
        if await is_admin(client, event.chat_id, me.id):
            clear(event.chat_id)
            return

        # Daily limit check (max 2)
        if not can_send(event.chat_id):
            return

        try:
            await client.send_message(
                event.chat_id,
                REMINDER_TEXT,
                buttons=BUTTONS,
                link_preview=False
            )
        except:
            pass
