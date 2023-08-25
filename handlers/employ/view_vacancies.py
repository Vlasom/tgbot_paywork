from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Text, StateFilter
from aiogram.fsm.state import default_state
from aiogram import Router

from keyboard.inline_keyboards import *

from queue_vacancy import QueueVacancy
from vacancy import VacanciesEmploy
from assets import texts

router = Router()


@router.callback_query(Text("employ"))
async def callback_employ_vacancies(callback: CallbackQuery):
    await callback.message.answer(texts.employ_warn_info)

    await callback.message.answer(texts.employ_warn_info)

    queue = QueueVacancy(user_id=callback.message.from_user.id)

    vacancy = VacanciesEmploy("asd")

    text = str(vacancy.get_db_row())

    await callback.message.answer(text)


@router.callback_query(Text("next"))
async def callback_next_vacancy(callback: CallbackQuery):
    message_text = "sfd"
    await callback.message.answer(message_text, reply_markup=inkb_more_like_next)
    await callback.message.edit_reply_markup(reply_markup=inkb_more_like)


@router.callback_query(StateFilter(default_state), Text("more"))
async def callback_more_vacancy(callback: CallbackQuery):
    if btn_next in callback.message.reply_markup.inline_keyboard[-1]:
        markup = inkb_less_like_next
    else:
        markup = inkb_less_like

    await callback.message.edit_text("очко", reply_markup=markup)


@router.callback_query(StateFilter(default_state), Text("less"))
async def callback_less_vacancy(callback: CallbackQuery):
    message_text = "sfd"
    await callback.message.answer(message_text, reply_markup=inkb_more_like_next)


@router.callback_query(StateFilter(default_state), Text("like"))
async def callback_like_vacancy(callback: CallbackQuery):
    message_text = "sfd"
    await callback.message.answer(message_text, reply_markup=inkb_more_like_next)
