from aiogram.types import CallbackQuery
from aiogram.filters import Text, StateFilter
from aiogram.fsm.state import default_state
from aiogram import Router

from keyboard.inline_keyboards import *

from queue_vacancy import QueueVacancy, QueueIter

from methods import vacancy_get_next

from assets import texts

router = Router()


@router.callback_query(Text("employ"))
async def callback_employ_vacancies(callback: CallbackQuery):
    await callback.message.answer(texts.employ_warn_info)

    await callback.message.answer(texts.employ_warn_info)

    # user_queue = QueueVacancy(user_id=callback.message.from_user.id, expire_date="1")
    # vacancies: list = await vacancy_view_next(5)
    # user_queue.insert(vacancies)
    # text = str(user_queue.get_next())

    vacancies: list = await vacancy_get_next("all")
    global user_queue_iter
    user_queue_iter = QueueIter(lst=vacancies, user_id=callback.from_user.id)

    text = str(user_queue_iter.next())
    user_queue_iter.insert(await vacancy_get_next(1))

    await callback.message.answer(text=text, reply_markup=inkb_contact_like_more_next)


@router.callback_query(Text("next"))
async def callback_next_vacancy(callback: CallbackQuery):

    if user_queue_iter.user_id == callback.from_user.id:
        message_text = str(user_queue_iter.next())
        await callback.message.answer(message_text, reply_markup=inkb_contact_like_more_next)
        user_queue_iter.insert(await vacancy_get_next(1))
    await callback.message.edit_reply_markup(reply_markup=inkb_contact_like_more)


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
