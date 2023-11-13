from aiogram.filters import BaseFilter
from aiogram.types import Message
from config import config


class IsAdmin(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in config.bot.admin_ids
