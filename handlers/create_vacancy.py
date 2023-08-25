from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from fsm.statesform import StapesForm as sf
from assets import texts
from aiogram import Router, Bot, F
from aiogram.filters import Command, Text, StateFilter
from keyboard.inline_keybords import *

router = Router()


@router.message(~StateFilter(default_state), Command(commands=['cancel']))
async def cancel_create(message: Message):
    await message.answer("Вы точно хотите отменить создание вакансии?", reply_markup=yes_no_kb)


@router.callback_query(Text("canceling"))
async def canceling(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Созание вакансии отменено")
    await state.clear()


@router.callback_query(Text("continue"))
async def canceling(callback: CallbackQuery, bot: Bot):
    await callback.message.delete()
    # await callback.message.edit_text("Созание Вакансии отменено")
    await bot.delete_message(callback.from_user.id, callback.message.message_id - 1)


@router.callback_query(Text("employer"))
async def sent_employer(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(texts.start_create)
    await callback.message.answer(texts.fill_employer)
    await state.set_state(sf.fill_employer)


@router.message(StateFilter(sf.fill_employer), F.text)
async def sent_job(message: Message, state: FSMContext):
    await message.answer(texts.fill_job)
    await state.update_data(employer=message.text)
    await state.set_state(sf.fill_job)


@router.message(StateFilter(sf.fill_job), F.text)
async def sent_salary(message: Message, state: FSMContext):
    await message.answer(texts.fill_salary)
    await state.update_data(job=message.text)
    await state.set_state(sf.fill_salary)


@router.message(StateFilter(sf.fill_salary), F.text)
async def sent_minage(message: Message, state: FSMContext):
    await message.answer(texts.fill_minage)
    await state.update_data(salary=message.text)
    await state.set_state(sf.fill_minage)


@router.message(StateFilter(sf.fill_minage), F.text)
async def sent_minexp(message: Message, state: FSMContext):
    await message.answer(texts.fill_minexp)
    await state.update_data(minage=message.text)
    await state.set_state(sf.fill_minexp)


@router.message(StateFilter(sf.fill_minexp), F.text)
async def sent_date(message: Message, state: FSMContext):
    await message.answer(texts.fill_date)
    await state.update_data(minexp=message.text)
    await state.set_state(sf.fill_date)


@router.message(StateFilter(sf.fill_date), F.text)
async def sent_short_dsp(message: Message, state: FSMContext):
    await message.answer(texts.fill_short_dsp)
    await state.update_data(date=message.text)
    await state.set_state(sf.fill_short_dsp)


@router.message(StateFilter(sf.fill_short_dsp), F.text)
async def sent_long_dsp(message: Message, state: FSMContext):
    await message.answer(texts.fill_long_dsp)
    await state.update_data(short_dsp=message.text)
    await state.set_state(sf.fill_long_dsp)


@router.message(StateFilter(sf.fill_long_dsp), F.text)
async def confirm_vacancy(message: Message, state: FSMContext):
    await message.answer(texts.confirm_vacancy)
    await state.update_data(long_dsp=message.text)
    data = await state.get_data()

    await message.answer(f"*{data.get('employer')}*\n"
                         f"{data.get('job')}\n"
                         f"{data.get('salary')}\n"
                         f"Минимальный возраст \- {data.get('minage')}\n"
                         f"Минимальный опыт работы \- {data.get('minexp')}\n"
                         f"Время \- {data.get('date')}\n"
                         "\n"
                         f"{data.get('short_dsp')}",
                         reply_markup=s_vacancy_kb)  # Сделать функцию которая будет формировать текст сообщений

    # сохранение данных и что-то ещё
    await state.set_state(sf.confirm_create)


@router.callback_query(StateFilter(sf.confirm_create), Text("more"))
async def more_vacancy(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await callback.message.edit_text(f"*{data.get('employer')}*\n"
                                     f"{data.get('job')}\n"
                                     f"{data.get('salary')}\n"
                                     f"Минимальный возраст \- {data.get('minage')}\n"
                                     f"Минимальный опыт работы \- {data.get('minexp')}\n"
                                     f"Время \- {data.get('date')}\n"
                                     "\n"
                                     f"{data.get('long_dsp')}",
                                     reply_markup=l_vacancy_kb)


@router.callback_query(StateFilter(sf.confirm_create), Text("less"))
async def more_vacancy(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await callback.message.edit_text(f"*{data.get('employer')}*\n"
                                     f"{data.get('job')}\n"
                                     f"{data.get('salary')}\n"
                                     f"Минимальный возраст \- {data.get('minage')}\n"
                                     f"Минимальный опыт работы \- {data.get('minexp')}\n"
                                     f"Время \- {data.get('date')}\n"
                                     "\n"
                                     f"{data.get('short_dsp')}",
                                     reply_markup=s_vacancy_kb)
