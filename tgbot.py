from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage, Redis

from assets.config import TOKEN

from handlers import commands, error_processing
from handlers import commandsotherstate
from handlers.main_window import main_page
from handlers.employ import view_vacancies
from handlers.employer import create_vacancy, edit_vacancy, basic, edit_my_vacancy

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

    dp.message.outer_middleware.register(AntiSpamMiddleware())

    dp.message.middleware.register(UserMiddleware())
    dp.callback_query.middleware.register(UserMiddleware())

    dp.include_router(commands.router)
    dp.include_router(commandsotherstate.router)
    dp.include_router(edit_my_vacancy.router)
    dp.include_router(main_page.router)
    dp.include_router(view_vacancies.router)
    dp.include_router(edit_vacancy.router)
    dp.include_router(create_vacancy.router)
    dp.include_router(basic.router)
    dp.include_router(error_processing.router)

    dp.shutdown.register(sql_connection.close_conn)
    dp.shutdown.register(redis_commands.close_conn)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(start())
