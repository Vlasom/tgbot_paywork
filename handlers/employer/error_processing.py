from aiogram.types import Message
from aiogram.fsm.state import default_state
from assets import texts
from aiogram import Router, F
from aiogram.filters import StateFilter


router = Router()

router.message.filter(~StateFilter(default_state))


@router.message(~F.text)
async def command_cancel_create(message: Message):
    await message.answer(texts.warning_msg)