from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage, Redis

from assets.config import TOKEN

from handlers import commands
from handlers.employ import view_vacancies
from handlers.employer import create_vacancy, edit_vacancy, error_processing

from classes.sql_conn import sql_connection
from classes import redis_commands

from middlewares.userdatamiddleware import UserMiddleware
from middlewares.antispammiddleware import AntiSpamMiddleware
import logging
import asyncio


async def start():
    redis_fsm = Redis(host='localhost')
    storage = RedisStorage(redis=redis_fsm)

    bot = Bot(token=TOKEN, parse_mode="HTML")
    dp = Dispatcher(storadge=storage)

    logging.basicConfig(level=logging.INFO)

    dp.message.middleware.register(UserMiddleware())
    dp.message.middleware.register(AntiSpamMiddleware())

    dp.callback_query.middleware.register(UserMiddleware())

    dp.include_router(commands.router)
    dp.include_router(view_vacancies.router)
    dp.include_router(edit_vacancy.router)
    dp.include_router(create_vacancy.router)
    dp.include_router(error_processing.router)

    dp.shutdown.register(sql_connection.close_conn)
    dp.shutdown.register(redis_commands.close_conn)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(start())
