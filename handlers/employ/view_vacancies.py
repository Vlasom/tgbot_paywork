from aiogram.types import CallbackQuery
from aiogram.filters import Text, StateFilter
from aiogram.fsm.state import default_state
from aiogram import Router, F

from methods.redis import users_history
from keyboards.inline_keyboards import *

from methods.sqlite.vacancies import add_like_vacancy, del_like_vacancy, vacancy_to_text
from methods.sqlite.users import on_nitifi_in_db, off_nitifi_in_db

from assets import texts
from methods.sqlite.sql_class import *
import sqlite3


router = Router()

_conn = sqlite3.connect("database//database.db")
_cur = _conn.cursor()

_sql_connection = SqlConnection(_cur, _conn)

redis_commands = RedisCommands()
db_commands = DatabaseCommands(sql_connection=_sql_connection)

vac_commands = VacanciesCommands(sql_connection=_sql_connection,
                                 db_commands=db_commands,
                                 redis_commands=redis_commands)


@router.callback_query(Text("employ"))
async def callback_employ_vacancies(callback: CallbackQuery):

    await callback.message.answer(texts.employ_warn_info)

    vacancy_text, vacancy_id = await vac_commands.get_not_viewed(user_tg_id=callback.from_user.id)

    vacancy = Vacancy(id=vacancy_id, text=vacancy_text)

    if vacancy.id == -1:
        await callback.answer()
        return await callback.message.answer(vacancy.text, reply_markup=inkb_on_off_notifi)

    await callback.message.answer(text=vacancy.text,
                                  reply_markup=await create_inkb(id=vacancy.id,
                                                                 is_next=True,
                                                                 btn_like_nlike="like",
                                                                 btn_more_less="more"))

    await redis_commands.user_add_history(user_tg_id=callback.from_user.id,
                                          vacancy=vacancy)
    await callback.answer()


@router.callback_query(F.data.startswith("next"))
async def callback_next_vacancy(callback: CallbackQuery):

    vacancy_text, vacancy_id = await vac_commands.get_not_viewed(user_tg_id=callback.from_user.id)
    vacancy = Vacancy(id=vacancy_id, text=vacancy_text)

    btn_more_less = callback.message.reply_markup.inline_keyboard[0][1].callback_data[:4]
    btn_like_nlike = callback.message.reply_markup.inline_keyboard[0][2].callback_data[:4]

    past_vacancy_id = callback.data.split("_")[1]

    await callback.message.edit_reply_markup(reply_markup=await create_inkb(id=past_vacancy_id,
                                                                            is_next=False,
                                                                            btn_like_nlike=btn_like_nlike,
                                                                            btn_more_less=btn_more_less))
    if vacancy.id == -1:
        return await callback.message.answer(vacancy.text, reply_markup=inkb_on_off_notifi)

    await callback.message.answer(text=vacancy.text,
                                  reply_markup=await create_inkb(id=vacancy.id,
                                                                 is_next=True,
                                                                 btn_like_nlike="like",
                                                                 btn_more_less="more"))

    await users_history.add_history(user_tg_id=callback.from_user.id,
                                    vacancy_id=vacancy.id)


@router.callback_query(StateFilter(default_state), F.data.startswith("more"))
async def callback_more_vacancy(callback: CallbackQuery):

    if callback.message.reply_markup.inline_keyboard[1][0].text.startswith("След"):
        btn_like_nlike = callback.message.reply_markup.inline_keyboard[0][2].callback_data[:4]
        is_next = True

    else:
        btn_like_nlike = callback.message.reply_markup.inline_keyboard[0][1].callback_data[:4]
        is_next = False

    vacancy = Vacancy(id=int(callback.data.split("_")[1]))

    text = await vacancy_to_text(vacancy=vacancy.id,
                                 type_descr="long")

    await callback.message.edit_text(text=text,
                                     reply_markup=await create_inkb(id=vacancy.id,
                                                                    is_next=is_next,
                                                                    btn_like_nlike=btn_like_nlike,
                                                                    btn_more_less="less"))


@router.callback_query(StateFilter(default_state), F.data.startswith("less"))
async def callback_less_vacancy(callback: CallbackQuery):

    if callback.message.reply_markup.inline_keyboard[1][0].text.startswith("След"):
        btn_like_nlike = callback.message.reply_markup.inline_keyboard[0][2].callback_data[:4]
        is_next = True

    else:
        btn_like_nlike = callback.message.reply_markup.inline_keyboard[0][1].callback_data[:4]
        is_next = False

    vacancy = Vacancy(id=int(callback.data.split("_")[1]))

    text = await vacancy_to_text(vacancy=vacancy.id,
                                 type_descr="short")

    await callback.message.edit_text(text=text, reply_markup=await create_inkb(id=vacancy.id,
                                                                               is_next=is_next,
                                                                               btn_like_nlike=btn_like_nlike,
                                                                               btn_more_less="more"))


@router.callback_query(StateFilter(default_state), F.data.startswith("like"))
async def callback_like_vacancy(callback: CallbackQuery):

    if callback.message.reply_markup.inline_keyboard[1][0].text.startswith("След"):
        btn_less_more = callback.message.reply_markup.inline_keyboard[0][1].callback_data[:4]
        is_next = True

    else:
        btn_less_more = callback.message.reply_markup.inline_keyboard[1][0].callback_data[:4]
        is_next = False

    vacancy = Vacancy(id=int(callback.data.split("_")[1]))

    await add_like_vacancy(user_tg_id=callback.from_user.id,
                           vacancy_id=vacancy.id)

    await callback.answer(texts.like_notification)

    await callback.message.edit_reply_markup(reply_markup=await create_inkb(id=vacancy.id,
                                                                            is_next=is_next,
                                                                            btn_like_nlike="nlike",
                                                                            btn_more_less=btn_less_more))


@router.callback_query(StateFilter(default_state), F.data.startswith("nlike"))
async def callback_like_vacancy(callback: CallbackQuery):
    if callback.message.reply_markup.inline_keyboard[1][0].text.startswith("След"):
        btn_less_more = callback.message.reply_markup.inline_keyboard[0][1].callback_data[:4]
        is_next = True

    else:
        btn_less_more = callback.message.reply_markup.inline_keyboard[1][0].callback_data[:4]
        is_next = False

    vacancy = Vacancy(id=int(callback.data.split("_")[1]))

    await del_like_vacancy(user_tg_id=callback.from_user.id)

    await callback.answer(texts.nlike_notification)
    await callback.message.edit_reply_markup(reply_markup=await create_inkb(id=vacancy.id,
                                                                            is_next=is_next,
                                                                            btn_like_nlike="like",
                                                                            btn_more_less=btn_less_more))


@router.callback_query(StateFilter(default_state), Text("on_notification"))
async def on_notification(callback: CallbackQuery):
    await on_nitifi_in_db(callback.from_user.id)
    await callback.answer("Уведомления включены")


@router.callback_query(StateFilter(default_state), Text("off_notification"))
async def off_notification(callback: CallbackQuery):
    await off_nitifi_in_db(callback.from_user.id)
    await callback.answer("Уведомления выключены")

