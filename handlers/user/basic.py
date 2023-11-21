from aiogram.types import CallbackQuery, Message
from aiogram.filters import StateFilter, Command
from aiogram.fsm.state import default_state
from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext

from keyboards.inline_keyboards import *

from assets import texts
from classes import *
from utils.setcomands import set_cancel_create_application_command, set_default_commands

from classes.Statesform import VacancyFormSteps as vfs

router = Router()


@router.callback_query(StateFilter(default_state), F.data.startswith("like"))
async def callback_like_vacancy(callback: CallbackQuery, user: User):
    if callback.message.reply_markup.inline_keyboard.__len__() == 3:
        is_next = True

    else:
        is_next = False

    btn_less_more = callback.message.reply_markup.inline_keyboard[1][0].callback_data[:4]

    vacancy = Vacancy(id=int(callback.data.split("_")[1]))

    await vac_commands.add_to_user_likes(user=user, vacancy=vacancy)

    await callback.answer(texts.like_notification)

    await callback.message.edit_reply_markup(reply_markup=await create_inkb_for_employ(id=vacancy.id,
                                                                                       is_next=is_next,
                                                                                       btn_like_nlike="nlike",
                                                                                       btn_more_less=btn_less_more))


@router.callback_query(StateFilter(default_state), F.data.startswith("nlike"))
async def callback_nlike_vacancy(callback: CallbackQuery, user: User):
    if callback.message.reply_markup.inline_keyboard.__len__() == 3:
        is_next = True

    else:
        is_next = False

    btn_less_more = callback.message.reply_markup.inline_keyboard[1][0].callback_data[:4]

    vacancy = Vacancy(id=int(callback.data.split("_")[1]))
    await vac_commands.del_from_user_likes(user=user, vacancy=vacancy)

    await callback.answer(texts.nlike_notification)
    await callback.message.edit_reply_markup(reply_markup=await create_inkb_for_employ(id=vacancy.id,
                                                                                       is_next=is_next,
                                                                                       btn_like_nlike="like",
                                                                                       btn_more_less=btn_less_more))


@router.callback_query(StateFilter(default_state), F.data.startswith("create_application"))
async def callback_create_application(callback: CallbackQuery, state: FSMContext, user: User, bot: Bot):
    vacancy = Vacancy(id=int(callback.data.split("_")[2]))

    if not await vac_commands.check_application(user, vacancy):
        btn_more_less = callback.message.reply_markup.inline_keyboard[1][0].callback_data.split("_")[0]
        btn_like_nlike = callback.message.reply_markup.inline_keyboard[0][1].callback_data.split("_")[0]
        await callback.message.delete()
        await state.update_data(vacancy_id=vacancy.id)
        await set_cancel_create_application_command(bot, callback.from_user.id)
        await state.set_state(vfs.create_application)
        await callback.message.answer("Отклик на вакансию")
        await callback.message.send_copy(chat_id=callback.message.chat.id,
                                         reply_markup=await create_inkb_for_employ(id=vacancy.id,
                                                                                   is_next=False,
                                                                                   btn_like_nlike=btn_like_nlike,
                                                                                   btn_more_less=btn_more_less))
        await callback.message.answer(text=texts.creating_vacancy_application, reply_markup=inkb_cancel_action)
    else:
        await callback.answer(text=texts.already_save_application, show_alert=True)


@router.message(StateFilter(vfs.create_application), Command(commands=["cancel"]))
async def command_cancel_create_application(message: Message, state: FSMContext, user: User, bot: Bot):
    await message.answer(texts.cancel_create_application)
    await set_default_commands(bot, message.from_user.id)
    markup = inkb_verified_users if await redis_commands.check_verification(user) else inkb_not_verified_users
    await message.answer(texts.main_page, reply_markup=markup)
    await state.clear()


@router.callback_query(StateFilter(vfs.create_application), F.data == "cancel_action")
async def callback_cancel_create_application(callback: CallbackQuery, state: FSMContext, user: User, bot: Bot):
    await callback.message.edit_text(text=callback.message.text + "\n---\nОтменить ↩️")
    await callback.message.answer(texts.cancel_create_application)
    await set_default_commands(bot, callback.message.from_user.id)
    markup = inkb_verified_users if await redis_commands.check_verification(user) else inkb_not_verified_users
    await callback.message.answer(texts.main_page, reply_markup=markup)
    await state.clear()


@router.message(StateFilter(vfs.create_application), F.text)
async def sent_application(message: Message, state: FSMContext, user: User, bot: Bot):
    data = await state.get_data()

    vacancy = Vacancy(id=data["vacancy_id"])
    application_text = message.text

    await vac_commands.add_application(user, vacancy, application_text)

    await message.answer(texts.save_application)

    await state.clear()

    creator_id = await vac_commands.get_creator_id(vacancy)
    data_list = [user.tg_id, user.fullname, application_text]
    text = "У вас новый отклик на вакансию\n" + await vac_commands.vacancy_miniature_text(id=vacancy.id)
    await bot.send_message(chat_id=creator_id,
                           text=text)
    await bot.send_message(chat_id=creator_id,
                           text=await vac_commands.application_to_text(data_list),
                           reply_markup=await create_inkb_application(user_id=user.tg_id, vacancy_id=vacancy.id))


@router.callback_query(StateFilter(default_state), F.data == "my_applications")
async def callback_show_my_application(message: Message, user: User):
    user_applications_data = await vac_commands.get_user_applications(user)

    if user_applications_data:
        for data in user_applications_data:
            employer = data[3]
            work_type = data[4]
            text = "Отклик на вакансию\n" + await vac_commands.vacancy_miniature_text(employer=employer,
                                                                                      work_type=work_type)
            await message.answer(text=text)
            await message.answer(text=data[0] + "\n\n" + data[1],
                                 reply_markup=await create_inkb_del_applicaion(user.tg_id, data[2]))
    else:
        await message.answer(texts.no_user_application)


@router.callback_query(StateFilter(default_state), F.data.startswith("delete_application"))
async def callback_delete_application(callback: CallbackQuery, user: User):
    vacancy_id = int(callback.data.split("_")[3])
    await callback.message.edit_reply_markup(
        reply_markup=await create_inkb_confirm_del_applicaion(user.tg_id, vacancy_id))


@router.callback_query(StateFilter(default_state), F.data.startswith("back_delete_application"))
async def callback_back_delete_application(callback: CallbackQuery, user: User):
    vacancy_id = int(callback.data.split("_")[4])
    await callback.message.edit_reply_markup(reply_markup=await create_inkb_del_applicaion(user.tg_id, vacancy_id))


@router.callback_query(StateFilter(default_state), F.data.startswith("confirm_delete_application"))
async def callback_confirm_delete_application(callback: CallbackQuery, user: User):
    vacancy_id = int(callback.data.split("_")[4])
    await vac_commands.delete_application(user.tg_id, vacancy_id)

    await callback.message.edit_text("Отклик удален")


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
