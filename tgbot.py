
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, Text
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from handlers import commands, callback_employ
from keyboard import inline_buttons
from assets import texts
from vacancy import VacanciesEmploy
from queue_vacancy import QueueVacancy
from assets.config import TOKEN

import logging
import asyncio

bot = Bot(token=TOKEN)
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)


@dp.message(Command(commands=['start']))
async def start_command(message: types.Message):
    return await commands.start_command(message)


@dp.message(Command(commands=['choice']))
async def choice_command(message: types.Message):
    return await commands.choice_command(message)


@dp.callback_query(Text("employer"))
async def callback_employ_vacancies(callback: types.CallbackQuery):
    return await callback_employ.callback_employ_vacancies(callback)


@dp.callback_query(Text("employ"))
async def callback_employ_vacancies(callback: types.CallbackQuery):
    return await callback_employ.callback_employ_vacancies(callback)


@dp.callback_query(Text("next"))
async def callback_next_vacancy(callback: types.CallbackQuery):
    return await callback_employ.callback_next_vacancy(callback)


@dp.callback_query(Text("more"))
async def callback_more_vacancy(callback: types.CallbackQuery):
    return await callback_employ.callback_more_vacancy(callback)


@dp.callback_query(Text("less"))
async def callback_less_vacancy(callback: types.CallbackQuery):
    return await callback_employ.callback_less_vacancy(callback)


@dp.callback_query(Text("like"))
async def callback_like_vacancy(callback: types.CallbackQuery):
    return await callback_employ.callback_like_vacancy(callback)


if __name__ == "__main__":
    dp.run_polling(bot)




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