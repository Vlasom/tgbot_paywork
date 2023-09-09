from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from fsm.statesform import StapesForm as sf
from aiogram import Router
from assets import texts
from keyboards.inline_keyboards import *
from methods.sqlite.users import add_user
from methods import get_liked_vacancies, vacancy_to_text

import asyncio

__all__ = ["command_choice", "command_start", "command_create_vacancy"]

router = Router()

# добавить фильтры для роутера


@router.message(Command(commands=['start']))
async def command_start(message: Message):
    await message.reply(texts.welcome_text)
    await asyncio.sleep(0.3)
    await message.answer(text=texts.employ_or_employer, reply_markup=inkb_employ_employer)
    await add_user(message.from_user.id)


@router.message(Command(commands=['choice']))
async def command_choice(message: Message):
    await message.reply(text=texts.employ_or_employer, reply_markup=inkb_employ_employer)


@router.message(Command(commands=['create_vacancy']))
async def command_create_vacancy(message: Message, state: FSMContext):
    await message.answer(texts.start_create)
    await message.answer(texts.fill_employer)
    await state.set_state(sf.fill_employer)


@router.message(Command(commands=['favorites']))
async def show_favorites(message: Message):
    user_tg_id = message.from_user.id
    liked_vacancies = await get_liked_vacancies(user_tg_id)
    for vacancy in liked_vacancies:
        text = await vacancy_to_text(vacancy, "short")
        id = vacancy[0]
        await message.answer(text=text, reply_markup=await create_inkb(id, isnext=False, like_nlike="nlike", more_less="more"))
