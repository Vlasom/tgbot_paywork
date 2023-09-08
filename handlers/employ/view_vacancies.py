from aiogram.types import CallbackQuery
from aiogram.filters import Text, StateFilter
from aiogram.fsm.state import default_state
from aiogram import Router, F

from methods.redis import users_history
from keyboards.inline_keyboards import *

from methods import get_vacancies_to_text, get_description

from assets import texts

router = Router()


@router.callback_query(Text("employ"))
async def callback_employ_vacancies(callback: CallbackQuery):
    await callback.message.answer(texts.employ_warn_info)

    vacancy_text, vacancy_id = await get_vacancies_to_text(user_tg_id=callback.from_user.id)

    await callback.message.answer(text=vacancy_text,
                                  reply_markup=await create_inkb(id=vacancy_id, isnext=True, more_less="more"))

    await users_history.add_history(user_tg_id=callback.from_user.id,
                                    vacancy_id=vacancy_id)
    await callback.answer()


@router.callback_query(F.data.startswith("next"))
async def callback_next_vacancy(callback: CallbackQuery):

    vacancy_text, vacancy_id = await get_vacancies_to_text(user_tg_id=callback.from_user.id)
    more_less = callback.message.reply_markup.inline_keyboard[0][1].callback_data[:4]


    await callback.message.edit_reply_markup(reply_markup=await
                                                        create_inkb(id=vacancy_id, isnext=False, more_less=more_less))

    await callback.message.answer(text=vacancy_text, reply_markup=await
                                                        create_inkb(id=vacancy_id, isnext=True, more_less="more"))

    await users_history.add_history(user_tg_id=callback.from_user.id,
                                    vacancy_id=vacancy_id)



@router.callback_query(StateFilter(default_state), F.data.startswith("more"))
async def callback_more_vacancy(callback: CallbackQuery):
    if callback.message.reply_markup.inline_keyboard[1][0].text == 'Следующаю ➡️':
        isnext = True
    else:
        isnext = False
    id = callback.data.split("_")[1]
    text = await get_description(id, "l_dscr")

    await callback.message.edit_text(text=text, reply_markup=await
                                                        create_inkb(id=id, isnext=isnext, more_less="less"))


@router.callback_query(StateFilter(default_state), F.data.startswith("less"))
async def callback_less_vacancy(callback: CallbackQuery):
    if callback.message.reply_markup.inline_keyboard[1][0].text == 'Следующаю ➡️':
        isnext = True
    else:
        isnext = False
    id = callback.data.split("_")[1]
    text = await get_description(id, "s_dscr")

    await callback.message.edit_text(text=text, reply_markup=await
                                                        create_inkb(id=id, isnext=isnext, more_less="more"))


@router.callback_query(StateFilter(default_state), F.data.startswith("like"))
async def callback_like_vacancy(callback: CallbackQuery):
    message_text = "sfd"
    await callback.message.answer(message_text, reply_markup=inkb_contact_like_more_next)
