import os
import time
from datetime import datetime
from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from dotenv import load_dotenv
from scraper import TamilScraper

# Load environment variables
load_dotenv()

class Config:
    TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
    OWNER_ID = int(os.getenv('OWNER_ID'))
    MONGO_URI = os.getenv('MONGO_URI')
    SCRAPE_INTERVAL = int(os.getenv('SCRAPE_INTERVAL', 600))

class Database:
    def __init__(self):
        try:
            self.client = MongoClient(Config.MONGO_URI)
            self.db = self.client.tamil_scraper
            self.posted = self.db.posted
            self._ensure_indexes()
        except ConnectionFailure as e:
            print(f"MongoDB connection failed: {e}")
            raise

    def _ensure_indexes(self):
        self.posted.create_index("url", unique=True)
        self.posted.create_index("timestamp")

    def is_posted(self, url: str) -> bool:
        return bool(self.posted.find_one({"url": url}))

    def mark_posted(self, data: dict):
        self.posted.insert_one(data)

class TamilBot:
    def __init__(self):
        self.db = Database()
        self.scraper = TamilScraper()
        self.updater = Updater(token=Config.TELEGRAM_TOKEN, use_context=True)
        self._setup_handlers()

    def _setup_handlers(self):
        dispatcher = self.updater.dispatcher
        dispatcher.add_handler(CommandHandler('start', self._start))
        dispatcher.add_handler(CommandHandler('stats', self._stats))

    def _start(self, update: Update, context: CallbackContext):
        if update.effective_user.id != Config.OWNER_ID:
            return
        update.message.reply_text(
            "🎬 Tamil Movie Scraper Bot\n\n"
            f"Scraping every {Config.SCRAPE_INTERVAL//60} minutes\n"
            f"Total posted: {self.db.posted.count_documents({})}"
        )

    def _stats(self, update: Update, context: CallbackContext):
        if update.effective_user.id != Config.OWNER_ID:
            return
        stats = self.db.posted.aggregate([
            {"$group": {
                "_id": "$site",
                "count": {"$sum": 1},
                "latest": {"$max": "$timestamp"}
            }}
        ])
        message = "📊 Bot Statistics\n\n"
        for stat in stats:
            message += f"{stat['_id']}: {stat['count']} (Last: {stat['latest'].strftime('%Y-%m-%d %H:%M')})\n"
        update.message.reply_text(message)

    def _scrape_and_post(self, context: CallbackContext):
        for site_scraper in [self.scraper.scrape_tamilblasters, self.scraper.scrape_tamilmv]:
            try:
                for item in site_scraper():
                    if not self.db.is_posted(item['url']):
                        self._send_to_telegram(context, item)
                        self.db.mark_posted({
                            'site': item['site'],
                            'title': item['title'],
                            'url': item['url'],
                            'timestamp': datetime.now()
                        })
                        time.sleep(1)  # Rate limiting
            except Exception as e:
                print(f"Scraping error: {e}")

    def _send_to_telegram(self, context: CallbackContext, item: dict):
        try:
            message = f"<b>{item['title']}</b>\n\n"
            if 'magnets' in item:
                message += "🧲 <b>Magnet Links:</b>\n"
                message += "\n".join(f"<code>{m}</code>" for m in item['magnets'][:2]) + "\n\n"
            if 'downloads' in item:
                message += "📥 <b>Downloads:</b>\n"
                message += "\n".join(item['downloads'][:2]) + "\n\n"
            message += f"🔗 <a href='{item['url']}'>View on {item['site']}</a>"

            context.bot.send_message(
                chat_id=Config.OWNER_ID,
                text=message,
                parse_mode='HTML',
                disable_web_page_preview=True
            )
        except Exception as e:
            print(f"Failed to send message: {e}")

    def start(self):
        job_queue = self.updater.job_queue
        job_queue.run_repeating(
            self._scrape_and_post,
            interval=Config.SCRAPE_INTERVAL,
            first=10
        )
        print("Bot started...")
        self.updater.start_polling()
        self.updater.idle()

if __name__ == '__main__':
    bot = TamilBot()
    bot.start()
