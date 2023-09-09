import asyncio

from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from fsm.statesform import StapesForm as sf
from assets import texts
from aiogram import Router, Bot, F
from aiogram.filters import Command, Text, StateFilter

from keyboards.inline_keyboards import *

router = Router()

@router.message(~StateFilter(default_state), Command(commands=['main_page']))
async def command_cancel_create(message: Message):
    await message.answer(texts.sure_cancel_create_vacancy, reply_markup=inkb_yes_no)