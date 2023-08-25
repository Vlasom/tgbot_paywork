from aiogram.types import Message, InlineKeyboardMarkup
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from fsm.statesform import StapesForm as sf
from aiogram import Router
from assets import texts
from keyboard import inline_buttons

import asyncio


router = Router()
# добавить фильтры для роутера


@router.message(Command(commands=['start']))
async def command_start(message: Message):
    await message.reply(texts.welcome_text)
    await asyncio.sleep(0.5)

    markup = InlineKeyboardMarkup(inline_keyboard=[[
        inline_buttons.btn_employer,
        inline_buttons.btn_employ]])

    await message.reply(text=texts.employ_or_employer, reply_markup=markup)


@router.message(Command(commands=['choice']))
async def command_choice(message: Message):
    markup = InlineKeyboardMarkup(inline_keyboard=[[
        inline_buttons.btn_employer,
        inline_buttons.btn_employ]])

    await message.reply(text=texts.employ_or_employer, reply_markup=markup)


@router.message(Command(commands=['create_vacancy']))
async def command_create_vacancy(message: Message, state: FSMContext):
    await message.answer(texts.start_create)
    await message.answer(texts.fill_employer)
    await state.set_state(sf.fill_employer)
