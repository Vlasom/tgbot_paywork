from .sql_class import SqlConnection, Vacancy
from aiogram.exceptions import TelegramRetryAfter, TelegramForbiddenError
from aiogram import Bot
import asyncio


class User:
    def __init__(self, tg_id: int, username: str, fullname: str):
        self.tg_id = tg_id
        self.username = username
        self.fullname = fullname


class UserCommands:
    def __init__(self, sql_connection: SqlConnection, user: User):
        self.sql_conn = sql_connection
        self.user = user

    async def create(self):
        # сделать возможнсть получать из аргумента пользователя которому тд и тп
        self.sql_conn.cur.execute("INSERT OR IGNORE "
                                  "INTO users (tg_id, username, fullname, active) "
                                  "VALUES (?, ?, ?, ?)",
                                  (self.user.tg_id, self.user.username, self.user.fullname, 1))

        self.sql_conn.cur.execute("UPDATE users "
                                  "SET username = ?, fullname = ?, active = ? "
                                  "WHERE tg_id = ?",
                                  (self.user.username, self.user.fullname, 1, self.user.tg_id))

        self.sql_conn.conn.commit()


class VacancyNotification:
    def __init__(self, sql_connection: SqlConnection):
        self.sql_conn = sql_connection

    async def check_existing_table(self, name_table: int) -> bool:
        self.sql_conn.cur.execute("SELECT name "
                                  "FROM sqlite_master "
                                  "WHERE type='table' AND name= ?",
                                  (name_table,))
        existing_table = self.sql_conn.cur.fetchone()

        return bool(existing_table)

    async def create_notification_table(self, name_table: int, vacancy_creator: int) -> None:

        self.sql_conn.cur.execute("CREATE TABLE "
                                  f"IF NOT EXISTS [{name_table}] "
                                  "(user_tg_id INTEGER PRIMARY KEY UNIQUE NOT NULL,"
                                  "status_notification TEXT DEFAULT waiting NOT NULL,"
                                  "error TEXT)")

        self.sql_conn.cur.execute(f"INSERT INTO [{name_table}] (user_tg_id) "
                                  "SELECT tg_id "
                                  "FROM users "
                                  "WHERE active = 1 "
                                  "AND notification_status = 1 AND tg_id <> ?",
                                  (vacancy_creator,))

        self.sql_conn.conn.commit()

    async def delete_notification_table(self, name_table: int) -> None:
        self.sql_conn.cur.execute(f"DROP TABLE [{name_table}]")
        self.sql_conn.conn.commit()

    async def get_users_with_no_notification(self, name_table: int) -> list:
        self.sql_conn.cur.execute(f"SELECT user_tg_id "
                                  f"FROM [{name_table}] "
                                  f"WHERE status_notification = 'waiting'")

        users_list_with_no_notification = [tuple_with_user_id[0] for tuple_with_user_id in self.sql_conn.cur.fetchall()]

        return users_list_with_no_notification

    async def update_notification_status(self,
                                         name_table: int,
                                         user: User,
                                         notification_status: str,
                                         error_description: str) -> None:

        self.sql_conn.cur.execute(f"UPDATE [{name_table}] "
                                  f"SET status_notification = '{notification_status}', error = '{error_description}' "
                                  f"WHERE user_tg_id = {user.tg_id}")

        self.sql_conn.conn.commit()

    async def update_status_of_available(self, user: User) -> None:
        self.sql_conn.cur.execute("UPDATE users "
                                  "SET active = 0 "
                                  "WHERE tg_id = ?", (user.tg_id,))

        self.sql_conn.conn.commit()

    async def turn_on_user_notification(self, user: User) -> None:
        self.sql_conn.cur.execute("UPDATE users "
                                  "SET notification_status = 1 "
                                  "WHERE tg_id = ?", (user.tg_id,))

        self.sql_conn.conn.commit()

    async def turn_off_user_notification(self, user: User) -> None:
        self.sql_conn.cur.execute("UPDATE users "
                                  "SET notification_status = 0 "
                                  "WHERE tg_id = ?", (user.tg_id,))

        self.sql_conn.conn.commit()


class NotificationsSender:

    def __init__(self,
                 vacancy: Vacancy,
                 vacancy_notification: VacancyNotification,
                 vacancy_markup,
                 creator_vacancy: int,
                 bot: Bot):

        self.vacancy = vacancy
        self.vacancy_notification = vacancy_notification
        self.vacancy_markup = vacancy_markup
        self.vacancy_creator = creator_vacancy
        self.bot = bot

    async def send_notifications(self, user: User) -> bool:
        try:
            await self.bot.send_message(chat_id=user.tg_id,
                                        text=self.vacancy.text,
                                        reply_markup=self.vacancy_markup)

        except TelegramRetryAfter as e:
            await asyncio.sleep(e.retry_after)
            return self.send_notifications(user)

        except TelegramForbiddenError:
            await self.vacancy_notification.update_status_of_available(user)

        except Exception as e:
            await self.vacancy_notification.update_notification_status(name_table=self.vacancy.id,
                                                                       user=user,
                                                                       notification_status=f"{e}",
                                                                       error_description='error')

        else:
            await self.vacancy_notification.update_notification_status(name_table=self.vacancy.id,
                                                                       user=user,
                                                                       notification_status='success',
                                                                       error_description="No errors")
            return True

        return False

    async def broadcaster(self) -> None:

        users_tg_id_no_notification = \
            await self.vacancy_notification.get_users_with_no_notification(name_table=self.vacancy.id)

        for user_tg_id in users_tg_id_no_notification:
            await self.send_notifications(user_tg_id)
            await asyncio.sleep(.05)

    async def sender(self) -> None:
        if not await self.vacancy_notification.check_existing_table(name_table=self.vacancy.id):
            await self.vacancy_notification.create_notification_table(name_table=self.vacancy.id,
                                                                      vacancy_creator=self.vacancy_creator)

        await self.broadcaster()

        await self.vacancy_notification.delete_notification_table(name_table=self.vacancy.id)
