import asyncio
import logging
from aiogram import Bot, Dispatcher
import routers

from config_reader import config


async def main():
    dp = Dispatcher()
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=config.bot_token.get_secret_value())
    # регисятрация роутеров
    dp.include_routers(routers.menu_router)
    dp.include_routers(routers.profile_router)
    dp.include_routers(routers.subjects_router)
    dp.include_routers(routers.subject_router)
    dp.include_routers(routers.lecture_router)
    dp.include_routers(routers.start_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
