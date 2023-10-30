from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage, Redis

from config import config

from handlers import commands, error_processing
from handlers import other_state
from handlers.main_window import main_page
from handlers.employ import view_vacancies
from handlers.employer import create_vacancy, vacancy_management
from handlers.admin import sender

from classes.sql_conn import sql_connection
from classes import redis_commands

from middlewares.userdatamiddleware import UserMiddleware
from middlewares.antispammiddleware import AntiSpamMiddleware

import logging
import asyncio


async def start():

    redis_fsm = Redis(host='localhost')
    storage = RedisStorage(redis=redis_fsm)

    bot = Bot(config.bot.token, parse_mode="HTML")
    dp = Dispatcher(storadge=storage)

    logging.basicConfig(level=logging.INFO)

    dp.message.outer_middleware.register(AntiSpamMiddleware())

    dp.message.middleware.register(UserMiddleware())
    dp.callback_query.middleware.register(UserMiddleware())

    dp.include_router(commands.router)
    dp.include_router(main_page.router)
    dp.include_router(view_vacancies.router)
    dp.include_router(vacancy_management.router)
    dp.include_router(create_vacancy.router)
    dp.include_router(sender.router)
    dp.include_router(other_state.router)
    dp.include_router(error_processing.router)

    dp.shutdown.register(sql_connection.close_conn)
    dp.shutdown.register(redis_commands.close_conn)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(start())
