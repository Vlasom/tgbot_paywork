import asyncio
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from assets import texts
from fsm.statesform import StapesForm as sf
from keyboard.inline_keyboards import *
from methods import row_to_text


async def sent_after_edit_preview(message: Message, state: FSMContext):
    data = await state.get_data()

    await message.answer(row_to_text(data, type_descr="short"), reply_markup=inkb_contact_like_more,
                         parse_mode="MarkdownV2")

    # сохранение данных и что-то ещё
    await asyncio.sleep(0.5)
    await message.answer("Выберите, что вы хотите отредактировать", reply_markup=inkb_edit_vac)
    await state.set_state(sf.confirm_create)
