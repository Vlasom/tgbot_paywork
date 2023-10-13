from aiogram.types import CallbackQuery, Message
from aiogram.filters import StateFilter
from aiogram.fsm.state import default_state
from aiogram import Router, F
from aiogram.fsm.context import FSMContext

from keyboards.inline_keyboards import *

from assets import texts
from classes import *

from fsm.statesform import StapesForm as sf

router = Router()


@router.callback_query(F.data == "employ")
async def callback_employ_vacancies(callback: CallbackQuery, user: User):
    await callback.message.answer(texts.employ_warn_info)

    vacancy_text, vacancy_id = await vac_commands.get_not_viewed(user=user)

    vacancy = Vacancy(id=vacancy_id, text=vacancy_text)

    if vacancy.id == -1:
        await callback.answer()
        return await callback.message.answer(texts.no_vacancies_notification, reply_markup=inkb_on_off_notifi)

    await callback.message.answer(text=vacancy.text,
                                  reply_markup=await create_inkb(id=vacancy.id,
                                                                 is_next=True,
                                                                 btn_like_nlike="like",
                                                                 btn_more_less="more"))

    await redis_commands.user_add_history(user=user,
                                          vacancy=vacancy)
    await callback.answer()


@router.callback_query(F.data.startswith("next"))
async def callback_next_vacancy(callback: CallbackQuery, user: User):
    vacancy_text, vacancy_id = await vac_commands.get_not_viewed(user=user)
    vacancy = Vacancy(id=vacancy_id, text=vacancy_text)

    btn_more_less = callback.message.reply_markup.inline_keyboard[0][1].callback_data[:4]
    btn_like_nlike = callback.message.reply_markup.inline_keyboard[0][2].callback_data[:4]

    past_vacancy_id = callback.data.split("_")[1]

    await callback.message.edit_reply_markup(reply_markup=await create_inkb(id=past_vacancy_id,
                                                                            is_next=False,
                                                                            btn_like_nlike=btn_like_nlike,
                                                                            btn_more_less=btn_more_less))
    if vacancy.id == -1:
        return await callback.message.answer(texts.no_vacancies_notification, reply_markup=inkb_on_off_notifi)

    await callback.message.answer(text=vacancy.text,
                                  reply_markup=await create_inkb(id=vacancy.id,
                                                                 is_next=True,
                                                                 btn_like_nlike="like",
                                                                 btn_more_less="more"))
    vacancy = Vacancy(id=vacancy_id)

    await redis_commands.user_add_history(user=user, vacancy=vacancy)


@router.callback_query(StateFilter(default_state), F.data.startswith("more"))
async def callback_more_vacancy(callback: CallbackQuery):
    if callback.message.reply_markup.inline_keyboard[1][0].text.startswith("След"):
        btn_like_nlike = callback.message.reply_markup.inline_keyboard[0][2].callback_data[:4]
        is_next = True

    else:
        btn_like_nlike = callback.message.reply_markup.inline_keyboard[0][1].callback_data[:4]
        is_next = False

    vacancy = Vacancy(id=int(callback.data.split("_")[1]))

    text = await vac_commands.to_text(vacancy=vacancy,
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

    text = await vac_commands.to_text(vacancy=vacancy,
                                      type_descr="short")

    await callback.message.edit_text(text=text, reply_markup=await create_inkb(id=vacancy.id,
                                                                               is_next=is_next,
                                                                               btn_like_nlike=btn_like_nlike,
                                                                               btn_more_less="more"))


@router.callback_query(StateFilter(default_state), F.data.startswith("like"))
async def callback_like_vacancy(callback: CallbackQuery, user: User):
    if callback.message.reply_markup.inline_keyboard[1][0].text.startswith("След"):
        btn_less_more = callback.message.reply_markup.inline_keyboard[0][1].callback_data[:4]
        is_next = True

    else:
        btn_less_more = callback.message.reply_markup.inline_keyboard[1][0].callback_data[:4]
        is_next = False

    vacancy = Vacancy(id=int(callback.data.split("_")[1]))

    await vac_commands.add_to_userlikes(user=user, vacancy=vacancy)

    await callback.answer(texts.like_notification)

    await callback.message.edit_reply_markup(reply_markup=await create_inkb(id=vacancy.id,
                                                                            is_next=is_next,
                                                                            btn_like_nlike="nlike",
                                                                            btn_more_less=btn_less_more))


@router.callback_query(StateFilter(default_state), F.data.startswith("nlike"))
async def callback_like_vacancy(callback: CallbackQuery, user: User):
    if callback.message.reply_markup.inline_keyboard[1][0].text.startswith("След"):
        btn_less_more = callback.message.reply_markup.inline_keyboard[0][1].callback_data[:4]
        is_next = True

    else:
        btn_less_more = callback.message.reply_markup.inline_keyboard[1][0].callback_data[:4]
        is_next = False

    vacancy = Vacancy(id=int(callback.data.split("_")[1]))
    await vac_commands.del_from_userlikes(user=user, vacancy=vacancy)

    await callback.answer(texts.nlike_notification)
    await callback.message.edit_reply_markup(reply_markup=await create_inkb(id=vacancy.id,
                                                                            is_next=is_next,
                                                                            btn_like_nlike="like",
                                                                            btn_more_less=btn_less_more))


@router.message(StateFilter(sf.create_application), F.text)
async def create_application(message: Message, state: FSMContext, user: User):
    data = await state.get_data()

    vacancy = Vacancy(id=data["vacancy_id"])
    apllication = message.text

    await vac_commands.add_vacancy_application(user, vacancy, apllication)
    await message.answer(texts.save_application)

    await state.clear()


@router.callback_query(StateFilter(default_state), F.data.startswith("applications"))
async def show_applications(callback: CallbackQuery):
    vacancy = Vacancy(id=int(callback.data.split("_")[1]))
    await callback.message.answer(f"Отклики на вакансию №{vacancy.id}")
    applications = await vac_commands.get_applications(vacancy)
    if applications:
        for application in applications:
            text = await vac_commands.application_to_text(application)
            await callback.message.answer(text)
    else:
        await callback.message.answer(texts.no_application)
    await callback.answer()


@router.callback_query(StateFilter(default_state), F.data == "on_notification")
async def callback_turn_on_user_notification(callback: CallbackQuery, user: User):
    await vac_notification.turn_on_user_notification(user=user)
    await callback.answer("Уведомления включены")


@router.callback_query(StateFilter(default_state), F.data == "off_notification")
async def callback_turn_off_user_notification(callback: CallbackQuery, user: User):
    await vac_notification.turn_off_user_notification(user=user)
    await callback.answer("Уведомления выключены")
