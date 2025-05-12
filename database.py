from pymongo import MongoClient
from info import MONGODB_URL

client = MongoClient(MONGODB_URL)
db = client.bot_db
channels_col = db.channels

def add_channel(chat_id):
    channels_col.update_one({"chat_id": chat_id}, {"$set": {"chat_id": chat_id}}, upsert=True)

def remove_channel(chat_id):
    channels_col.delete_one({"chat_id": chat_id})

def get_channels():
    return [x["chat_id"] for x in channels_col.find()]
