from aiogram.types import Message, InlineKeyboardMarkup
from aiogram.filters import Command
from aiogram import Router
from assets import texts
from keyboard import inline_buttons

import asyncio


router = Router()


@router.message(Command(commands=['start']))
async def start_command(message: Message):
    await message.reply(texts.welcome_text)
    await asyncio.sleep(0.5)

    markup = InlineKeyboardMarkup(inline_keyboard=[[
        inline_buttons.btn_employer,
        inline_buttons.btn_employ]])

    await message.reply(text=texts.employ_or_employer, reply_markup=markup)


@router.message(Command(commands=['choice']))
async def choice_command(message: Message):
    markup = InlineKeyboardMarkup(inline_keyboard=[[
        inline_buttons.btn_employer,
        inline_buttons.btn_employ]])

    await message.reply(text=texts.employ_or_employer, reply_markup=markup)
