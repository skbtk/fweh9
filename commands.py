from pyrogram import filters
from pyrogram.types import Message
from script import extract_links
from info import UPLOAD_CHANNEL
from script import upload_links_to_channel

def register_handlers(app):

    @app.on_message(filters.command("start") & filters.private)
    async def start_handler(client, message: Message):
        await message.reply("👋 Hello! I'm alive and ready to scrape download links!")

    @app.on_message(filters.command("status") & filters.private)
    async def status_handler(client, message: Message):
        await message.reply(f"📢 Uploading to channel: `{UPLOAD_CHANNEL}`")

    @app.on_message(filters.command("scrape_filmyfly") & filters.private)
    async def scrape_filmyfly_handler(client, message: Message):
        if len(message.command) < 2:
            return await message.reply("❗ Send a FilmyFly movie page URL.\n\n`/scrape_filmyfly <url>`")
        
        url = message.command[1]
        await message.reply("🔍 Scraping links, please wait...")
        links = await extract_links(url)

        if not links:
            return await message.reply("❌ No links found.")

        await upload_links_to_channel(app, UPLOAD_CHANNEL, links)
        await message.reply(f"✅ Uploaded {len(links)} links to the channel.")

    @app.on_message(filters.command("scrape_tamilblasters") & filters.private)
    async def scrape_tamilblasters_handler(client, message: Message):
        await message.reply("🔄 TamilBlasters scraping coming soon or under development.")
