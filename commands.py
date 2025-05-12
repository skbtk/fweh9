from pyrogram import filters
from pyrogram.types import Message
from info import OWNER_ID
from database import add_channel, remove_channel, get_channels
from script import upload_links
from scraper_filmyfly import extract_links as extract_filmyfly
from scraper_tamilblasters import extract_links as extract_tamilblasters

def register_handlers(app):

    @app.on_message(filters.command("start"))
    async def start(_, message: Message):
        await message.reply("🤖 Bot is online!")

    @app.on_message(filters.command("setchannel") & filters.user(OWNER_ID))
    async def set_channel(_, message: Message):
        if len(message.command) < 2:
            return await message.reply("⚠️ Usage: /setchannel <chat_id>")
        try:
            chat_id = int(message.command[1])
            add_channel(chat_id)
            await message.reply("✅ Channel added.")
        except:
            await message.reply("❌ Invalid chat_id")

    @app.on_message(filters.command("delchannel") & filters.user(OWNER_ID))
    async def del_channel(_, message: Message):
        if len(message.command) < 2:
            return await message.reply("⚠️ Usage: /delchannel <chat_id>")
        try:
            chat_id = int(message.command[1])
            remove_channel(chat_id)
            await message.reply("✅ Channel removed.")
        except:
            await message.reply("❌ Invalid chat_id")

    @app.on_message(filters.command("status") & filters.user(OWNER_ID))
    async def status(_, message: Message):
        channels = get_channels()
        await message.reply(f"📡 Channels:\n" + "\n".join([str(c) for c in channels]) if channels else "No channels set.")

    @app.on_message(filters.command("scrape_filmyfly") & filters.user(OWNER_ID))
    async def scrape_ff(_, message: Message):
        if len(message.command) < 2:
            return await message.reply("⚠️ Usage: /scrape_filmyfly <url>")
        url = message.command[1]
        links = extract_filmyfly(url)
        if not links:
            return await message.reply("❌ No links found.")
        await upload_links(app, links)

    @app.on_message(filters.command("scrape_tamilblasters") & filters.user(OWNER_ID))
    async def scrape_tb(_, message: Message):
        links = extract_tamilblasters()
        if not links:
            return await message.reply("❌ No links found.")
        await upload_links(app, links)
