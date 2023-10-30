import asyncio

from aiogram.types import CallbackQuery
from aiogram import Router, F, Bot
from aiogram.filters import StateFilter, Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from classes.Statesform import VacancyFormSteps as vfs
from keyboards.inline_keyboards import *
from keyboards.inline_keyboards import create_inkb_for_employ

from classes import db_commands
from assets import texts
from utils.setcomands import set_cancel_edit_command, set_cancel_create_command


router = Router()
router.callback_query.filter(StateFilter(vfs.confirm_create))


async def send_preview(message: Message, state: FSMContext):
    data = await state.get_data()
    await message.answer(text=await db_commands.dict_to_text(vacancy_values=data,
                                                             type_descr="short"),
                         reply_markup=await create_inkb_for_employ(id=-1, is_next=False, btn_like_nlike="like",
                                                                   btn_more_less="more"))

    await asyncio.sleep(0.2)
    await message.answer("Выберите, что вы хотите отредактировать", reply_markup=inkb_edit_vac)
    await state.set_state(vfs.confirm_create)


@router.callback_query(F.data == 'edit_employer')
async def callback_edit_employer(callback: CallbackQuery,
                                 state: FSMContext,
                                 bot: Bot):
    await callback.message.edit_text(text=texts.fill_employer)
    await set_cancel_edit_command(bot, callback.from_user.id)
    await state.set_state(vfs.edit_employer)


@router.callback_query(F.data == 'edit_job')
async def callback_edit_job(callback: CallbackQuery,
                            state: FSMContext,
                            bot: Bot):
    await callback.message.edit_text(text=texts.fill_job)
    await set_cancel_edit_command(bot, callback.from_user.id)
    await state.set_state(vfs.edit_job)


@router.callback_query(F.data == 'edit_salary')
async def callback_edit_salary(callback: CallbackQuery,
                               state: FSMContext,
                               bot: Bot):
    await callback.message.edit_text(text=texts.fill_salary)
    await set_cancel_edit_command(bot, callback.from_user.id)
    await state.set_state(vfs.edit_salary)


@router.callback_query(F.data == 'edit_minage')
async def callback_edit_min_age(callback: CallbackQuery,
                                state: FSMContext,
                                bot: Bot):
    await callback.message.edit_text(text=texts.fill_min_age)
    await set_cancel_edit_command(bot, callback.from_user.id)
    await state.set_state(vfs.edit_min_age)


@router.callback_query(F.data == 'edit_minexp')
async def callback_edit_min_exp(callback: CallbackQuery,
                                state: FSMContext,
                                bot: Bot):
    await callback.message.edit_text(text=texts.fill_min_exp)
    await set_cancel_edit_command(bot, callback.from_user.id)
    await state.set_state(vfs.edit_min_exp)


@router.callback_query(F.data == 'edit_date')
async def callback_edit_date(callback: CallbackQuery,
                             state: FSMContext,
                             bot: Bot):
    await callback.message.edit_text(text=texts.fill_date)
    await set_cancel_edit_command(bot, callback.from_user.id)
    await state.set_state(vfs.edit_date)


@router.callback_query(F.data == 'edit_short_dsp')
async def callback_edit_short_dsp(callback: CallbackQuery,
                                  state: FSMContext,
                                  bot: Bot):
    await callback.message.edit_text(text=texts.fill_short_dsp)
    await set_cancel_edit_command(bot, callback.from_user.id)
    await state.set_state(vfs.edit_short_dsp)


@router.callback_query(F.data == 'edit_long_dsp')
async def callback_edit_long_dsp(callback: CallbackQuery,
                                 state: FSMContext,
                                 bot: Bot):
    await callback.message.edit_text(text=texts.fill_long_dsp)
    await set_cancel_edit_command(bot, callback.from_user.id)
    await state.set_state(vfs.edit_long_dsp)


@router.message(StateFilter(vfs.edit_employer, vfs.edit_job, vfs.edit_salary, vfs.edit_min_age,
                            vfs.edit_min_exp, vfs.edit_date, vfs.edit_short_dsp, vfs.edit_long_dsp),
                Command(commands=['cancel']))
async def send_job(message: Message,
                   state: FSMContext,
                   bot: Bot):
    await message.delete()
    await bot.edit_message_text(text=texts.mess12dsh,
                                reply_markup=inkb_edit_cancel_save,
                                chat_id=message.from_user.id,
                                message_id=message.message_id - 1)
    await state.set_state(vfs.confirm_create)


