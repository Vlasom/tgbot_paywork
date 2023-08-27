from typing import Any, Callable, Dict, Awaitable

from aiogram import BaseMiddleware
from aiogram.dispatcher.flags import get_flag
from aiogram.types import Message, CallbackQuery
from aiogram.utils.chat_action import ChatActionSender


class CallbackQuerryChatActionMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
            event: CallbackQuery,
            data: Dict[str, Any]
    ) -> Any:
        chat_action = get_flag(data, "chat_action") or "typing"
        if not isinstance(event, CallbackQuery):
            return await handler(event, data)
        async with ChatActionSender.typing(chat_id=event.message.chat.id):
            return await handler(event, data)
