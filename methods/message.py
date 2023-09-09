import asyncio
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from fsm.statesform import StapesForm as sf
from keyboards.inline_keyboards import *
from methods import dict_to_text
from keyboards.inline_keyboards import create_inkb


async def sent_after_edit_preview(message: Message, state: FSMContext):
    data = await state.get_data()

    await message.answer(await dict_to_text(data, type_descr="short"), reply_markup=await create_inkb(id=-1, isnext=False, like_nlike="like", more_less="more"),
                         parse_mode="MarkdownV2")

    # сохранение данных и что-то ещё
    await asyncio.sleep(0.5)
    await message.answer("Выберите, что вы хотите отредактировать", reply_markup=inkb_edit_vac)
    await state.set_state(sf.confirm_create)
