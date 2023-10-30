from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import default_state

from classes.Statesform import VacancyFormSteps as vfs

from assets import texts
from keyboards.inline_keyboards import inkb_skip_stage_create

router = Router()
router.message.filter(~StateFilter(default_state))


@router.message(StateFilter(vfs.fill_employer,
                            vfs.fill_job,
                            vfs.fill_salary,
                            vfs.fill_min_age,
                            vfs.fill_min_exp,
                            vfs.fill_date,
                            vfs.fill_short_dsp,
                            vfs.fill_long_dsp,
                            vfs.confirm_create,
                            vfs.edit_employer,
                            vfs.edit_job,
                            vfs.edit_salary,
                            vfs.edit_min_age,
                            vfs.edit_min_exp,
                            vfs.edit_date,
                            vfs.edit_short_dsp,
                            vfs.edit_long_dsp),
                Command(commands=['start',
                                  'choice',
                                  'create_vacancy',
                                  'favorites',
                                  'my_vacancies',
                                  'main_page',
                                  'help'
                                  ]))
async def command_in_creating_vacancy(message: Message, state: FSMContext):
    await message.answer(texts.command_in_creating_vacancy)
    state_now = await state.get_state()
    if state_now == vfs.fill_employer:
        await message.answer(texts.fill_employer)
    if state_now == vfs.fill_job:
        await message.answer(texts.fill_job)
    if state_now == vfs.fill_salary:
        await message.answer(texts.fill_salary)
    if state_now == vfs.fill_min_age:
        await message.answer(texts.fill_min_age, reply_markup=inkb_skip_stage_create)
    if state_now == vfs.fill_min_exp:
        await message.answer(texts.fill_min_exp, reply_markup=inkb_skip_stage_create)
    if state_now == vfs.fill_short_dsp:
        await message.answer(texts.fill_date)
    if state_now == vfs.fill_long_dsp:
        await message.answer(texts.fill_short_dsp)


@router.message(StateFilter(vfs.create_application),
                Command(commands=['start',
                                  'choice',
                                  'create_vacancy',
                                  'favorites',
                                  'my_vacancies',
                                  'main_page',
                                  'help'
                                  ]))
async def command_in_creating_application(message: Message):
    await message.answer(texts.command_in_creating_application)


@router.callback_query(StateFilter(vfs.fill_employer,
                                   vfs.fill_job,
                                   vfs.fill_salary,
                                   vfs.fill_min_age,
                                   vfs.fill_min_exp,
                                   vfs.fill_date,
                                   vfs.fill_short_dsp,
                                   vfs.fill_long_dsp,
                                   vfs.confirm_create,
                                   vfs.edit_employer,
                                   vfs.edit_job,
                                   vfs.edit_salary,
                                   vfs.edit_min_age,
                                   vfs.edit_min_exp,
                                   vfs.edit_date,
                                   vfs.edit_short_dsp,
                                   vfs.edit_long_dsp))
async def callback_in_creating_vacancy(callback: CallbackQuery):
    await callback.answer(texts.callback_in_creating_vacancy)


@router.callback_query(StateFilter(vfs.create_application))
async def callback_in_creating_application(callback: CallbackQuery):
    await callback.answer(texts.callback_in_creating_application)
