from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from fsm.statesform import StapesForm as sf
from assets import texts
from aiogram import Router, F, Bot
from aiogram.filters import Text, StateFilter

from methods import send_preview

router = Router()

router.callback_query.filter(StateFilter(sf.confirm_create))


@router.callback_query(Text('edit_employer'))
async def callback_edit_employer(callback: CallbackQuery,
                                 state: FSMContext):
    await callback.answer()
    await callback.message.edit_text(text=texts.fill_employer)
    await state.set_state(sf.edit_employer)


@router.callback_query(Text('edit_job'))
async def callback_edit_job(callback: CallbackQuery,
                            state: FSMContext):
    await callback.answer()
    await callback.message.edit_text(text=texts.fill_job)
    await state.set_state(sf.edit_job)


@router.callback_query(Text('edit_salary'))
async def callback_edit_salary(callback: CallbackQuery,
                               state: FSMContext):
    await callback.message.edit_text(text=texts.fill_salary)
    await state.set_state(sf.edit_salary)


@router.callback_query(Text('edit_minage'))
async def callback_edit_min_age(callback: CallbackQuery,
                                state: FSMContext):
    await callback.answer()
    await callback.message.edit_text(text=texts.fill_min_age)
    await state.set_state(sf.edit_min_age)


@router.callback_query(Text('edit_minexp'))
async def callback_edit_min_exp(callback: CallbackQuery,
                                state: FSMContext):
    await callback.answer()
    await callback.message.edit_text(text=texts.fill_min_exp)
    await state.set_state(sf.edit_min_exp)


@router.callback_query(Text('edit_date'))
async def callback_edit_date(callback: CallbackQuery,
                             state: FSMContext):
    await callback.answer()
    await callback.message.edit_text(text=texts.fill_date)
    await state.set_state(sf.edit_date)


@router.callback_query(Text('edit_short_dsp'))
async def callback_edit_short_dsp(callback: CallbackQuery,
                                  state: FSMContext):
    await callback.answer()
    await callback.message.edit_text(text=texts.fill_short_dsp)
    await state.set_state(sf.edit_short_dsp)


@router.callback_query(Text('edit_long_dsp'))
async def callback_edit_long_dsp(callback: CallbackQuery,
                                 state: FSMContext):
    await callback.answer()
    await callback.message.edit_text(text=texts.fill_long_dsp)
    await state.set_state(sf.edit_long_dsp)


@router.message(StateFilter(sf.edit_employer), F.text)
async def send_job(message: Message,
                   state: FSMContext,
                   bot: Bot):
    await state.set_state(sf.confirm_create)

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
