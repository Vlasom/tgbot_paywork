from methods.sqlite.users import process_db_notifi
from keyboards.inline_keyboards import create_inkb
from aiogram.exceptions import TelegramRetryAfter, TelegramForbiddenError
from aiogram import Bot
import asyncio
from objects import Vacancy


class Sender:

    def __init__(self, id_vacancy_notification: int, vacancy: Vacancy, markup, creator_id, bot: Bot):
        self.id_vacancy_notification = id_vacancy_notification
        self.vacancy = vacancy
        self.markup = markup
        self.creator = creator_id
        self.bot = bot

    async def send_notifications(self, user_tg_id):
        try:
            await self.bot.send_message(chat_id=user_tg_id, text=self.vacancy.text, reply_markup=self.markup)

        except TelegramRetryAfter as e:
            await asyncio.sleep(e.retry_after)
            return self.send_notifications(user_tg_id)

        except TelegramForbiddenError as e:
            await process_db_notifi.update_active(user_tg_id)

        except Exception as e:
            await process_db_notifi.update_status(self.id_vacancy_notification, user_tg_id, 'error', f"{e}")

        else:
            await process_db_notifi.update_status(self.id_vacancy_notification, user_tg_id, 'success', "No errors")
            return True
        return False

    async def broadcaster(self):

        users_tg_id = await process_db_notifi.get_users_with_notification(self.id_vacancy_notification)
        try:
            for tg_id in users_tg_id:
                await self.send_notifications(tg_id)
                await asyncio.sleep(.05)
        finally:
            pass

    async def sender(self):
        if not await process_db_notifi.check_table(self.id_vacancy_notification):
            await process_db_notifi.create_table(self.id_vacancy_notification, self.creator)

        await self.broadcaster()

        await process_db_notifi.delete_table(self.id_vacancy_notification)
