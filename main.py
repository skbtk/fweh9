import logging
from pyrogram import Client
from info import API_ID, API_HASH, BOT_TOKEN
from commands import register_handlers

logging.basicConfig(level=logging.INFO)

app = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

def main():
    register_handlers(app)
    logging.info("Bot started.")
    app.run()

if __name__ == "__main__":
    main()
