from aiogram import Bot, Dispatcher

from assets.config import TOKEN
from handlers import callback_employ, commands, create_vacancy

import logging
import asyncio


async def start():

    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    logging.basicConfig(level=logging.INFO)

    dp.include_router(commands.router)
    dp.include_router(callback_employ.router)
    dp.include_router(create_vacancy.router)


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