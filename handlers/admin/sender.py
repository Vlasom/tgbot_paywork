from aiogram.types import CallbackQuery, Message
from aiogram.filters import StateFilter
from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext

from keyboards.inline_keyboards import *
from filters.is_admin import IsAdmin

from classes import vac_notification
from classes.Notifications import NotificationsSender
from classes.Statesform import SenderFormSteps as sfs
from classes.Users import User

import asyncio

router = Router()
router.callback_query.filter(IsAdmin())
router.message.filter(IsAdmin())


@router.callback_query(F.data == "admin_sender")
async def add_sender(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(f"{callback.message.text}\n\nРассылка")
    await asyncio.sleep(.5)
    await callback.message.answer("Выполняю, Создатель. Напишите название рассылки")
    await state.set_state(sfs.get_sender_name)
    await callback.answer()


@router.message(StateFilter(sfs.get_sender_name), F.text)
async def get_sender_name(message: Message, state: FSMContext):
    await state.update_data(sender_name=message.text)
    await message.answer("Хорошо. Напишите текст сообщения для рассылки")
    await state.set_state(sfs.get_sender_text)


@router.message(StateFilter(sfs.get_sender_text), F.text)
async def get_sender_text(message: Message, state: FSMContext):
    await state.update_data(sender_text=message.text)
    await message.answer("Принял. Хотите ли вы добавить кнопку, Создатель?", reply_markup=inkb_sender_with_without_btn)
    await state.set_state(sfs.sender_with_without_btn)


@router.callback_query(StateFilter(sfs.sender_with_without_btn), F.data == "sender_with_btn")
async def sender_with_btn(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(f"{callback.message.text}\n\nБезусловно")
    await asyncio.sleep(.5)
    await callback.message.answer("Конечно. Напишите текст для кнопки")
    await state.set_state(sfs.get_sender_btn_text)


@router.message(StateFilter(sfs.get_sender_btn_text), F.text)
async def get_sender_btn_text(message: Message, state: FSMContext):
    await state.update_data(sender_btn_text=message.text)
    await message.answer("Записал. Напишите ссылку для кнопки")
    await state.set_state(sfs.get_sender_btn_url)


@router.message(StateFilter(sfs.get_sender_btn_url), F.text)
async def get_sender_btn_url(message: Message, state: FSMContext):
    await state.update_data(sender_btn_url=message.text)
    data = await state.get_data()
    await message.answer(
        f"Сохранил. Вот сообщение для рассылки \"{data['sender_name']}\", Создатель:")

    await message.answer(text=data['sender_text'],
                         reply_markup=await create_inkb_for_sender(btn_text=data['sender_btn_text'],
                                                                   btn_url=data['sender_btn_url']))

    await message.answer("Начинаю рассылку?", reply_markup=inkb_start_cancel_sender)
    await state.set_state(sfs.confirm_sender)


@router.callback_query(StateFilter(sfs.sender_with_without_btn), F.data == "sender_without_btn")
async def sender_with_btn(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(f"{callback.message.text}\n\nЭто недопустимо")
    await asyncio.sleep(.5)
    data = await state.get_data()
    await callback.message.answer(
        f"Разумеется. Вот сообщение для рассылки \"{data['sender_name']}\", Создатель:")
    await callback.message.answer(text=data['sender_text'])
    await callback.message.answer("Начинаю рассылку?", reply_markup=inkb_start_cancel_sender)
    await state.set_state(sfs.confirm_sender)


@router.callback_query(StateFilter(sfs.confirm_sender), F.data == "start_sender")
async def start_sender(callback: CallbackQuery, state: FSMContext, user: User, bot: Bot):
    await callback.message.edit_text(f"{callback.message.text}\n\nИсполняй")
    await asyncio.sleep(.5)
    await callback.message.answer("Слушаюсь создатель.")
    data = await state.get_data()
    if data.get('sender_btn_text') and data.get("sender_btn_url"):
        markup = await create_inkb_for_sender(btn_text=data['sender_btn_text'],
                                              btn_url=data['sender_btn_url'])
    else:
        markup = None
    notif_sender = NotificationsSender(text=data['sender_text'],
                                       markup=markup,
                                       db_notification=vac_notification,
                                       notification_name=data["sender_name"],
                                       creator=user,
                                       bot=bot)

    await notif_sender.sender(is_vacancy_notification=False)
    await state.clear()


@router.callback_query(StateFilter(sfs.confirm_sender), F.data == "cancel_sender")
async def cancel_sender(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(f"{callback.message}\n\nПрервать")
    await asyncio.sleep(.5)
    await callback.message.answer("Как пожелаете, Создатель.")
    await state.clear()
