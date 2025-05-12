from motor.motor_asyncio import AsyncIOMotorClient
from info import MONGODB_URL

client = AsyncIOMotorClient(MONGODB_URL)
db = client.scraperbot
channel_collection = db.channels

async def get_channels(add=None):
    if add:
        await channel_collection.update_one({"chat_id": add}, {"$set": {"chat_id": add}}, upsert=True)
    return await channel_collection.distinct("chat_id")
