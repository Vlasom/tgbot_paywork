from aiogram.types import CallbackQuery, Message
from aiogram.filters import Text, StateFilter
from aiogram.fsm.state import default_state
from aiogram import Router, F
from aiogram.fsm.context import FSMContext

from keyboards.inline_keyboards import *

from assets import texts
from classes import *

from fsm.statesform import StapesForm as sf


router = Router()




# @router.callback_query(StateFilter(default_state), F)
# async def callback_edit_employer(callback: CallbackQuery,
#                                  state: FSMContext):
#     fsm_state = 0
#     text = ""
#     if








"""


@router.message(StateFilter(sf.edit_employer), F.text)
async def send_job(message: Message,
                   state: FSMContext,
                   bot: Bot):

    await bot.delete_message(chat_id=message.from_user.id,
                             message_id=message.message_id - 2)
    await bot.delete_message(chat_id=message.from_user.id,
                             message_id=message.message_id - 3)

    await message.answer(text=texts.edit_employer)
    await state.update_data(employer=message.text)

    await send_preview(message=message, state=state)


@router.message(StateFilter(sf.edit_job), F.text)
async def send_salary(message: Message,
                      state: FSMContext,
                      bot: Bot):
    await state.set_state(sf.confirm_create)

    await bot.delete_message(chat_id=message.from_user.id,
                             message_id=message.message_id - 2)
    await bot.delete_message(chat_id=message.from_user.id,
                             message_id=message.message_id - 3)

    await message.answer(text=texts.edit_job)
    await state.update_data(work_type=message.text)

    await send_preview(message=message, state=state)


@router.message(StateFilter(sf.edit_salary), F.text)
async def send_min_age(message: Message,
                       state: FSMContext,
                       bot: Bot):
    await state.set_state(sf.confirm_create)

    await bot.delete_message(chat_id=message.from_user.id,
                             message_id=message.message_id - 2)
    await bot.delete_message(chat_id=message.from_user.id,
                             message_id=message.message_id - 3)

    await message.answer(text=texts.edit_salary)
    await state.update_data(salary=message.text)

    await send_preview(message=message, state=state)


@router.message(StateFilter(sf.edit_min_age), F.text)
async def send_min_exp(message: Message,
                       state: FSMContext,
                       bot: Bot):
    await state.set_state(sf.confirm_create)

    await bot.delete_message(chat_id=message.from_user.id,
                             message_id=message.message_id - 2)
    await bot.delete_message(chat_id=message.from_user.id,
                             message_id=message.message_id - 3)

    await message.answer(text=texts.edit_minage)
    await state.update_data(min_age=message.text)

    await send_preview(message=message, state=state)


@router.message(StateFilter(sf.edit_min_exp), F.text)
async def send_date(message: Message,
                    state: FSMContext,
                    bot: Bot):
    await state.set_state(sf.confirm_create)

    await bot.delete_message(chat_id=message.from_user.id,
                             message_id=message.message_id - 2)
    await bot.delete_message(chat_id=message.from_user.id,
                             message_id=message.message_id - 3)

    await message.answer(text=texts.edit_minexp)
    await state.update_data(min_exp=message.text)

    await send_preview(message=message, state=state)


@router.message(StateFilter(sf.edit_date), F.text)
async def send_short_dsp(message: Message,
                         state: FSMContext,
                         bot: Bot):
    await state.set_state(sf.confirm_create)

    await bot.delete_message(chat_id=message.from_user.id,
                             message_id=message.message_id - 2)
    await bot.delete_message(chat_id=message.from_user.id,
                             message_id=message.message_id - 3)

    await message.answer(text=texts.edit_date)
    await state.update_data(datetime=message.text)

    await send_preview(message=message, state=state)


@router.message(StateFilter(sf.edit_short_dsp), F.text)
async def send_long_dsp(message: Message,
                        state: FSMContext,
                        bot: Bot):
    await state.set_state(sf.confirm_create)

    await bot.delete_message(chat_id=message.from_user.id,
                             message_id=message.message_id - 2)
    await bot.delete_message(chat_id=message.from_user.id,
                             message_id=message.message_id - 3)

    await message.answer(text=texts.edit_short_dsp)
    await state.update_data(s_dscr=message.text)

    await send_preview(message=message, state=state)


@router.message(StateFilter(sf.edit_long_dsp), F.text)
async def confirm_vacancy(message: Message,
                          state: FSMContext,
                          bot: Bot):
    await state.set_state(sf.confirm_create)

    await bot.delete_message(chat_id=message.from_user.id,
                             message_id=message.message_id - 2)
    await bot.delete_message(chat_id=message.from_user.id,
                             message_id=message.message_id - 3)

    await message.answer(text=texts.edit_long_dsp)
    await state.update_data(l_dscr=message.text)
    await send_preview(message=message,
                       state=state)
    """