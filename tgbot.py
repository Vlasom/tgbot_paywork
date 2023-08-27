from aiogram import Bot, Dispatcher

from assets.config import TOKEN

from handlers import commands
from handlers import view_vacancies
from handlers import create_vacancy, edit_vacancy, errors_processing

from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.chat_action import ChatActionMiddleware

from middleware.chat_action import CallbackQuerryChatActionMiddleware

import logging
import asyncio


async def start():
    storadge = MemoryStorage()

    bot = Bot(token=TOKEN)                          # parse_mode="MarkdownV2"
    dp = Dispatcher(storadge=storadge)

    logging.basicConfig(level=logging.INFO)

    dp.message.middleware.register(ChatActionMiddleware())
    dp.callback_query.middleware.register(CallbackQuerryChatActionMiddleware())
    dp.include_router(commands.router)
    dp.include_router(view_vacancies.router)
    dp.include_router(edit_vacancy.router)
    dp.include_router(create_vacancy.router)
    dp.include_router(errors_processing.router)


    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(start())

    #
    # row: str | list = get_db_row(count=1, rules='count_of_viewer >= 5')
    #
    # vacancy = VacancyEmploy(db_id=int(row['db_id']),
    #                         employer=row['employer'],
    #                         salary=row['salary'],
    #                         date=datetime(row['date']),
    #                         work_type=row['work_type'],
    #                         min_age=row['min_age'],
    #                         work_exp=row['work_exp'],
    #                         s_descr=row['s_descr'],
    #                         l_descr=row['l_descr'])
    #
    #
    # answer: list = vacancy.to_text()
