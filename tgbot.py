from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, Text
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage
from aiogram import F

from handlers import commands, callback_employ
from fsm.statesform import StapesForm as sf
from keyboard import inline_buttons
from assets import texts
from vacancy import VacanciesEmploy
from queue_vacancy import QueueVacancy
from assets.config import TOKEN
from handlers import create_vacancy
import aioredis

import logging
import asyncio


redis_fsm = aioredis.Redis(host='localhost', db=0)
redis_storadge = aioredis.Redis(host='localhost', db=1)

storadge = RedisStorage(redis=redis_fsm)


bot = Bot(token=TOKEN)
dp = Dispatcher(storadge=storadge)

logging.basicConfig(level=logging.INFO)


@dp.message(Command(commands=['start']))
async def start_command(message: types.Message):
    return await commands.start_command(message)


@dp.message(Command(commands=['choice']))
async def choice_command(message: types.Message):
    return await commands.choice_command(message)




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


####################


@dp.callback_query(Text("employer"))
async def sent_employer(callback: CallbackQuery, state: FSMContext):
    return await create_vacancy.sent_employer(callback, state)


@dp.message(F.text(), sf.fill_employer)
async def sent_job(message: Message, state: FSMContext):
    return await create_vacancy.sent_job(message, state)


@dp.message(F.text(), sf.fill_job)
async def sent_salary(message: Message, state: FSMContext):
    return await create_vacancy.sent_salary(message, state)


@dp.message(F.text(), sf.fill_salary)
async def sent_minage(message: Message, state: FSMContext):
    return await create_vacancy.sent_minage(message, state)


@dp.message(F.text(), sf.fill_minage)
async def sent_minexp(message: Message, state: FSMContext):
    return await create_vacancy.sent_minexp(message, state)


@dp.message(F.text(), sf.fill_minexp)
async def sent_date(message: Message, state: FSMContext):
    return await create_vacancy.sent_date(message, state)


@dp.message(F.text(), sf.fill_date)
async def sent_short_dsp(message: Message, state: FSMContext):
    return await create_vacancy.sent_short_dsp(message, state)


@dp.message(F.text(), sf.fill_short_dsp)
async def sent_long_dsp(message: Message, state: FSMContext):
    return await create_vacancy.sent_long_dsp(message, state)


@dp.message(F.text(), sf.fill_long_dsp)
async def save_vacancy(message: Message, state: FSMContext):
    return await create_vacancy.save_vacancy(message, state)













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