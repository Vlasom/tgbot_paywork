from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from fsm.statesform import StapesForm as sf

from keyboards.inline_keyboards import *
from methods.sqlite.users import add_user
from methods.sqlite.vacancies import get_liked_vacancies, vacancy_to_text

from assets import texts
import asyncio

__all__ = ["command_choice", "command_start", "command_create_vacancy"]

router = Router()


@router.message(Command(commands=['start']))
async def command_start(message: Message, state: FSMContext):
    if await state.get_state() is None:
        await message.reply(texts.welcome_text)
        await asyncio.sleep(0.3)
        await message.answer(text=texts.employ_or_employer, reply_markup=inkb_employ_employer)
        await add_user(message.from_user.id)
    else:
        await message.answer(text=texts.default_state_warn)



@router.message(Command(commands=['choice']))
async def command_choice(message: Message, state: FSMContext):
    if await state.get_state() is None:
        await message.reply(text=texts.employ_or_employer, reply_markup=inkb_employ_employer)
    else:
        await message.answer(texts.default_state_warn)


@router.message(Command(commands=['create_vacancy']))
async def command_create_vacancy(message: Message, state: FSMContext):
    if await state.get_state() is None:
        await message.answer(texts.start_create)
        await message.answer(texts.fill_employer)
        await state.set_state(sf.fill_employer)
    else:
        await message.answer(texts.default_state_warn)


@router.message(Command(commands=['favorites']))
async def command_show_favorites(message: Message, state: FSMContext):
    if await state.get_state() is None:
        user_tg_id = message.from_user.id
        liked_vacancies = await get_liked_vacancies(user_tg_id)
        for vacancy in liked_vacancies:
            text = await vacancy_to_text(vacancy, "short")
            id = vacancy[0]
            await message.answer(text=text, reply_markup=await create_inkb(id, is_next=False, btn_like_nlike="nlike", btn_more_less="more"))
    else:
        await message.answer(texts.default_state_warn)
