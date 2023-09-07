from aiogram.types import CallbackQuery
from aiogram.filters import Text, StateFilter
from aiogram.fsm.state import default_state
from aiogram import Router

from methods.redis import users_history
from keyboard.inline_keyboards import *

from methods import get_vacancies_to_text

from assets import texts

router = Router()


@router.callback_query(Text("employ"))
async def callback_employ_vacancies(callback: CallbackQuery):
    await callback.message.answer(texts.employ_warn_info)

    vacancy_text, vacancy_id = await get_vacancies_to_text(user_tg_id=callback.from_user.id)

    await callback.message.answer(text=vacancy_text,
                                  reply_markup=inkb_contact_like_more_next)

    await users_history.add_history(user_tg_id=callback.from_user.id,
                                    vacancy_id=vacancy_id)


@router.callback_query(Text("next"))
async def callback_next_vacancy(callback: CallbackQuery):

    vacancy_text, vacancy_id = await get_vacancies_to_text(user_tg_id=callback.from_user.id)

    await callback.message.edit_reply_markup(reply_markup=inkb_contact_like_more)
    await callback.message.answer(text=vacancy_text,
                                  reply_markup=inkb_contact_like_more_next)

    await users_history.add_history(user_tg_id=callback.from_user.id,
                                    vacancy_id=vacancy_id)



@router.callback_query(StateFilter(default_state), Text("more"))
async def callback_more_vacancy(callback: CallbackQuery):
    if btn_next in callback.message.reply_markup.inline_keyboard[-1]:
        markup = inkb_contact_like_less_next
    else:
        markup = inkb_contact_like_less

    await callback.message.edit_text(text="очко", reply_markup=markup)


@router.callback_query(StateFilter(default_state), Text("less"))
async def callback_less_vacancy(callback: CallbackQuery):
    if btn_next in callback.message.reply_markup.inline_keyboard[-1]:
        markup = inkb_contact_like_more_next
    else:
        markup = inkb_contact_like_more

    await callback.message.edit_text("sfd", reply_markup=markup)


@router.callback_query(StateFilter(default_state), Text("like"))
async def callback_like_vacancy(callback: CallbackQuery):
    message_text = "sfd"
    await callback.message.answer(message_text, reply_markup=inkb_contact_like_more_next)