@router.message(StateFilter(vfs.edit_employer), F.text)
async def send_job(message: Message,
                   state: FSMContext,
                   bot: Bot):
    await state.set_state(vfs.confirm_create)

    await bot.delete_message(chat_id=message.from_user.id,
                             message_id=message.message_id - 2)
    await bot.delete_message(chat_id=message.from_user.id,
                             message_id=message.message_id - 3)

    await message.answer(text=texts.edit_employer)
    await state.update_data(employer=message.text)
    await set_cancel_create_command(bot, message.from_user.id)

    await send_preview(message=message, state=state)


@router.message(StateFilter(vfs.edit_job), F.text)
async def send_salary(message: Message,
                      state: FSMContext,
                      bot: Bot):
    await state.set_state(vfs.confirm_create)

    await bot.delete_message(chat_id=message.from_user.id,
                             message_id=message.message_id - 2)
    await bot.delete_message(chat_id=message.from_user.id,
                             message_id=message.message_id - 3)

    await message.answer(text=texts.edit_job)
    await state.update_data(work_type=message.text)
    await set_cancel_create_command(bot, message.from_user.id)

    await send_preview(message=message, state=state)


@router.message(StateFilter(vfs.edit_salary), F.text)
async def send_min_age(message: Message,
                       state: FSMContext,
                       bot: Bot):
    await state.set_state(vfs.confirm_create)

    await bot.delete_message(chat_id=message.from_user.id,
                             message_id=message.message_id - 2)
    await bot.delete_message(chat_id=message.from_user.id,
                             message_id=message.message_id - 3)

    await message.answer(text=texts.edit_salary)
    await state.update_data(salary=message.text)
    await set_cancel_create_command(bot, message.from_user.id)

    await send_preview(message=message, state=state)


@router.message(StateFilter(vfs.edit_min_age), F.text)
async def send_min_exp(message: Message,
                       state: FSMContext,
                       bot: Bot):
    await state.set_state(vfs.confirm_create)

    await bot.delete_message(chat_id=message.from_user.id,
                             message_id=message.message_id - 2)
    await bot.delete_message(chat_id=message.from_user.id,
                             message_id=message.message_id - 3)

    await message.answer(text=texts.edit_minage)
    await state.update_data(min_age=message.text)
    await set_cancel_create_command(bot, message.from_user.id)

    await send_preview(message=message, state=state)


@router.message(StateFilter(vfs.edit_min_exp), F.text)
async def send_date(message: Message,
                    state: FSMContext,
                    bot: Bot):
    await state.set_state(vfs.confirm_create)

    await bot.delete_message(chat_id=message.from_user.id,
                             message_id=message.message_id - 2)
    await bot.delete_message(chat_id=message.from_user.id,
                             message_id=message.message_id - 3)

    await message.answer(text=texts.edit_minexp)
    await state.update_data(min_exp=message.text)
    await set_cancel_create_command(bot, message.from_user.id)

    await send_preview(message=message, state=state)


@router.message(StateFilter(vfs.edit_date), F.text)
async def send_short_dsp(message: Message,
                         state: FSMContext,
                         bot: Bot):
    await state.set_state(vfs.confirm_create)

    await bot.delete_message(chat_id=message.from_user.id,
                             message_id=message.message_id - 2)
    await bot.delete_message(chat_id=message.from_user.id,
                             message_id=message.message_id - 3)

    await message.answer(text=texts.edit_date)
    await state.update_data(datetime=message.text)
    await set_cancel_create_command(bot, message.from_user.id)

    await send_preview(message=message, state=state)


@router.message(StateFilter(vfs.edit_short_dsp), F.text)
async def send_long_dsp(message: Message,
                        state: FSMContext,
                        bot: Bot):
    await state.set_state(vfs.confirm_create)

    await bot.delete_message(chat_id=message.from_user.id,
                             message_id=message.message_id - 2)
    await bot.delete_message(chat_id=message.from_user.id,
                             message_id=message.message_id - 3)

    await message.answer(text=texts.edit_short_dsp)
    await state.update_data(s_dscr=message.text)
    await set_cancel_create_command(bot, message.from_user.id)

    await send_preview(message=message, state=state)


@router.message(StateFilter(vfs.edit_long_dsp), F.text)
async def confirm_vacancy(message: Message,
                          state: FSMContext,
                          bot: Bot):
    await state.set_state(vfs.confirm_create)

    await bot.delete_message(chat_id=message.from_user.id,
                             message_id=message.message_id - 2)
    await bot.delete_message(chat_id=message.from_user.id,
                             message_id=message.message_id - 3)

    await message.answer(text=texts.edit_long_dsp)
    await state.update_data(l_dscr=message.text)
    await set_cancel_create_command(bot, message.from_user.id)

    await send_preview(message=message, state=state)
