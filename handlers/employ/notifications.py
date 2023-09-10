from methods.sqlite.users import cheak_table, create_table, delete_table, get_users_with_notification, update_status, update_active
from keyboards.inline_keyboards import create_inkb
from aiogram.exceptions import TelegramRetryAfter, TelegramForbiddenError
from aiogram import Bot
import asyncio

from aiogram.types import Message




async def send_notifications(id_vacancy_notification: int, user_tg_id, text, markup, bot: Bot):
    try:
        await bot.send_message(chat_id=user_tg_id, text=text, reply_markup=markup)

    except TelegramRetryAfter as e:
        await asyncio.sleep(e.retry_after)
        return send_notifications(id_vacancy_notification, user_tg_id, text, markup, bot)

    except TelegramForbiddenError as e:
        await update_active(user_tg_id)

    except Exception as e:
        await update_status(id_vacancy_notification, user_tg_id, 'error', f"{e}")

    else:
        await update_status(id_vacancy_notification, user_tg_id, 'success', "No errors")
        return True
    return False



async def broadcaster(id_vacancy_notification: int, vacancy_text: str, bot: Bot):
    markup = await create_inkb(id=id_vacancy_notification,
                               is_next=False,
                               btn_like_nlike="like",
                               btn_more_less="more")
    users_tg_id = await get_users_with_notification(id_vacancy_notification)
    try:
        for tg_id in users_tg_id:
            await send_notifications(id_vacancy_notification, tg_id, vacancy_text, markup, bot)
            await asyncio.sleep(.05)
    finally:
        pass


async def sender(id_vacancy_notification: int, vacancy_text: str, creator, bot: Bot):
    if not await cheak_table(id_vacancy_notification):
        await create_table(id_vacancy_notification, creator)
    await broadcaster(id_vacancy_notification, vacancy_text, bot)

    await delete_table(id_vacancy_notification)
    print("кайф, все работает")
