from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import default_state

from fsm.statesform import StapesForm as sf

from assets import texts
from keyboards.inline_keyboards import inkb_skip_stage_create

router = Router()
router.message.filter(~StateFilter(default_state))


@router.message(StateFilter(sf.fill_employer,
                            sf.fill_job,
                            sf.fill_salary,
                            sf.fill_min_age,
                            sf.fill_min_exp,
                            sf.fill_date,
                            sf.fill_short_dsp,
                            sf.fill_long_dsp,
                            sf.confirm_create,
                            sf.edit_employer,
                            sf.edit_job,
                            sf.edit_salary,
                            sf.edit_min_age,
                            sf.edit_min_exp,
                            sf.edit_date,
                            sf.edit_short_dsp,
                            sf.edit_long_dsp),
                Command(commands=['start',
                                  'choice',
                                  'create_vacancy',
                                  'favorites',
                                  'my_vacancies',
                                  ]))
async def command_in_other_state(message: Message, state: FSMContext):
    await message.answer(texts.command_in_creating_vacancy)
    state_now = await state.get_state()
    if state_now == sf.fill_employer:
        await message.answer(texts.fill_employer)
    if state_now == sf.fill_job:
        await message.answer(texts.fill_job)
    if state_now == sf.fill_salary:
        await message.answer(texts.fill_salary)
    if state_now == sf.fill_min_age:
        await message.answer(texts.fill_min_age, reply_markup=inkb_skip_stage_create)
    if state_now == sf.fill_min_exp:
        await message.answer(texts.fill_min_exp, reply_markup=inkb_skip_stage_create)
    if state_now == sf.fill_short_dsp:
        await message.answer(texts.fill_date)
    if state_now == sf.fill_long_dsp:
        await message.answer(texts.fill_short_dsp)


@router.message(StateFilter(sf.create_application),
                Command(commands=['start',
                                  'choice',
                                  'create_vacancy',
                                  'favorites',
                                  'my_vacancies',
                                  ]))
async def command_in_other_state(message: Message):
    await message.answer(texts.command_in_creating_vacancy)
