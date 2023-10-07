from aiogram.types import CallbackQuery
from aiogram.fsm.state import default_state
from assets import texts
from aiogram import Router
from aiogram.filters import StateFilter, Text

from classes import vac_commands, User, Vacancy, db_commands
from keyboards.inline_keyboards import *

router = Router()
router.callback_query.filter(StateFilter(default_state))


@router.callback_query(Text("favorites"))
async def callback_favorites(callback: CallbackQuery, user: User):
    user_liked_vacancies = await vac_commands.get_user_likes(user)

    if user_liked_vacancies:
        for vacancy_values in user_liked_vacancies:
            vacancy = Vacancy(values=await db_commands.row_to_dict(vacancy_values))

            text = await vac_commands.to_text(vacancy=vacancy,
                                              type_descr="short")

            await callback.message.answer(text=text,
                                          reply_markup=await create_inkb(id=vacancy.id,
                                                                         is_next=False,
                                                                         btn_like_nlike="nlike",
                                                                         btn_more_less="more"))
    else:
        await callback.message.answer(texts.no_favorites)
    await callback.answer()


@router.callback_query(Text("my_vacancies"))
async def callback_favorites(callback: CallbackQuery, user: User):
    created_user_vacancies = await vac_commands.get_user_creates(user)

    if created_user_vacancies:
        for vacancy_values in created_user_vacancies:
            vacancy = Vacancy(values=await db_commands.row_to_dict(vacancy_values))

            text = await vac_commands.to_text(vacancy=vacancy,
                                              type_descr="short")

            await callback.message.answer(text=text,
                                          reply_markup=await create_inkb_for_employer(id=vacancy.id,
                                                                                      btn_more_less="more"))
    else:
        await callback.message.answer(texts.no_created)
    await callback.answer()
