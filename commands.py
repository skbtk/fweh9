from pyrogram import filters
from pyrogram.types import Message
from script import extract_links
from database import (
    set_channel, get_channels, remove_channel, upload_links
)

def register_handlers(app):

    @app.on_message(filters.command("start") & filters.private)
    async def start_handler(client, message: Message):
        await message.reply("👋 Hello! I'm alive and ready to scrape download links!")

    @app.on_message(filters.command("status") & filters.private)
    async def status_handler(client, message: Message):
        channels = await get_channels()
        if not channels:
            await message.reply("❌ No channels set yet.")
        else:
            reply = "📢 Current set channels:\n"
            for ch in channels:
                reply += f"➤ `{ch}`\n"
            await message.reply(reply)

    @app.on_message(filters.command("scrape_filmyfly") & filters.private)
    async def scrape_filmyfly_handler(client, message: Message):
        if len(message.command) < 2:
            return await message.reply("❗ Send a FilmyFly movie page URL.\n\n`/scrape_filmyfly <url>`")
        
        url = message.command[1]
        await message.reply("🔍 Scraping links, please wait...")
        links = await extract_links(url)

        if not links:
            return await message.reply("❌ No links found.")

        await upload_links(links)
        await message.reply(f"✅ Uploaded {len(links)} links to the set channels.")

    @app.on_message(filters.command("scrape_tamilblasters") & filters.private)
    async def scrape_tamilblasters_handler(client, message: Message):
        await message.reply("🔄 TamilBlasters scraping coming soon or under development.")

    @app.on_message(filters.command("setchannel") & filters.private)
    async def setchannel_handler(client, message: Message):
        if len(message.command) < 2:
            return await message.reply("❗ Send a channel ID.\n\n`/setchannel <channel_id>`")
        channel_id = int(message.command[1])
        await set_channel(channel_id)
        await message.reply(f"✅ Channel `{channel_id}` added.")

    @app.on_message(filters.command("delchannel") & filters.private)
    async def delchannel_handler(client, message: Message):
        if len(message.command) < 2:
            return await message.reply("❗ Send a channel ID.\n\n`/delchannel <channel_id>`")
        channel_id = int(message.command[1])
        await remove_channel(channel_id)
        await message.reply(f"🗑️ Channel `{channel_id}` removed.")
