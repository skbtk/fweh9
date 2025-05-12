from pyrogram import Client, filters
from pyrogram.types import Message
from info import OWNER_ID
from script import START_TEXT, STATUS_TEXT
from database import get_channels

def register_handlers(app: Client):

    @app.on_message(filters.command("start") & filters.private)
    async def start(_, message: Message):
        await message.reply_text(START_TEXT)

    @app.on_message(filters.command("status") & filters.user(OWNER_ID))
    async def status(_, message: Message):
        channels = await get_channels()
        await message.reply_text(STATUS_TEXT.format(len(channels)))

    @app.on_message(filters.command("setchannel") & filters.user(OWNER_ID))
    async def set_channel(_, message: Message):
        if len(message.command) < 2:
            return await message.reply_text("Usage: /setchannel <chat_id>")
        chat_id = message.command[1]
        await get_channels(add=chat_id)
        await message.reply_text("Channel added successfully.")
