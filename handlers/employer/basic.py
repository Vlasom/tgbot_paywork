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


@router.callback_query(StateFilter(default_state), F.data.startswith("contact"))
async def callback_create_application(callback: CallbackQuery, state: FSMContext, user: User):
    vacancy = Vacancy(id=int(callback.data.split("_")[1]))

    if not await vac_commands.check_vacancy_application(user, vacancy):
        await state.update_data(vacancy_id=vacancy.id)
        await state.set_state(sf.create_application)
        await callback.message.answer(texts.creating_vacancy_application)
    else:
        await callback.message.answer(texts.not_save_application)
    await callback.answer()


@router.callback_query(StateFilter(default_state), F.data.startswith("my_edit"))
async def callback_my_edit(callback: CallbackQuery, state: FSMContext, user: User):
    vacancy = Vacancy(id=int(callback.data.split("_")[2]))
    btn_more_less = callback.message.reply_markup.inline_keyboard[2][0].callback_data.split("_")[1]
    await callback.message.edit_reply_markup(reply_markup=await create_inkb_for_editing(id=vacancy.id,
                                                                                        btn_more_less=btn_more_less))
