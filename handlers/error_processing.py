from aiogram.types import Message
from aiogram.fsm.state import default_state
from aiogram import Router, F
from aiogram.filters import StateFilter, Command

from keyboards.inline_keyboards import *

from assets import texts

router = Router()


@router.message(~StateFilter(default_state), ~F.text)
async def command_cancel_create(message: Message):
    await message.answer(texts.warning_msg)


@router.message(Command(commands=[""]))
async def command_cancel_create(message: Message):
    await message.answer(texts.command_doesnt_exist)


@router.message(StateFilter(default_state))
async def command_cancel_create(message: Message):
    await message.answer(texts.random_msg, reply_markup=inkb_main_page)
