from aiogram import Router, Bot, F
from aiogram.types import Message, BufferedInputFile
from aiogram.filters import Command, StateFilter, CommandObject
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


@router.message(StateFilter(default_state), Command(commands=['start']))
async def command_start(message: Message, user: User, bot: Bot):
    await set_default_commands(bot, message.from_user.id, user)
    await message.reply(texts.welcome_text(message.from_user.id, message.from_user.first_name))
    await asyncio.sleep(0.3)
    await message.answer(text=texts.employ_or_employer, reply_markup=inkb_employ_employer)
    await db_commands.add_user_to_db(user)


@router.message(StateFilter(default_state), Command(commands=['help']))
async def command_help(message: Message):
    await message.answer(text=texts.help_txt)


@router.message(StateFilter(default_state), Command(commands=['view_vacancies']))
async def command_view_vacancies(message: Message, user: User):
    await message.answer(texts.employ_warn_info)

    vacancy = await vac_commands.get_not_viewed(user=user)

    if not vacancy:
        return await message.answer(texts.no_vacancies_msg, reply_markup=inkb_no_more_vacancies)

    photo = BufferedInputFile(vacancy.photo, filename="")
    await message.answer_photo(photo=photo,
                               caption=vacancy.text,
                               reply_markup=await create_inkb_for_employ(id=vacancy.id,
                                                                         is_next=True,
                                                                         btn_like_nlike="like",
                                                                         btn_more_less="more"))

    await redis_commands.user_add_history(user=user,
                                          vacancy=vacancy)


@router.message(StateFilter(default_state), Command(commands=['create_vacancy']))
async def command_create_vacancy(message: Message, state: FSMContext, user: User):
    if await redis_commands.check_verification(user):
        await message.answer(texts.start_create, reply_markup=inkb_cancel_action)
        await message.answer(texts.fill_employer)
        await state.set_state(vfs.fill_employer)
    else:
        await message.answer(texts.unverified_user)


@router.message(StateFilter(default_state), Command(commands=['main_page']))
async def command_main_page(message: Message, user: User):
    markup = inkb_verified_users if await redis_commands.check_verification(user) else inkb_not_verified_users
    await message.answer(texts.main_page, reply_markup=markup)


@router.message(StateFilter(default_state), Command(commands=['favorites']))
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


@router.message(StateFilter(default_state), Command(commands=['my_vacancies']))
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


@router.message(StateFilter(default_state), Command(commands=['my_applications']))
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


@router.message(IsAdmin(), StateFilter(default_state), Command(commands=['admin']))
async def admin_panel(message: Message):
    await message.answer("Приветсвую, Создатель", reply_markup=inkb_admin_panel)


@router.message(StateFilter(default_state), Command(commands=['password_verify']))
async def command_set_verstatus(message: Message, bot: Bot, command: CommandObject):
    try:
        user_tg_id = command.args
        await redis_commands.verify(user_tg_id)
        await redis_commands.load_verified_users()
        await bot.send_message(chat_id=user_tg_id, text="✅ Вы получили статус работодателя")
        await message.answer("Успешно")

    except Exception as ex:
        await message.answer("Не удалось верифицировать пользователя\n\nОшибка\n\n" + str(ex))


@router.message(StateFilter(vfs.fill_employer,
                            vfs.fill_job,
                            vfs.fill_salary,
                            vfs.fill_min_age,
                            vfs.fill_min_exp,
                            vfs.fill_date,
                            vfs.fill_short_dsp,
                            vfs.fill_long_dsp,
                            vfs.confirm_create,
                            vfs.edit_employer,
                            vfs.edit_job,
                            vfs.edit_salary,
                            vfs.edit_min_age,
                            vfs.edit_min_exp,
                            vfs.edit_date,
                            vfs.edit_short_dsp,
                            vfs.edit_long_dsp),
                ~Command(commands=['cancel']),
                F.text.startswith("/"))
async def command_in_creating_vacancy(message: Message, state: FSMContext):
    await message.answer(texts.command_in_creating_vacancy)
    state_now = await state.get_state()
    if state_now == vfs.fill_employer:
        await message.answer(texts.fill_employer)
    if state_now == vfs.fill_job:
        await message.answer(texts.fill_job)
    if state_now == vfs.fill_salary:
        await message.answer(texts.fill_salary)
    if state_now == vfs.fill_min_age:
        await message.answer(texts.fill_min_age, reply_markup=inkb_skip_stage_create)
    if state_now == vfs.fill_min_exp:
        await message.answer(texts.fill_min_exp, reply_markup=inkb_skip_stage_create)
    if state_now == vfs.fill_short_dsp:
        await message.answer(texts.fill_date)
    if state_now == vfs.fill_long_dsp:
        await message.answer(texts.fill_short_dsp)


@router.message(StateFilter(default_state), Command(commands=['cancel']))
async def command_cancel_in_default_state(message: Message):
    await message.answer(texts.command_cancel_in_default_state)


@router.message(StateFilter(vfs.create_application),
                ~Command(commands=['cancel']),
                F.text.startswith("/"))
async def command_in_creating_application(message: Message):
    await message.answer(texts.command_in_creating_application)


@router.message(F.text.startswith("/"),
                ~Command(commands=['cancel']))
async def process_unknown_command(message: Message):
    await message.answer(texts.command_doesnt_exist)
