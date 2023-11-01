import asyncio

from aiogram.types import CallbackQuery, Message, BufferedInputFile
from aiogram.filters import StateFilter, Command
from aiogram.fsm.state import default_state
from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext

from keyboards.inline_keyboards import *

from assets import texts
from classes import *
from utils.setcomands import set_cancel_application_command, set_default_commands

from classes.Statesform import VacancyFormSteps as vfs

router = Router()


@router.callback_query(StateFilter(default_state), F.data == "employ")
async def callback_employ_vacancies(callback: CallbackQuery, user: User):
    await callback.message.answer(texts.employ_warn_info)

    vacancy_text, photo_data, vacancy_id = await vac_commands.get_not_viewed(user=user)
    photo = BufferedInputFile(photo_data, filename="")

    vacancy = Vacancy(id=vacancy_id, text=vacancy_text)

    if vacancy.id == -1:
        await callback.answer()
        return await callback.message.answer(texts.no_vacancies_msg, reply_markup=inkb_no_more_vacancies)

    btn_like_nlike = "nlike" if await vac_commands.check_user_like(user, vacancy) else "like"

    await callback.message.answer_photo(photo=photo,
                                        caption=vacancy.text,
                                        reply_markup=await create_inkb_for_employ(id=vacancy.id,
                                                                                  is_next=True,
                                                                                  btn_like_nlike=btn_like_nlike,
                                                                                  btn_more_less="more"))

    await redis_commands.user_add_history(user=user,
                                          vacancy=vacancy)
    await callback.answer()


@router.callback_query(StateFilter(default_state), F.data.startswith("next"))
async def callback_next_vacancy(callback: CallbackQuery, user: User):
    vacancy_text, photo_data, vacancy_id = await vac_commands.get_not_viewed(user=user)
    photo = BufferedInputFile(photo_data, filename="")

    vacancy = Vacancy(id=vacancy_id, text=vacancy_text)

    btn_more_less = callback.message.reply_markup.inline_keyboard[1][0].callback_data[:4]
    btn_like_nlike = callback.message.reply_markup.inline_keyboard[0][1].callback_data[:4]

    past_vacancy_id = callback.data.split("_")[1]

    await callback.message.edit_reply_markup(reply_markup=await create_inkb_for_employ(id=past_vacancy_id,
                                                                                       is_next=False,
                                                                                       btn_like_nlike=btn_like_nlike,
                                                                                       btn_more_less=btn_more_less))
    if vacancy.id == -1:
        await asyncio.sleep(.5)
        return await callback.message.answer(texts.no_vacancies_notification, reply_markup=inkb_on_off_notifi)

    btn_like_nlike = "nlike" if await vac_commands.check_user_like(user, vacancy) else "like"

    await callback.message.answer_photo(photo=photo,
                                        caption=vacancy.text,
                                        reply_markup=await create_inkb_for_employ(id=vacancy.id,
                                                                                  is_next=True,
                                                                                  btn_like_nlike=btn_like_nlike,
                                                                                  btn_more_less="more"))
    vacancy = Vacancy(id=vacancy_id)

    await redis_commands.user_add_history(user=user, vacancy=vacancy)


@router.callback_query(F.data.startswith("more"))
async def callback_more_vacancy(callback: CallbackQuery):
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
async def callback_less_vacancy(callback: CallbackQuery):
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


@router.callback_query(StateFilter(default_state), F.data.startswith("like"))
async def callback_like_vacancy(callback: CallbackQuery, user: User):
    if callback.message.reply_markup.inline_keyboard.__len__() == 3:
        is_next = True

    else:
        is_next = False

    btn_less_more = callback.message.reply_markup.inline_keyboard[1][0].callback_data[:4]

    vacancy = Vacancy(id=int(callback.data.split("_")[1]))

    await vac_commands.add_to_userlikes(user=user, vacancy=vacancy)

    await callback.answer(texts.like_notification)

    await callback.message.edit_reply_markup(reply_markup=await create_inkb_for_employ(id=vacancy.id,
                                                                                       is_next=is_next,
                                                                                       btn_like_nlike="nlike",
                                                                                       btn_more_less=btn_less_more))


@router.callback_query(StateFilter(default_state), F.data.startswith("nlike"))
async def callback_like_vacancy(callback: CallbackQuery, user: User):
    if callback.message.reply_markup.inline_keyboard.__len__() == 3:
        is_next = True

    else:
        is_next = False

    btn_less_more = callback.message.reply_markup.inline_keyboard[1][0].callback_data[:4]

    vacancy = Vacancy(id=int(callback.data.split("_")[1]))
    await vac_commands.del_from_userlikes(user=user, vacancy=vacancy)

    await callback.answer(texts.nlike_notification)
    await callback.message.edit_reply_markup(reply_markup=await create_inkb_for_employ(id=vacancy.id,
                                                                                       is_next=is_next,
                                                                                       btn_like_nlike="like",
                                                                                       btn_more_less=btn_less_more))


