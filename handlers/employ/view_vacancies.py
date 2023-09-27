from aiogram.types import CallbackQuery, Message
from aiogram.filters import Text, StateFilter
from aiogram.fsm.state import default_state
from aiogram import Router, F
from aiogram.fsm.context import FSMContext

from methods.redis import users_history
from keyboards.inline_keyboards import *

from methods.sqlite.vacancies import get_vacancies_to_text, add_like_vacancy, del_like_vacancy, vacancy_to_text, \
    add_vacancy_application, check_vacancy_application
from methods.sqlite.users import on_nitifi_in_db, off_nitifi_in_db

from assets import texts

from fsm.statesform import StapesForm as sf

router = Router()


@router.callback_query(Text("employ"))
async def callback_employ_vacancies(callback: CallbackQuery):
    await callback.message.answer(texts.employ_warn_info)

    vacancy_text, vacancy_id = await get_vacancies_to_text(user_tg_id=callback.from_user.id)
    if vacancy_id == -1:
        await callback.answer()
        return await callback.message.answer(vacancy_text, reply_markup=inkb_on_off_notifi)

    await callback.message.answer(text=vacancy_text,
                                  reply_markup=await create_inkb(id=vacancy_id,
                                                                 is_next=True,
                                                                 btn_like_nlike="like",
                                                                 btn_more_less="more"))

    await users_history.add_history(user_tg_id=callback.from_user.id,
                                    vacancy_id=vacancy_id)
    await callback.answer()


@router.callback_query(F.data.startswith("next"))
async def callback_next_vacancy(callback: CallbackQuery):
    vacancy_text, vacancy_id = await get_vacancies_to_text(user_tg_id=callback.from_user.id)

    btn_more_less = callback.message.reply_markup.inline_keyboard[0][1].callback_data[:4]
    btn_like_nlike = callback.message.reply_markup.inline_keyboard[0][2].callback_data[:4]

    past_vacancy_id = callback.data.split("_")[1]

    await callback.message.edit_reply_markup(reply_markup=await create_inkb(id=past_vacancy_id,
                                                                            is_next=False,
                                                                            btn_like_nlike=btn_like_nlike,
                                                                            btn_more_less=btn_more_less))
    if vacancy_id == -1:
        return await callback.message.answer(vacancy_text, reply_markup=inkb_on_off_notifi)

    await callback.message.answer(text=vacancy_text,
                                  reply_markup=await create_inkb(id=vacancy_id,
                                                                 is_next=True,
                                                                 btn_like_nlike="like",
                                                                 btn_more_less="more"))

    await users_history.add_history(user_tg_id=callback.from_user.id,
                                    vacancy_id=vacancy_id)


@router.callback_query(StateFilter(default_state), F.data.startswith("more"))
async def callback_more_vacancy(callback: CallbackQuery):
    if callback.message.reply_markup.inline_keyboard[1][0].text.startswith("След"):
        btn_like_nlike = callback.message.reply_markup.inline_keyboard[0][2].callback_data[:4]
        is_next = True

    else:
        btn_like_nlike = callback.message.reply_markup.inline_keyboard[0][1].callback_data[:4]
        is_next = False

    vacancy_id = int(callback.data.split("_")[1])

    text = await vacancy_to_text(vacancy=vacancy_id,
                                 type_descr="long")

    await callback.message.edit_text(text=text,
                                     reply_markup=await create_inkb(id=vacancy_id,
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

    vacancy_id = int(callback.data.split("_")[1])

    text = await vacancy_to_text(vacancy=vacancy_id,
                                 type_descr="short")

    await callback.message.edit_text(text=text, reply_markup=await create_inkb(id=vacancy_id,
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

    vacancy_id = callback.data.split("_")[1]

    await add_like_vacancy(user_tg_id=callback.from_user.id,
                           vacancy_id=vacancy_id)

    await callback.answer(texts.like_notification)

    await callback.message.edit_reply_markup(reply_markup=await create_inkb(id=vacancy_id,
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

    vacancy_id = callback.data.split("_")[1]

    await del_like_vacancy(user_tg_id=callback.from_user.id)

    await callback.answer(texts.nlike_notification)
    await callback.message.edit_reply_markup(reply_markup=await create_inkb(id=vacancy_id,
                                                                            is_next=is_next,
                                                                            btn_like_nlike="like",
                                                                            btn_more_less=btn_less_more))


@router.callback_query(StateFilter(default_state), F.data.startswith("created_more"))
async def callback_more_vacancy(callback: CallbackQuery):
    vacancy_id = int(callback.data.split("_")[2])

    text = await vacancy_to_text(vacancy=vacancy_id,
                                 type_descr="long")

    await callback.message.edit_text(text=text,
                                     reply_markup=await create_inkb_for_employer(id=vacancy_id,
                                                                                 btn_more_less="less"))


@router.callback_query(StateFilter(default_state), F.data.startswith("created_less"))
async def callback_less_vacancy(callback: CallbackQuery):
    vacancy_id = int(callback.data.split("_")[2])

    text = await vacancy_to_text(vacancy=vacancy_id,
                                 type_descr="short")

    await callback.message.edit_text(text=text, reply_markup=await create_inkb_for_employer(id=vacancy_id,
                                                                                            btn_more_less="more"))


@router.callback_query(StateFilter(default_state), F.data.startswith("contact"))
async def callback_create_application(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    vacancy_id = int(callback.data.split("_")[1])

    if not await check_vacancy_application(user_id, vacancy_id):
        await state.update_data(vacancy_id=vacancy_id)
        await state.set_state(sf.create_application)
        await callback.message.answer(texts.creating_vacancy_application)
    else:
        await callback.message.answer(texts.not_save_application)
    await callback.answer()


@router.message(StateFilter(sf.create_application), F.text)
async def create_application(message: Message, state: FSMContext):
    data = await state.get_data()

    user_id = message.from_user.id
    vacancy_id = data["vacancy_id"]
    apllication = message.text

    await add_vacancy_application(user_id, vacancy_id, apllication)
    await message.answer(texts.save_application)

    await state.clear()


@router.callback_query(StateFilter(default_state), Text("on_notification"))
async def on_notification(callback: CallbackQuery):
    await on_nitifi_in_db(callback.from_user.id)
    await callback.answer("Уведомления включены")


@router.callback_query(StateFilter(default_state), Text("off_notification"))
async def off_notification(callback: CallbackQuery):
    await off_nitifi_in_db(callback.from_user.id)
    await callback.answer("Уведомления выключены")
