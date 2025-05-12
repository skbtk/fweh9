import logging
from pyrogram import Client
from info import API_ID, API_HASH, BOT_TOKEN
from commands import register_handlers
from flask import Flask

logging.basicConfig(level=logging.INFO)

# Initialize the Flask app
flask_app = Flask(__name__)

# Define a simple health check endpoint
@flask_app.route("/health")
def health_check():
    return "OK", 200  # Respond with "OK" to pass health checks

# Initialize the Pyrogram bot
app = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

def main():
    register_handlers(app)
    logging.info("Bot started.")
    # Run the Flask app in the background
    flask_app.run(host="0.0.0.0", port=8000)  # Ensure it listens on port 8000
    app.run()

if __name__ == "__main__":
    main()
