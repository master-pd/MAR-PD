from telethon.tl.functions.channels import GetParticipantRequest
from telethon.tl.types import (
    ChannelParticipantAdmin,
    ChannelParticipantCreator
)

async def is_admin(client, chat_id, user_id):
    try:
        participant = await client(
            GetParticipantRequest(chat_id, user_id)
        )
        return isinstance(
            participant.participant,
            (ChannelParticipantAdmin, ChannelParticipantCreator)
        )
    except:
        return False
