import os
import logging
from motor.motor_asyncio import AsyncIOMotorClient

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load MongoDB URL from environment variable
MONGO_URL = os.getenv("MONGO_URL")

# Connect to MongoDB
client = AsyncIOMotorClient(MONGO_URL)
db = client["scraper"]
col = db["channels"]

async def get_channels():
    try:
        data = await col.find({}).to_list(length=None)
        return [i["chat_id"] for i in data]
    except Exception as e:
        logger.error(f"get_channels error: {e}")
        return []

async def set_channel(chat_id: int):
    try:
        exists = await col.find_one({"chat_id": chat_id})
        if not exists:
            await col.insert_one({"chat_id": chat_id})
            logger.info(f"Channel {chat_id} added to database.")
    except Exception as e:
        logger.error(f"set_channel error: {e}")

async def remove_channel(chat_id: int):
    try:
        await col.delete_one({"chat_id": chat_id})
        logger.info(f"Channel {chat_id} removed from database.")
    except Exception as e:
        logger.error(f"remove_channel error: {e}")

async def upload_links(links: list):
    try:
        channels = await get_channels()
        if not channels:
            logger.warning("No channels found to send links to.")
            return
        from pyrogram import Client  # Imported here to avoid circular import
        from info import API_ID, API_HASH, BOT_TOKEN
        app = Client("bot-uploader", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
        await app.start()
        for chat_id in channels:
            for link in links:
                try:
                    await app.send_message(chat_id, link)
                except Exception as e:
                    logger.error(f"Failed to send link to {chat_id}: {e}")
        await app.stop()
    except Exception as e:
        logger.error(f"upload_links error: {e}")
