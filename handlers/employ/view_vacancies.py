from aiogram.types import CallbackQuery
from aiogram.filters import Text, StateFilter
from aiogram.fsm.state import default_state
from aiogram import Router, F

from methods.redis import users_history
from keyboards.inline_keyboards import *

from methods import get_vacancies_to_text, add_like_vacancy, del_like_vacancy, vacancy_to_text

from assets import texts

router = Router()


@router.callback_query(Text("employ"))
async def callback_employ_vacancies(callback: CallbackQuery):
    await callback.message.answer(texts.employ_warn_info)

    vacancy_text, vacancy_id = await get_vacancies_to_text(user_tg_id=callback.from_user.id)
    if vacancy_id == -1:
        await callback.message.answer(vacancy_text)
        return

    await callback.message.answer(text=vacancy_text,
                                  reply_markup=await create_inkb(id=vacancy_id, isnext=True, like_nlike="like",
                                                                 more_less="more"))

    await users_history.add_history(user_tg_id=callback.from_user.id,
                                    vacancy_id=vacancy_id)
    await callback.answer()


@router.callback_query(F.data.startswith("next"))
async def callback_next_vacancy(callback: CallbackQuery):
    vacancy_text, vacancy_id = await get_vacancies_to_text(user_tg_id=callback.from_user.id)
    more_less = callback.message.reply_markup.inline_keyboard[0][1].callback_data[:4]
    like_nlike = callback.message.reply_markup.inline_keyboard[0][2].callback_data[:4]
    past_vacancy_id = callback.data.split("_")[1]

    await callback.message.edit_reply_markup(reply_markup=await create_inkb(id=past_vacancy_id,
                                                                            isnext=False,
                                                                            like_nlike=like_nlike,
                                                                            more_less=more_less))
    if vacancy_id == -1:
        await callback.message.answer(vacancy_text)
        return

    await callback.message.answer(text=vacancy_text, reply_markup=await create_inkb(id=vacancy_id,
                                                                                    isnext=True,
                                                                                    like_nlike="like",
                                                                                    more_less="more"))

    await users_history.add_history(user_tg_id=callback.from_user.id,
                                    vacancy_id=vacancy_id)


@router.callback_query(StateFilter(default_state), F.data.startswith("more"))
async def callback_more_vacancy(callback: CallbackQuery):
    if callback.message.reply_markup.inline_keyboard[1][0].text == 'Следующаю ➡️':
        like_nlike = callback.message.reply_markup.inline_keyboard[0][2].callback_data[:4]
        isnext = True
    else:
        like_nlike = callback.message.reply_markup.inline_keyboard[0][1].callback_data[:4]
        isnext = False
    id = callback.data.split("_")[1]
    text = await vacancy_to_text(int(id), "long")

    await callback.message.edit_text(text=text, reply_markup=await create_inkb(id=id,
                                                                               isnext=isnext,
                                                                               like_nlike=like_nlike,
                                                                               more_less="less"))


@router.callback_query(StateFilter(default_state), F.data.startswith("less"))
async def callback_less_vacancy(callback: CallbackQuery):
    if callback.message.reply_markup.inline_keyboard[1][0].text == 'Следующаю ➡️':
        like_nlike = callback.message.reply_markup.inline_keyboard[0][2].callback_data[:4]
        isnext = True
    else:
        like_nlike = callback.message.reply_markup.inline_keyboard[0][1].callback_data[:4]
        isnext = False
    id = callback.data.split("_")[1]
    text = await vacancy_to_text(int(id), "short")

    await callback.message.edit_text(text=text, reply_markup=await create_inkb(id=id,
                                                                               isnext=isnext,
                                                                               like_nlike=like_nlike,
                                                                               more_less="more"))


@router.callback_query(StateFilter(default_state), F.data.startswith("like"))
async def callback_like_vacancy(callback: CallbackQuery):
    if callback.message.reply_markup.inline_keyboard[1][0].text == 'Следующаю ➡️':
        less_more = callback.message.reply_markup.inline_keyboard[0][1].callback_data[:4]
        isnext = True
    else:
        less_more = callback.message.reply_markup.inline_keyboard[1][0].callback_data[:4]
        isnext = False
    id = callback.data.split("_")[1]
    await add_like_vacancy(callback.from_user.id, id)
    await callback.answer(texts.like_notification)

    await callback.message.edit_reply_markup(reply_markup=await create_inkb(id=id,
                                                                            isnext=isnext,
                                                                            like_nlike="nlike",
                                                                            more_less=less_more))


@router.callback_query(StateFilter(default_state), F.data.startswith("nlike"))
async def callback_like_vacancy(callback: CallbackQuery):
    if callback.message.reply_markup.inline_keyboard[1][0].text == 'Следующаю ➡️':
        less_more = callback.message.reply_markup.inline_keyboard[0][1].callback_data[:4]
        isnext = True
    else:
        less_more = callback.message.reply_markup.inline_keyboard[1][0].callback_data[:4]
        isnext = False
    id = callback.data.split("_")[1]
    await del_like_vacancy(callback.from_user.id)
    await callback.answer(texts.nlike_notification)

    await callback.message.edit_reply_markup(reply_markup=await create_inkb(id=id,
                                                                            isnext=isnext,
                                                                            like_nlike="like",
                                                                            more_less=less_more))
