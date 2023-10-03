from aiogram import Bot, Dispatcher

from assets.config import TOKEN
from handlers import commands

from handlers.employ import view_vacancies
from handlers.employer import create_vacancy, edit_vacancy, error_processing

from aiogram.fsm.storage.redis import RedisStorage, Redis

from methods.sqlite.processes_db import close_db
from methods.redis.processes_redis import close_redis

import logging
import asyncio


async def start():
    redis_fsm = Redis(host='localhost')
    storage = RedisStorage(redis=redis_fsm)

    bot = Bot(token=TOKEN, parse_mode="HTML")
    dp = Dispatcher(storadge=storage)

    logging.basicConfig(level=logging.INFO)

    dp.include_router(commands.router)
    dp.include_router(view_vacancies.router)
    dp.include_router(edit_vacancy.router)
    dp.include_router(create_vacancy.router)
    dp.include_router(error_processing.router)

    dp.shutdown.register(close_db)
    dp.shutdown.register(close_redis)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(start())


