from aiogram import BaseMiddleware
from aiogram.types import Message
from typing import Callable, Dict, Any, Awaitable
from classes.Users import User
from classes import redis_commands
from assets.texts import warning_spam_msg


class AntiSpamMiddleware(BaseMiddleware):

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        user = User(tg_id=event.from_user.id)
        status = await redis_commands.check_last_action_status(user)
        if status:
            await event.answer(warning_spam_msg)
        else:
            await redis_commands.add_last_action_status(user)
            await handler(event, data)
            await redis_commands.del_last_action_status(user)

