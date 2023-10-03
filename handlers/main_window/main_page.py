from aiogram.types import Message
from aiogram.fsm.state import default_state
from assets import texts
from aiogram import Router
from aiogram.filters import Command, StateFilter

from keyboards.inline_keyboards import *

router = Router()


@router.message(~StateFilter(default_state), Command(commands=['main_page']))
async def command_cancel_create(message: Message):
    await message.answer(texts.sure_cancel_create_vacancy, reply_markup=inkb_yes_no)