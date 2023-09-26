from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from fsm.statesform import StapesForm as sf

from keyboards.inline_keyboards import *
from methods.sqlite.users import add_user
from methods.sqlite.vacancies import get_liked_vacancies, vacancy_to_text, get_created_vacancies

from assets import texts
import asyncio

__all__ = [ "command_start", "command_choice", "command_create_vacancy"]

router = Router()


@router.message(Command(commands=['start']))
async def command_start(message: Message, bot: Bot, state: FSMContext):
    if await state.get_state() is None:
        await message.reply(texts.welcome_text)
        await asyncio.sleep(0.3)
        await message.answer(text=texts.employ_or_employer, reply_markup=inkb_employ_employer)
        await add_user(message.from_user.id, message.from_user.username, message.from_user.full_name)
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
        if liked_vacancies:
            for vacancy in liked_vacancies:
                text = await vacancy_to_text(vacancy, "short")
                id = vacancy[0]
                await message.answer(text=text,
                                     reply_markup=await create_inkb(id=id,
                                                                    is_next=False,
                                                                    btn_like_nlike="nlike",
                                                                    btn_more_less="more"))
        else:
            await message.answer(texts.no_favorites)

    else:
        await message.answer(texts.default_state_warn)

@router.message(Command(commands=['my_vacancies']))
async def command_show_created_vacancies(message: Message, state: FSMContext):
    if await state.get_state() is None:
        vacancies = await get_created_vacancies(message.from_user.id)
        if vacancies:
            for vacancy in vacancies:
                text = await vacancy_to_text(vacancy, "short")
                id = vacancy[0]
                await message.answer(text=text,
                                     reply_markup=await create_inkb_for_employer(id=id,
                                                                                 btn_more_less="more"))
        else:
            await message.answer(texts.no_created)

    else:
        await message.answer(texts.default_state_warn)