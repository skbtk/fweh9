import asyncio
from pyrogram import Client, idle
from aiohttp import web
import os
import logging

from info import API_ID, API_HASH, BOT_TOKEN
from commands import register_handlers

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Client("scraper_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
register_handlers(app)

async def handle(request):
    return web.Response(text="Bot is running")

async def run_web():
    app_web = web.Application()
    app_web.router.add_get("/", handle)
    runner = web.AppRunner(app_web)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 8000)
    await site.start()
    logger.info("Health check server started on port 8000.")

async def main():
    await run_web()
    await app.start()
    logger.info("Bot started.")
    await idle()
    await app.stop()
    logger.info("Bot stopped.")

if __name__ == "__main__":
    asyncio.run(main())
