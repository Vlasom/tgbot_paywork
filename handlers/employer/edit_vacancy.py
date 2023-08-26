import asyncio

from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from fsm.statesform import StapesForm as sf
from assets import texts
from aiogram import Router, Bot, F
from aiogram.filters import Command, Text, StateFilter

from keyboard.inline_keyboards import *
from keyboard.keyboards import *

router = Router()

router.callback_query.filter(StateFilter(sf.confirm_create))


@router.callback_query(Text('stop_edit'))
async def callback_edit_employer(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(texts.confirm_vacancy)
    data = await state.get_data()

    await callback.message.answer(texts.confirm_vacancy_txt(data, type_descr="short"),
                                  reply_markup=inkb_contact_like_more,
                                  parse_mode="MarkdownV2")

    # сохранение данных и что-то ещё
    await asyncio.sleep(0.7)
    await callback.message.answer(texts.mess12dsh, reply_markup=inkb_edit_cancel_save)
    await state.set_state(sf.confirm_create)


@router.callback_query(Text('edit_employer'))
async def callback_edit_employer(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_text(texts.fill_employer)
    await state.set_state(sf.edit_employer)


@router.callback_query(Text('edit_job'))
async def callback_edit_job(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_text(texts.fill_job)
    await state.set_state(sf.edit_job)


@router.callback_query(Text('edit_salary'))
async def callback_edit_salary(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(texts.fill_salary)
    await state.set_state(sf.edit_salary)


@router.callback_query(Text('edit_minage'))
async def callback_edit_minage(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_text(texts.fill_minage)
    await state.set_state(sf.edit_minage)


@router.callback_query(Text('edit_minexp'))
async def edit_minexp(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_text(texts.fill_minexp)
    await state.set_state(sf.edit_minexp)


@router.callback_query(Text('edit_date'))
async def edit_date(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_text(texts.fill_date)
    await state.set_state(sf.edit_date)


@router.callback_query(Text('edit_short_dsp'))
async def edit_short_dsp(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_text(texts.fill_short_dsp)
    await state.set_state(sf.edit_short_dsp)


@router.callback_query(Text('edit_long_dsp'))
async def edit_long_dsp(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_text(texts.fill_long_dsp)
    await state.set_state(sf.edit_long_dsp)


@router.message(StateFilter(sf.edit_employer), F.text)
async def sent_job(message: Message, state: FSMContext):
    await message.answer(texts.edit_employer)
    await state.update_data(employer=message.text)
    await state.set_state(sf.confirm_create)
    await message.answer("Выберите, что вы хотите отредактировать", reply_markup=inkb_process_edit_vac)


@router.message(StateFilter(sf.edit_job), F.text)
async def sent_salary(message: Message, state: FSMContext):
    await message.answer(texts.edit_job)
    await state.update_data(job=message.text)
    await state.set_state(sf.confirm_create)
    await message.answer("Выберите, что вы хотите отредактировать", reply_markup=inkb_process_edit_vac)


@router.message(StateFilter(sf.edit_salary), F.text)
async def sent_minage(message: Message, state: FSMContext):
    await message.answer(texts.edit_salary)
    await state.update_data(salary=message.text)
    await state.set_state(sf.confirm_create)
    await message.answer("Выберите, что вы хотите отредактировать", reply_markup=inkb_process_edit_vac)


@router.message(StateFilter(sf.edit_minage), F.text)
async def sent_minexp(message: Message, state: FSMContext):
    await message.answer(texts.edit_minage)
    await state.update_data(minage=message.text)
    await state.set_state(sf.confirm_create)
    await message.answer("Выберите, что вы хотите отредактировать", reply_markup=inkb_process_edit_vac)


@router.message(StateFilter(sf.edit_minexp), F.text)
async def sent_date(message: Message, state: FSMContext):
    await message.answer(texts.edit_minexp)
    await state.update_data(minexp=message.text)
    await state.set_state(sf.confirm_create)
    await message.answer("Выберите, что вы хотите отредактировать", reply_markup=inkb_process_edit_vac)


@router.message(StateFilter(sf.edit_date), F.text)
async def sent_short_dsp(message: Message, state: FSMContext):
    await message.answer(texts.edit_date)
    await state.update_data(date=message.text)
    await state.set_state(sf.confirm_create)
    await message.answer("Выберите, что вы хотите отредактировать", reply_markup=inkb_process_edit_vac)


@router.message(StateFilter(sf.edit_short_dsp), F.text)
async def sent_long_dsp(message: Message, state: FSMContext):
    await message.answer(texts.edit_short_dsp)
    await state.update_data(short_dsp=message.text)
    await state.set_state(sf.confirm_create)
    await message.answer("Выберите, что вы хотите отредактировать", reply_markup=inkb_process_edit_vac)


@router.message(StateFilter(sf.edit_long_dsp), F.text)
async def confirm_vacancy(message: Message, state: FSMContext):
    await message.answer(texts.edit_long_dsp)
    await state.update_data(long_dsp=message.text)
    await state.set_state(sf.confirm_create)
    await message.answer("Выберите, что вы хотите отредактировать", reply_markup=inkb_process_edit_vac)
