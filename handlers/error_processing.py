from aiogram.types import Message, ErrorEvent
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.state import default_state
from aiogram import Router, F
from aiogram.filters import StateFilter, Command, ExceptionTypeFilter

from classes.Statesform import VacancyFormSteps as vfs
from classes.Statesform import SenderFormSteps as sfs
from keyboards.inline_keyboards import *
from classes import *
from assets import texts

router = Router()


@router.message(~StateFilter(default_state),
                ~StateFilter(vfs.fill_image),
                ~StateFilter(vfs.edit_image),
                ~StateFilter(sfs.fill_sender_image),
                ~F.text)
async def wrong_type(message: Message):
    await message.answer(texts.warning_msg)


@router.message(Command(commands=[""]))
async def process_unknown_command(message: Message):
    await message.answer(texts.command_doesnt_exist)


@router.message(StateFilter(default_state))
async def process_unknown_message(message: Message, user: User):
    markup = inkb_verified_users if await redis_commands.check_verification(user) else inkb_not_verified_users
    await message.answer(texts.random_msg, reply_markup=markup)


@router.error(ExceptionTypeFilter(TelegramBadRequest), F.update.message.as_("message"))
async def process_bad_request_error(event: ErrorEvent, message: Message):  # удаление или редактироваие сообщения
    await message.answer(texts.waning_u_are_stupid)
