from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from typing import Callable, Dict, Any, Awaitable
from classes.Users import User


class UserMiddleware(BaseMiddleware):

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message | CallbackQuery,
            data: Dict[str, Any]
    ) -> Any:
        data["user"]: User = User(tg_id=event.from_user.id,
                                  username=event.from_user.username,
                                  fullname=event.from_user.full_name)
        return await handler(event, data)
