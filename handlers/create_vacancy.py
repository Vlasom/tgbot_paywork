from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from fsm.statesform import StapesForm as sf
from assets import texts


async def sent_employer(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(texts.fill_employer)
    await state.set_state(sf.fill_employer)


async def sent_job(message: Message, state: FSMContext):
    await message.answer(texts.fill_job)
    await state.update_data(employer=message.text)
    await state.set_state(sf.fill_job)


async def sent_salary(message: Message, state: FSMContext):
    await message.answer(texts.fill_salary)
    await state.update_data(job=message.text)
    await state.set_state(sf.fill_salary)


async def sent_minage(message: Message, state: FSMContext):
    await message.answer(texts.fill_minage)
    await state.update_data(salary=message.text)
    await state.set_state(sf.fill_minage)


async def sent_minexp(message: Message, state: FSMContext):
    await message.answer(texts.fill_minexp)
    await state.update_data(minage=message.text)
    await state.set_state(sf.fill_minexp)


async def sent_date(message: Message, state: FSMContext):
    await message.answer(texts.fill_date)
    await state.update_data(minexp=message.text)
    await state.set_state(sf.fill_date)


async def sent_short_dsp(message: Message, state: FSMContext):
    await message.answer(texts.fill_short_dsp)
    await state.update_data(date=message.text)
    await state.set_state(sf.fill_short_dsp)


async def sent_long_dsp(message: Message, state: FSMContext):
    await message.answer(texts.fill_long_dsp)
    await state.update_data(short_dsp=message.text)
    await state.set_state(sf.fill_long_dsp)


async def save_vacancy(message: Message, state: FSMContext):
    await message.answer(texts.save_vacancy)
    await state.update_data(long_dsp=message.text)
    # сохранение данных и что-то ещё
    await state.clear()
