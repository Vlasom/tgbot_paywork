from aiogram.types import CallbackQuery, BufferedInputFile
from aiogram.fsm.state import default_state
from assets import texts
from aiogram import Router, F
from aiogram.filters import StateFilter

from classes import vac_commands, User, Vacancy, db_commands, redis_commands, vac_notification
from keyboards.inline_keyboards import *
from keyboards.NotifiCallbackFactory import NotifiCallbackFactory, create_inkb_user_notifications

router = Router()
router.callback_query.filter(StateFilter(default_state))


@router.callback_query(F.data == "settings_notification")
async def settings_notification(callback: CallbackQuery, user: User):
    await callback.message.edit_text(text="Уведомления", reply_markup=await create_inkb_user_notifications(user))


@router.callback_query(NotifiCallbackFactory.filter())
async def notification_parameters(callback: CallbackQuery, callback_data: NotifiCallbackFactory, user: User):
    if callback_data.place == 2:
        if not await vac_notification.get_user_email(user=user):
            return await callback.message.answer(texts.mail_verification)

    if callback_data.status == 0:
        await vac_notification.turn_on_user_notification(place=callback_data.place, event=callback_data.event,
                                                         user=user)
        await callback.message.edit_reply_markup(reply_markup=await create_inkb_user_notifications(user))

    elif callback_data.status == 1:
        await vac_notification.turn_off_user_notification(place=callback_data.place, event=callback_data.event,
                                                          user=user)
        await callback.message.edit_reply_markup(reply_markup=await create_inkb_user_notifications(user))


@router.callback_query(F.data == "back_notifications")
async def back_notifications(callback: CallbackQuery, user: User):
    markup = inkb_verified_users if await redis_commands.check_verification(user) else inkb_not_verified_users
    await callback.message.edit_text(texts.main_page, reply_markup=markup)


@router.callback_query(F.data == "new_vacancy_notifications")
async def back_notifications(callback: CallbackQuery, user: User):
    await callback.answer("Уведомления, приходящие когда в боте создается новая вакансия.", show_alert=True)


@router.callback_query(F.data == "del_from_likes_notifications")
async def back_notifications(callback: CallbackQuery, user: User):
    await callback.answer(
        "Уведомления, приходящие когда работодатель удаляет вакансию, которая находилась у вас в избранных.", show_alert=True)


@router.callback_query(F.data == "application_answer_notifications")
async def back_notifications(callback: CallbackQuery, user: User):
    await callback.answer(
        "Уведомления, приходящие когда работодатель отклоняет или принимает ваш отклик.", show_alert=True)
