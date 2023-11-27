from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage, Redis
from aiogram.utils.callback_answer import CallbackAnswerMiddleware

from config import load_config, Config

from handlers import commands, error_processing
from handlers.main_window import main_page
from handlers.user import view_vacancies
from handlers.user import basic
from handlers.employer import create_vacancy, vacancy_management
from handlers.admin import sender

from classes.sql_conn import sql_connection
from classes import redis_commands

from middlewares.userdatamiddleware import UserDataMiddleware
from middlewares.antispammiddleware import AntiSpamMiddleware

import logging
import asyncio


async def start():
    config: Config = load_config(None)

    redis_fsm = Redis(host='localhost')
    storage = RedisStorage(redis=redis_fsm)

    bot = Bot(config.bot.token, parse_mode="HTML")
    dp = Dispatcher(storadge=storage)

    logging.basicConfig(level=logging.INFO)

    dp.message.outer_middleware.register(AntiSpamMiddleware())

    dp.message.middleware.register(UserDataMiddleware())
    dp.callback_query.middleware.register(UserDataMiddleware())

    dp.callback_query.middleware.register(CallbackAnswerMiddleware())

    dp.include_router(commands.router)
    dp.include_router(main_page.router)
    dp.include_router(view_vacancies.router)
    dp.include_router(basic.router)
    dp.include_router(vacancy_management.router)
    dp.include_router(create_vacancy.router)
    dp.include_router(sender.router)
    dp.include_router(error_processing.router)

    dp.startup.register(redis_commands.load_verified_users)

    dp.shutdown.register(sql_connection.close_conn)
    dp.shutdown.register(redis_commands.close_conn)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(start())
