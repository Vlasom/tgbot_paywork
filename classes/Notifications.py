from aiogram.exceptions import TelegramRetryAfter, TelegramForbiddenError
from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup, FSInputFile

from .SqlConnection import SqlConnection
from .Users import User
from classes.sql_conn import sql_connection
from assets import texts

import asyncio

events = {1: "new_vacancy_notifi", 2: "del_from_likes", 3: "answer_applications"}
places = {1: "users_tg_notifications", 2: "users_email_notifications"}
class DBNotification:
    def __init__(self):
        self.sql_conn: SqlConnection = sql_connection

    async def check_existing_table(self, table_name: str) -> bool:
        self.sql_conn.cur.execute("SELECT name "
                                  "FROM sqlite_master "
                                  "WHERE type='table' AND name= ?",
                                  (table_name,))
        existing_table = self.sql_conn.cur.fetchone()

        return bool(existing_table)

    async def create_notification_table(self, table_name: str, creator: int,
                                        is_vacancy_notification: bool) -> None:
        self.sql_conn.cur.execute("CREATE TABLE "
                                  f"IF NOT EXISTS [{table_name}] "
                                  "(user_tg_id INTEGER PRIMARY KEY UNIQUE NOT NULL,"
                                  "status_notification TEXT DEFAULT waiting NOT NULL,"
                                  "error TEXT)")

        self.sql_conn.cur.execute(f"INSERT INTO [{table_name}] (user_tg_id) "
                                  "SELECT tg_id "
                                  "FROM users JOIN users_tg_notifications "
                                  "ON users_tg_notifications.user_tg_id = users.tg_id "
                                  "WHERE users.active = 1 "
                                  "AND users.tg_id <> ?"
                                  f"{'AND users_tg_notifications.new_vacancy_notifi = 1' if is_vacancy_notification else ''}",
                                  (creator,))

        self.sql_conn.conn.commit()

    async def delete_notification_table(self, table_name: str) -> None:
        self.sql_conn.cur.execute(f"DROP TABLE [{table_name}]")
        self.sql_conn.conn.commit()

    async def get_not_notified_users(self, table_name: str) -> list:
        self.sql_conn.cur.execute(f"SELECT user_tg_id "
                                  f"FROM [{table_name}] "
                                  f"WHERE status_notification = 'waiting'")

        users_list_with_no_notification = [tuple_with_user_id[0] for tuple_with_user_id in self.sql_conn.cur.fetchall()]

        return users_list_with_no_notification

    async def update_notification_status(self,
                                         table_name: str,
                                         user: User,
                                         notification_status: str,
                                         error_description: str) -> None:
        self.sql_conn.cur.execute(f"UPDATE [{table_name}] "
                                  f"SET status_notification = '{notification_status}', error = '{error_description}' "
                                  f"WHERE user_tg_id = {user.tg_id}")

        self.sql_conn.conn.commit()

    async def update_status_of_available(self, user: User) -> None:
        self.sql_conn.cur.execute("UPDATE users "
                                  "SET active = 0 "
                                  "WHERE tg_id = ?", (user.tg_id,))

        self.sql_conn.conn.commit()

    async def turn_on_user_notification(self, place, event, user: User) -> None:
        self.sql_conn.cur.execute(f"UPDATE {places[place]} "
                                  f"SET {events[event]} = 1 "
                                  "WHERE user_tg_id = ?", (user.tg_id,))

        self.sql_conn.conn.commit()

    async def turn_off_user_notification(self, place, event, user: User) -> None:
        self.sql_conn.cur.execute(f"UPDATE {places[place]} "
                                  f"SET {events[event]} = 0 "
                                  "WHERE user_tg_id = ?", (user.tg_id,))

        self.sql_conn.conn.commit()

    async def get_user_email(self, user: User):
        self.sql_conn.cur.execute("SELECT email from users WHERE tg_id = ?", (user.tg_id,))
        email = self.sql_conn.cur.fetchone()[0]
        return email
    async def get_user_notifications(self, user: User):
        user_notifications = {}
        self.sql_conn.cur.execute("SELECT * from users_tg_notifications WHERE user_tg_id = ?", (user.tg_id,))
        user_notifications["tg"] = self.sql_conn.cur.fetchone()
        if await self.get_user_email(user):
            self.sql_conn.cur.execute("SELECT * from users_email_notifications WHERE user_tg_id = ?", (user.tg_id,))
            user_notifications["email"] = self.sql_conn.cur.fetchone()
        else:
            user_notifications["email"] = [0] * 4

        return user_notifications




class NotificationsSender:

    def __init__(self,
                 text: str,
                 markup: InlineKeyboardMarkup,
                 db_notification: DBNotification,
                 notification_name: str,
                 creator: User,
                 bot: Bot,
                 photo: FSInputFile = None):

        self.text = text
        self.markup = markup
        self.db_notification = db_notification
        self.notification_name = notification_name
        self.creator = creator
        self.bot = bot
        self.photo = photo

    async def send_notifications(self, user: User, is_vacancy_notification: bool) -> bool:
        try:
            if is_vacancy_notification:
                await self.bot.send_message(chat_id=user.tg_id,
                                            text=texts.new_vacancy_msg)
                await asyncio.sleep(.05)
            if self.photo:
                await self.bot.send_photo(chat_id=user.tg_id,
                                          photo=self.photo,
                                          caption=self.text,
                                          reply_markup=self.markup)
            else:
                await self.bot.send_message(chat_id=user.tg_id,
                                            text=self.text,
                                            reply_markup=self.markup)

        except TelegramRetryAfter as e:
            await asyncio.sleep(e.retry_after)
            await self.send_notifications(user, is_vacancy_notification)

        except TelegramForbiddenError:
            await self.db_notification.update_status_of_available(user)

        except Exception as e:
            await self.db_notification.update_notification_status(table_name=self.notification_name,
                                                                  user=user,
                                                                  notification_status=f"{e}",
                                                                  error_description='error')

        else:
            await self.db_notification.update_notification_status(table_name=self.notification_name,
                                                                  user=user,
                                                                  notification_status='success',
                                                                  error_description="No errors")
            return True

        return False

    async def broadcaster(self, is_vacancy_notification: bool) -> None:

        not_notified_users_tg_ids = \
            await self.db_notification.get_not_notified_users(table_name=self.notification_name)

        for user_tg_id in not_notified_users_tg_ids:
            user = User(tg_id=user_tg_id)
            await self.send_notifications(user, is_vacancy_notification)
            await asyncio.sleep(.05)

    async def sender(self, is_vacancy_notification: bool) -> None:
        if not await self.db_notification.check_existing_table(table_name=self.notification_name):
            await self.db_notification.create_notification_table(table_name=self.notification_name,
                                                                 creator=self.creator.tg_id,
                                                                 is_vacancy_notification=is_vacancy_notification)

        await self.broadcaster(is_vacancy_notification)

        await self.db_notification.delete_notification_table(table_name=self.notification_name)