@router.callback_query(StateFilter(default_state), F.data.startswith("contact"))
async def callback_create_application(callback: CallbackQuery, state: FSMContext, user: User, bot: Bot):
    vacancy = Vacancy(id=int(callback.data.split("_")[1]))

    if not await vac_commands.check_vacancy_application(user, vacancy):
        await state.update_data(vacancy_id=vacancy.id)
        await set_cancel_application_command(bot, callback.from_user.id)
        await state.set_state(vfs.create_application)
        await callback.message.answer(texts.creating_vacancy_application)
    else:
        await callback.message.answer(texts.already_save_application)
    await callback.answer()


@router.message(StateFilter(vfs.create_application), Command(commands=["cancel"]))
async def create_application(message: Message, state: FSMContext, bot: Bot):
    await message.answer(texts.cancel_create_application)
    await set_default_commands(bot, message.from_user.id)
    await state.clear()


@router.message(StateFilter(vfs.create_application), F.text)
async def create_application(message: Message, state: FSMContext, user: User, bot: Bot):
    data = await state.get_data()

    vacancy = Vacancy(id=data["vacancy_id"])
    application = message.text

    await vac_commands.add_vacancy_application(user, vacancy, application)
    await message.answer(texts.save_application)

    await state.clear()

    creator_id = await vac_commands.get_creator_id(vacancy)
    data_list = [user.tg_id, user.fullname, application]
    await bot.send_message(chat_id=creator_id,
                           text=await vac_commands.application_notification_text(vacancy))
    await bot.send_message(chat_id=creator_id,
                           text=await vac_commands.application_to_text(data_list))


@router.callback_query(StateFilter(default_state), F.data == "on_notification")
async def callback_turn_on_user_notification(callback: CallbackQuery, user: User):
    await vac_notification.turn_on_user_notification(user=user)
    text = f"{callback.message.text}\n\n—————\nДа, присылать уведомления 🔔"
    await callback.message.edit_text(text)
    await callback.message.answer("✅ Уведомления успешно включены!\n\n"
                                  "🔰 Мы обязательно сообщим Вам когда появится новая вакансия! :)")
    markup = inkb_verified_users if await redis_commands.check_verification(user) else inkb_not_verified_users
    await callback.message.answer(text=texts.main_page, reply_markup=markup)


@router.callback_query(StateFilter(default_state), F.data == "off_notification")
async def callback_turn_off_user_notification(callback: CallbackQuery, user: User):
    await vac_notification.turn_on_user_notification(user=user)
    text = f"{callback.message.text}\n\n—————\nНет, не нужно 🔕"
    await callback.message.edit_text(text)
    await callback.message.answer("⛔️ Уведомления не были включены!\n\n"
                                  "🔰 Вы не узнаете когда появится новая вакансия :(")
    markup = inkb_verified_users if await redis_commands.check_verification(user) else inkb_not_verified_users
    await callback.message.answer(text=texts.main_page, reply_markup=markup)


@router.callback_query(StateFilter(default_state), F.data == "redisplay")
async def callback_turn_off_user_notification(callback: CallbackQuery, user: User):
    text = f"{callback.message.text}\n\n—————\nПоcмотреть вакансии заново 🔄"
    await callback.message.edit_text(text)
    await redis_commands.user_del_history(user)

    vacancy_text, photo_data, vacancy_id = await vac_commands.get_not_viewed(user=user)
    photo = BufferedInputFile(photo_data, filename="")

    vacancy = Vacancy(id=vacancy_id, text=vacancy_text)

    if vacancy.id == -1:
        await callback.answer()
        return await callback.message.answer(texts.no_vacancies_msg, reply_markup=inkb_no_more_vacancies)

    await callback.message.answer_photo(photo=photo,
                                        caption=vacancy.text,
                                        reply_markup=await create_inkb_for_employ(id=vacancy.id,
                                                                                  is_next=True,
                                                                                  btn_like_nlike="like",
                                                                                  btn_more_less="more"))

    await redis_commands.user_add_history(user=user,
                                          vacancy=vacancy)
    await callback.answer()


@router.callback_query(StateFilter(default_state), F.data == "back_later")
async def callback_turn_off_user_notification(callback: CallbackQuery):
    text = f"{callback.message.text}\n\n—————\nВернусь позже 🔜"
    await callback.message.edit_text(text)
    await callback.message.answer(texts.ok_bro_msg)
