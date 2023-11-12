import asyncio

from aiogram.types import CallbackQuery, BufferedInputFile
from aiogram.filters import StateFilter
from aiogram.fsm.state import default_state
from aiogram import Router, F

from keyboards.inline_keyboards import *

from assets import texts
from classes import *


router = Router()


@router.callback_query(StateFilter(default_state), F.data == "view_vacancies")
async def callback_view_vacancies(callback: CallbackQuery, user: User):
    await callback.message.answer(texts.employ_warn_info)

    vacancy = await vac_commands.get_not_viewed(user=user)

    if not vacancy:
        return await callback.message.answer(texts.no_vacancies_msg, reply_markup=inkb_no_more_vacancies)

    photo = BufferedInputFile(vacancy.photo, filename="")
    btn_like_nlike = "nlike" if await vac_commands.check_user_like(user, vacancy) else "like"

    await callback.message.answer_photo(photo=photo,
                                        caption=vacancy.text,
                                        reply_markup=await create_inkb_for_employ(id=vacancy.id,
                                                                                  is_next=True,
                                                                                  btn_like_nlike=btn_like_nlike,
                                                                                  btn_more_less="more"))

    await redis_commands.user_add_history(user=user,
                                          vacancy=vacancy)


@router.callback_query(StateFilter(default_state), F.data.startswith("next"))
async def callback_next_vacancy(callback: CallbackQuery, user: User):
    vacancy = await vac_commands.get_not_viewed(user=user)

    btn_more_less = callback.message.reply_markup.inline_keyboard[1][0].callback_data[:4]
    btn_like_nlike = callback.message.reply_markup.inline_keyboard[0][1].callback_data[:4]

    past_vacancy_id = callback.data.split("_")[1]

    await callback.message.edit_reply_markup(reply_markup=await create_inkb_for_employ(id=past_vacancy_id,
                                                                                       is_next=False,
                                                                                       btn_like_nlike=btn_like_nlike,
                                                                                       btn_more_less=btn_more_less))
    if not vacancy:
        await asyncio.sleep(.5)
        return await callback.message.answer(texts.no_vacancies_notification, reply_markup=inkb_on_off_notifi)

    photo = BufferedInputFile(vacancy.photo, filename="")
    btn_like_nlike = "nlike" if await vac_commands.check_user_like(user, vacancy) else "like"

    await callback.message.answer_photo(photo=photo,
                                        caption=vacancy.text,
                                        reply_markup=await create_inkb_for_employ(id=vacancy.id,
                                                                                  is_next=True,
                                                                                  btn_like_nlike=btn_like_nlike,
                                                                                  btn_more_less="more"))

    await redis_commands.user_add_history(user=user, vacancy=vacancy)


@router.callback_query(F.data.startswith("more"))
async def callback_more(callback: CallbackQuery):
    if callback.message.reply_markup.inline_keyboard.__len__() == 3:
        is_next = True

    else:
        is_next = False

    btn_like_nlike = callback.message.reply_markup.inline_keyboard[0][1].callback_data[:4]

    vacancy = Vacancy(id=int(callback.data.split("_")[1]))

    text = await vac_commands.to_text(vacancy=vacancy,
                                      type_descr="long")

    await callback.message.edit_caption(caption=text,
                                        reply_markup=await create_inkb_for_employ(id=vacancy.id,
                                                                                  is_next=is_next,
                                                                                  btn_like_nlike=btn_like_nlike,
                                                                                  btn_more_less="less"))


@router.callback_query(F.data.startswith("less"))
async def callback_less(callback: CallbackQuery):
    if callback.message.reply_markup.inline_keyboard.__len__() == 3:
        is_next = True

    else:
        is_next = False

    btn_like_nlike = callback.message.reply_markup.inline_keyboard[0][1].callback_data[:4]

    vacancy = Vacancy(id=int(callback.data.split("_")[1]))

    text = await vac_commands.to_text(vacancy=vacancy,
                                      type_descr="short")

    await callback.message.edit_caption(caption=text,
                                        reply_markup=await create_inkb_for_employ(id=vacancy.id,
                                                                                  is_next=is_next,
                                                                                  btn_like_nlike=btn_like_nlike,
                                                                                  btn_more_less="more"))


@router.callback_query(StateFilter(default_state), F.data == "redisplay")
async def callback_redisplay_vacancy(callback: CallbackQuery, user: User):
    text = f"{callback.message.text}\n\n—————\nПоcмотреть вакансии заново 🔄"
    await callback.message.edit_text(text)
    await redis_commands.user_del_history(user)

    vacancy = await vac_commands.get_not_viewed(user=user)

    if not vacancy:
        return await callback.message.answer(texts.no_vacancies_msg, reply_markup=inkb_no_more_vacancies)

    photo = BufferedInputFile(vacancy.photo, filename="")
    await callback.message.answer_photo(photo=photo,
                                        caption=vacancy.text,
                                        reply_markup=await create_inkb_for_employ(id=vacancy.id,
                                                                                  is_next=True,
                                                                                  btn_like_nlike="like",
                                                                                  btn_more_less="more"))

    await redis_commands.user_add_history(user=user,
                                          vacancy=vacancy)


@router.callback_query(StateFilter(default_state), F.data == "back_later")
async def callback_back_later(callback: CallbackQuery):
    text = f"{callback.message.text}\n\n—————\nВернусь позже 🔜"
    await callback.message.edit_text(text)
    await callback.message.answer(texts.ok_bro_msg)
