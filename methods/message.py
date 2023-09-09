import asyncio
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from fsm.statesform import StapesForm as sf
from keyboards.inline_keyboards import *
from methods.sqlite.vacancies import dict_to_text
from keyboards.inline_keyboards import create_inkb


async def send_preview(message: Message, state: FSMContext):

    data = await state.get_data()
    await message.answer(text=await dict_to_text(vacancy_values=data,
                                                 type_descr="short"),
                         reply_markup=await create_inkb(id=-1,
                                                        is_next=False,
                                                        btn_like_nlike="like",
                                                        btn_more_less="more"))

    await asyncio.sleep(0.2)
    await message.answer("Выберите, что вы хотите отредактировать", reply_markup=inkb_edit_vac)
    await state.set_state(sf.confirm_create)
