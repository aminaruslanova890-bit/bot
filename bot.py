import asyncio
import logging
import os
import sys
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher
from handlers import router

# Load environment variables
load_dotenv()

# Logger setup
logging.basicConfig(level=logging.INFO)

async def main():
    bot_token = os.getenv("BOT_TOKEN")
    if not bot_token or bot_token == "your_bot_token_here":
        logging.error("❌ BOT_TOKEN is not set in .env file!")
        return

    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(token=bot_token)
    dp = Dispatcher()
    
    dp.include_router(router)
    
    # Drop pending updates to avoid conflict loop on restart if many are queued
    await bot.delete_webhook(drop_pending_updates=True)

    logging.info("🚀 Bot is starting...")
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logging.error(f"Error: {e}")
    finally:
        await bot.session.close()

if __name__ == "__main__":
    try:
        if sys.platform == "win32":
             asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot stopped!")
