import logging
import threading
from flask import Flask
from pyrogram import Client
from info import API_ID, API_HASH, BOT_TOKEN
from commands import register_handlers

# Logging
logging.basicConfig(level=logging.INFO)

# Create Flask app
flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "Bot is running", 200

# Run Flask in a thread
def run_flask():
    flask_app.run(host="0.0.0.0", port=8000)

# Pyrogram Client
app = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

def main():
    register_handlers(app)  # Even if it's empty
    logging.info("Bot started.")
    app.run()

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    main()
