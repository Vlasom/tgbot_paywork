from aiogram.types import Message, CallbackQuery, ErrorEvent
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


@router.callback_query(StateFilter(vfs.fill_employer,
                                   vfs.fill_job,
                                   vfs.fill_salary,
                                   vfs.fill_min_age,
                                   vfs.fill_min_exp,
                                   vfs.fill_date,
                                   vfs.fill_short_dsp,
                                   vfs.fill_long_dsp,
                                   vfs.fill_image,
                                   vfs.confirm_create,
                                   vfs.edit_employer,
                                   vfs.edit_job,
                                   vfs.edit_salary,
                                   vfs.edit_min_age,
                                   vfs.edit_min_exp,
                                   vfs.edit_date,
                                   vfs.edit_short_dsp,
                                   vfs.edit_long_dsp,
                                   vfs.edit_image))
async def callback_in_creating_vacancy(callback: CallbackQuery):
    await callback.answer(text=texts.callback_in_creating_vacancy, show_alert=True)


@router.callback_query(StateFilter(vfs.create_application))
async def callback_in_creating_application(callback: CallbackQuery):
    await callback.answer(text=texts.callback_in_creating_application, show_alert=True)


@router.message(~StateFilter(default_state),
                ~StateFilter(vfs.fill_image),
                ~StateFilter(vfs.edit_image),
                ~StateFilter(sfs.fill_sender_image),
                ~F.text)
async def wrong_type(message: Message):
    await message.answer(texts.warning_msg)


@router.message(StateFilter(vfs.fill_image, vfs.edit_image, sfs.fill_sender_image),
                ~(F.photo | F.document))
async def wrong_type_image(message: Message):
    await message.answer(texts.awaitable_image)


@router.message(StateFilter(default_state))
async def process_unknown_message(message: Message, user: User):
    markup = inkb_verified_users if await redis_commands.check_verification(user) else inkb_not_verified_users
    await message.answer(texts.random_msg, reply_markup=markup)


@router.error(ExceptionTypeFilter(TelegramBadRequest), F.update.message.as_("message"))
async def process_bad_request_error(event: ErrorEvent, message: Message):  # удаление или редактироваие сообщения
    await message.answer(texts.waning_u_are_stupid)
