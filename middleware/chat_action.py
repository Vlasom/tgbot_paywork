from typing import Any, Callable, Dict, Awaitable

from aiogram import BaseMiddleware
from aiogram.dispatcher.flags import get_flag
from aiogram.types import CallbackQuery
from aiogram.utils.chat_action import ChatActionSender


class CallbackQuerryChatActionMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
            event: CallbackQuery,
            data: Dict[str, Any]
    ) -> Any:
        only_editing_cb = get_flag(data, "only_editing")
        if not only_editing_cb:
            async with ChatActionSender.typing(chat_id=event.message.chat.id):
                return await handler(event, data)
        return await handler(event, data)
