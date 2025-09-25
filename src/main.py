import asyncio

from aiogram import Bot, Dispatcher

from src.config import app_config
from src.bot.routers import router as main_router

async def main():
    bot = Bot(token=app_config.BOT.TOKEN)
    dp = Dispatcher()

    dp.include_router(main_router)

    try:
        print("Bot started...")
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
        print("Bot stopped.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nStopped by CTRL+C")