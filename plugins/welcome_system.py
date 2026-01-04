from telethon import events
from utils.image_maker import make_image

def setup(client):

    # 🔹 Bot added to group
    @client.on(events.ChatAction())
    async def on_bot_added(event):
        if not event.is_group or not event.user_added:
            return

        me = await client.get_me()
        if me.id not in event.action.users:
            return

        chat = await event.get_chat()
        full = await client.get_entity(event.chat_id)

        title = f"Welcome to {chat.title}"
        subtitle = f"Members: {chat.participants_count}"

        img = make_image(title, subtitle)

        text = (
            f"👋 **Welcome!**\n\n"
            f"🇧🇩 **বাংলা:**\n"
            f"এই গ্রুপে আমাকে যুক্ত করার জন্য ধন্যবাদ।\n\n"
            f"🇺🇸 **English:**\n"
            f"Thanks for adding me to this group.\n\n"
            f"📌 **Group:** {chat.title}\n"
            f"👥 **Members:** {chat.participants_count}"
        )

        await client.send_file(event.chat_id, img, caption=text)

    # 🔹 New member joined
    @client.on(events.ChatAction())
    async def on_user_join(event):
        if not event.user_joined or not event.is_group:
            return

        user = await event.get_user()
        name = user.first_name or "New Member"

        title = f"Welcome {name}"
        subtitle = "Enjoy your stay!"

        img = make_image(title, subtitle)

        text = (
            f"🎉 **Welcome {name}!**\n\n"
            f"🇧🇩 গ্রুপে আপনাকে স্বাগতম\n"
            f"🇺🇸 Welcome to the group\n"
        )

        await client.send_file(event.chat_id, img, caption=text)
