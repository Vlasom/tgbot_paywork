import asyncio

from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from fsm.statesform import StapesForm as sf
from assets import texts
from aiogram import Router, Bot, F
from aiogram.filters import Command, Text, StateFilter

from keyboard.inline_keyboards import *

router = Router()

router.message.filter(~StateFilter(default_state))


@router.message(~F.text)
async def command_cancel_create(message: Message):
    await message.answer(texts.warning_msg)