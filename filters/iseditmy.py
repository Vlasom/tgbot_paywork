from aiogram.filters import BaseFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message


class IsEditMy(BaseFilter):
    async def __call__(self, message: Message, state: FSMContext):
        data = await state.get_data()
        return "id" in data.keys()
