from aiogram import Router, Bot
from aiogram.types import Message, BufferedInputFile
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

from keyboards.inline_keyboards import *
from classes import User, Vacancy, vac_commands, db_commands, redis_commands
from classes.Statesform import VacancyFormSteps as vfs
from assets import texts
from utils.setcomands import set_default_commands
from filters.is_admin import IsAdmin

import asyncio

router = Router()
router.message.filter(StateFilter(default_state))


@router.message(Command(commands=['start']))
async def command_start(message: Message, user: User, bot: Bot):
    await message.reply(texts.welcome_text(message.from_user.id, message.from_user.first_name))
    await asyncio.sleep(0.3)
    await message.answer(text=texts.employ_or_employer, reply_markup=inkb_employ_employer)
    await set_default_commands(bot, message.from_user.id)
    await db_commands.add_user_to_db(user)


@router.message(Command(commands=['help']))
async def command_help(message: Message):
    await message.answer(text=texts.help_txt)


@router.message(Command(commands=['view_vacancies']))
async def command_view_vacancies(message: Message, user: User):
    await message.answer(texts.employ_warn_info)

    vacancy = await vac_commands.get_not_viewed(user=user)

    if not vacancy:
        return await message.answer(texts.no_vacancies_notification, reply_markup=inkb_on_off_notifi)

    photo = BufferedInputFile(vacancy.photo, filename="")
    await message.answer_photo(photo=photo,
                               caption=vacancy.text,
                               reply_markup=await create_inkb_for_employ(id=vacancy.id,
                                                                         is_next=True,
                                                                         btn_like_nlike="like",
                                                                         btn_more_less="more"))

    await redis_commands.user_add_history(user=user,
                                          vacancy=vacancy)


@router.message(Command(commands=['create_vacancy']))
async def command_create_vacancy(message: Message, state: FSMContext):
    await message.answer(texts.start_create, reply_markup=inkb_cancel_action)
    await message.answer(texts.fill_employer)
    await state.set_state(vfs.fill_employer)


@router.message(StateFilter(default_state), Command(commands=['main_page']))
async def command_main_page(message: Message, user: User):
    markup = inkb_verified_users if await redis_commands.check_verification(user) else inkb_not_verified_users
    await message.answer(texts.main_page, reply_markup=markup)


@router.message(Command(commands=['favorites']))
async def command_show_favorites(message: Message, user: User):
    user_liked_vacancies = await vac_commands.get_user_likes(user)

    if user_liked_vacancies:
        for vacancy_values in user_liked_vacancies:
            photo = BufferedInputFile(vacancy_values[9], filename="")

            vacancy = Vacancy(values=await db_commands.row_to_dict(vacancy_values))
            text = await vac_commands.to_text(vacancy=vacancy,
                                              type_descr="short")

            await message.answer_photo(photo=photo,
                                       caption=text,
                                       reply_markup=await create_inkb_for_employ(id=vacancy.id,
                                                                                 is_next=False,
                                                                                 btn_like_nlike="nlike",
                                                                                 btn_more_less="more"))
    else:
        await message.answer(texts.no_favorites, reply_markup=inkb_view_vacancies)


@router.message(Command(commands=['my_vacancies']))
async def command_show_created_vacancies(message: Message, user: User):
    created_user_vacancies = await vac_commands.get_user_creates(user)

    if created_user_vacancies:
        for vacancy_values in created_user_vacancies:
            photo = BufferedInputFile(vacancy_values[9], filename="")

            vacancy = Vacancy(values=await db_commands.row_to_dict(vacancy_values))
            text = await vac_commands.to_text(vacancy=vacancy,
                                              type_descr="short")

            await message.answer_photo(photo=photo,
                                       caption=text,
                                       reply_markup=await create_inkb_for_employer(id=vacancy.id,
                                                                                   btn_more_less="more"))
    else:
        await message.answer(texts.no_created, reply_markup=inkb_create_vacancy)


@router.message(Command(commands=['my_applications']))
async def command_show_my_application(message: Message, user: User):
    user_applications_data = await vac_commands.get_user_applications(user)
    reply_to_message_id = message.message_id + 1

    if user_applications_data:
        for application_data in user_applications_data:
            photo = BufferedInputFile(application_data[9], filename="")

            vacancy = Vacancy(values=await db_commands.row_to_dict(application_data))
            vacancy_text = await vac_commands.to_text(vacancy=vacancy,
                                                      type_descr="short")
            btn_like_nlike = "nlike" if await vac_commands.check_user_like(user, vacancy) else "like"

            await message.answer_photo(photo=photo,
                                       caption=vacancy_text,
                                       reply_markup=await create_inkb_for_employ(id=vacancy.id,
                                                                                 is_next=False,
                                                                                 btn_like_nlike=btn_like_nlike,
                                                                                 btn_more_less="more"))

            await message.answer(text=application_data[10] + "\n\n" + application_data[11],
                                 reply_to_message_id=reply_to_message_id)
            reply_to_message_id += 2
    else:
        await message.answer(texts.no_user_application)


@router.message(IsAdmin(), Command(commands=['admin']))
async def admin_panel(message: Message):
    await message.answer("Приветсвую, Создатель", reply_markup=inkb_admin_panel)
