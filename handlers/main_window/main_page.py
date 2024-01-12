from aiogram.types import CallbackQuery, BufferedInputFile
from aiogram.fsm.state import default_state
from assets import texts
from aiogram import Router, F
from aiogram.filters import StateFilter

from classes import vac_commands, User, Vacancy, db_commands, redis_commands
from keyboards.inline_keyboards import *

router = Router()
router.callback_query.filter(StateFilter(default_state))


@router.callback_query(F.data == "main_window")
async def callback_favorites(callback: CallbackQuery, user: User):
    markup = inkb_verified_users if await redis_commands.check_verification(user) else inkb_not_verified_users
    await callback.message.answer(texts.main_page, reply_markup=markup)


@router.callback_query(F.data == "favorites")
async def callback_favorites(callback: CallbackQuery, user: User):
    user_liked_vacancies = await vac_commands.get_user_likes(user)

    if user_liked_vacancies:
        for vacancy_values in user_liked_vacancies:
            photo = BufferedInputFile(vacancy_values[9], filename="")

            vacancy = Vacancy(values=await db_commands.row_to_dict(vacancy_values))
            text = await vac_commands.to_text(vacancy=vacancy,
                                              type_descr="short")

            await callback.message.answer_photo(photo=photo,
                                                caption=text,
                                                reply_markup=await create_inkb_for_employ(id=vacancy.id,
                                                                                          is_next=False,
                                                                                          btn_like_nlike="nlike",
                                                                                          btn_more_less="more"))
    else:
        await callback.message.answer(texts.no_favorites)


@router.callback_query(StateFilter(default_state), F.data == "my_applications")
async def callback_show_my_application(callback: CallbackQuery, user: User):
    user_applications_data = await vac_commands.get_user_applications(user)
    reply_to_message_id = callback.message.message_id + 1

    if user_applications_data:
        for application_data in user_applications_data:
            photo = BufferedInputFile(application_data[9], filename="")

            vacancy = Vacancy(values=await db_commands.row_to_dict(application_data))
            vacancy_text = await vac_commands.to_text(vacancy=vacancy,
                                                      type_descr="short")
            btn_like_nlike = "nlike" if await vac_commands.check_user_like(user, vacancy) else "like"

            await callback.message.answer_photo(photo=photo,
                                                caption=vacancy_text,
                                                reply_markup=await create_inkb_for_employ(id=vacancy.id,
                                                                                          is_next=False,
                                                                                          btn_like_nlike=btn_like_nlike,
                                                                                          btn_more_less="more"))

            emoji = lambda text: "✅" if text == "Принято" else "❌" if text == "Отклонено" else "⏳"
            await callback.message.answer(text=f'ℹ️ Статус – {str(application_data[11]).lower()} '
                                               f'{emoji(str(application_data[11]))}\n\n💬 {application_data[10]}',

                                          reply_to_message_id=reply_to_message_id,
                                          reply_markup=await create_inkb_del_applicaion(user_id=user.tg_id,
                                                                                        vacancy_id=vacancy.values.get(
                                                                                            "id")))
            reply_to_message_id += 2
    else:
        await callback.message.answer(texts.no_user_application)


@router.callback_query(F.data == "my_vacancies")
async def callback_my_vacancies(callback: CallbackQuery, user: User):
    created_user_vacancies = await vac_commands.get_user_creates(user)

    if created_user_vacancies:
        for vacancy_values in created_user_vacancies:
            photo = BufferedInputFile(vacancy_values[9], filename="")

            vacancy = Vacancy(values=await db_commands.row_to_dict(vacancy_values))
            text = await vac_commands.to_text(vacancy=vacancy,
                                              type_descr="short")

            await callback.message.answer_photo(photo=photo,
                                                caption=text,
                                                reply_markup=await create_inkb_for_employer(id=vacancy.id,
                                                                                            btn_more_less="more"))
    else:
        await callback.message.answer(texts.no_created, reply_markup=inkb_create_vacancy)


@router.callback_query(F.data == "settings")
async def callback_settings(callback: CallbackQuery, user: User):
    await callback.message.edit_text("Настройки бота:", reply_markup=inkb_settings)

