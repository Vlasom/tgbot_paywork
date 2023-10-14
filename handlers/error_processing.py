from aiogram.types import Message, ErrorEvent
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.state import default_state
from aiogram import Router, F
from aiogram.filters import StateFilter, Command, ExceptionTypeFilter

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


@router.error(ExceptionTypeFilter(TelegramBadRequest), F.update.message.as_("message"))
async def command_cancel_create(event: ErrorEvent, message: Message):
    await message.answer(texts.waning_u_are_stupid)

