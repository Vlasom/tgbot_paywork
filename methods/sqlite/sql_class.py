import sqlite3
from datetime import datetime
import redis
from assets import texts
from user_class import User

columns_titles = ["id", "employer", "work_type", "salary", "min_age", "min_exp", "datetime", "s_dscr", "l_dscr"]


class SqlConnection:

    def __init__(self, cur: sqlite3, conn: sqlite3):
        self.cur: sqlite3 = cur
        self.conn: sqlite3 = conn

    async def close_conn(self):
        self.conn.close()


class DatabaseCommands:
    def __init__(self, sql_connection: SqlConnection):
        self.sql_conn: SqlConnection = sql_connection

    async def get_row_by_id(self, row_id_in_db: int) -> tuple:
        # Получение строки из бд по передаваемому id

        self.sql_conn.cur.execute("SELECT * FROM vacancies WHERE id = ?", (row_id_in_db,))
        row_in_db: tuple = self.sql_conn.cur.fetchone()
        return row_in_db

    @staticmethod
    async def row_to_dict(row_in_db: tuple) -> dict:
        # Переделывание передаваемой в функцию строки из бд в словарь

        diction: dict = {}
        for i, column in enumerate(columns_titles):
            diction[column] = row_in_db[i]

        return diction

    @staticmethod
    async def dict_to_text(vacancy_values: dict, type_descr: str) -> str:
        employer: str = vacancy_values['employer']
        work_type: str = vacancy_values['work_type']
        salary: str = vacancy_values['salary']
        min_age: str = f"Минимальный возраст: {vacancy_values['min_age']}\n" if vacancy_values[
                                                                                    'min_age'] is not None else ""
        min_exp: str = f"Минимальный опыт работы: {vacancy_values['min_exp']}\n" if vacancy_values[
                                                                                        'min_exp'] is not None else ""
        datetime: str = vacancy_values['datetime']
        descr: str = vacancy_values['s_dscr'] if type_descr == "short" else vacancy_values['l_dscr']

        final_text = (f"<b>{employer}</b>\n"
                      f"{work_type}\n"
                      f"{salary}\n"
                      f"{min_age}"
                      f"{min_exp}"
                      f"{datetime}\n"
                      f"{descr}")

        return final_text


class Vacancy:
    def __init__(self,
                 values: dict = None,
                 id: int = None,
                 text: str = None):
        self.values: dict = values
        self.id: int = id
        self.text: str = text


class RedisCommands:
    def __init__(self):
        self.redis_client: redis.Redis = redis.Redis(host='localhost', db=1, charset="utf-8", decode_responses=True)

    async def close_conn(self):
        self.redis_client.close()

    async def user_add_history(self, user: User, vacancy: Vacancy):
        try:
            await self.redis_client.sadd(f"{user.tg_id}_history", vacancy.id)
            await self.redis_client.expire(f"{user.tg_id}_history", 86400)
            return True

        except Exception as ex:
            return False

    async def user_get_history(self, user: User) -> set | bool:
        history = self.redis_client.smembers(f"{user.tg_id}_history")

        if history:
            return history
        else:
            return False


class VacanciesCommands:
    def __init__(self,
                 sql_connection: SqlConnection,
                 db_commands: DatabaseCommands,
                 redis_commands: RedisCommands):

        self.sql_conn: SqlConnection = sql_connection
        self.db_cmd: DatabaseCommands = db_commands
        self.redis_cmd: RedisCommands = redis_commands

    async def create(self, vacancy: Vacancy) -> bool | bool and int:
        try:
            # Создаем в бд вакансию по словарю
            self.sql_conn.cur.execute(
                "INSERT INTO vacancies "
                "(employer, work_type, salary, min_age, min_exp, datetime, s_dscr, l_dscr, creator_tg_id, date_of_create)"
                f"VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (*vacancy.values.values(), datetime.now().strftime("%Y-%m-%d  %H:%M:%S"),))
            self.sql_conn.conn.commit()

            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            # порешать снизу суету

            # Получение id только что созданной вакансии для рассылки
            self.sql_conn.cur.execute("SELECT last_insert_rowid()")
            created_vacancy_id: int = self.sql_conn.cur.fetchone()[0]
            return created_vacancy_id

        except Exception as ex:
            return False

    async def to_text(self, vacancy: Vacancy, type_descr: str) -> str:
        # !!!!!!!!!!!!!! Почему бы не работать сразу с values вакансии, нежели с id

        if vacancy.id:  # если у вакансии id, а не ряд
            row: tuple = await self.db_cmd.get_row_by_id(vacancy.id)

            vacancy.values = await self.db_cmd.row_to_dict(row)

        final_text: str = await self.db_cmd.dict_to_text(vacancy_values=vacancy.values, type_descr=type_descr)

        return final_text

    async def get_not_viewed(self, user: User):
        # получаем множество уже просмотренных пользователем вакансий
        if history_of_viewed_vac := await self.redis_cmd.user_get_history(user):

            # получаем из базы данных вакансии которых он не видел (list[tuple])
            # и сортируем по кол-ву просмотрам
            self.sql_conn.cur.execute(f"SELECT * "
                                      f"FROM vacancies "
                                      f"WHERE id not in ({', '.join(history_of_viewed_vac)}) "
                                      f"ORDER BY count_of_viewers ASC")
        else:
            # если история пуста, получаем все вакансии и сортируем по кол-ву просмотрам
            self.sql_conn.cur.execute("SELECT * "
                                      "FROM vacancies "
                                      "ORDER BY count_of_viewers ASC")

        # записываем в переменную вакансию с наименьшим кол-вом просмотров
        not_viewed_vacancy = self.sql_conn.cur.fetchone()
        #  id vacany
        if not_viewed_vacancy:

            # получаем её id
            not_viewed_vacancy_id: int = not_viewed_vacancy[0]

            # добавляем этой вакансии в бд один просмотр
            self.sql_conn.cur.execute("UPDATE vacancies "
                                      "SET count_of_viewers = count_of_viewers + 1 "
                                      "WHERE id = ?", (not_viewed_vacancy_id,))
            self.sql_conn.conn.commit()

            # возвращаем текст вакансии и её id
            vacancy = Vacancy(id=not_viewed_vacancy_id)
            return await self.to_text(vacancy=vacancy,
                                      type_descr="short"), not_viewed_vacancy_id
        else:
            return texts.no_vacancies_notification, -1

    async def add_to_userlikes(self, user: User, vacancy: Vacancy) -> None:
        self.sql_conn.cur.execute("INSERT OR IGNORE "
                                  "INTO users_likes "
                                  "(user_tg_id, vacancy_id) "
                                  "VALUES (?, ?)",
                                  (user.tg_id, vacancy.id,))

        self.sql_conn.conn.commit()

    async def del_from_userlikes(self, user: User, vacancy: Vacancy) -> None:
        self.sql_conn.cur.execute("DELETE "
                                  "FROM users_likes "
                                  "WHERE user_tg_id = ? "
                                  "AND vacancy_id = ?",
                                  (user.tg_id, vacancy.id,))

        self.sql_conn.conn.commit()

    async def get_user_likes(self, user: User) -> list[tuple]:
        self.sql_conn.cur.execute("SELECT vacancies.* "
                                  "FROM users_likes "
                                  "JOIN vacancies ON users_likes.vacancy_id = vacancies.id "
                                  "WHERE users_likes.user_tg_id = ?",
                                  (user.tg_id,))

        users_liked_vacancies = self.sql_conn.cur.fetchall()
        return users_liked_vacancies

    async def get_user_creates(self, user: User) -> list[tuple]:
        self.sql_conn.cur.execute("SELECT * "
                                  "FROM vacancies "
                                  "WHERE creator_tg_id = ?",
                                  (user.tg_id,))

        created_by_user_vacancies = self.sql_conn.cur.fetchall()
        return created_by_user_vacancies

    async def check_vacancy_application(self, user: User, vacancy: Vacancy) -> bool:
        self.sql_conn.cur.execute(
            "SELECT 1 FROM vacancies_applications WHERE user_id = ? AND vacancy_id = ?",
            (user.tg_id, vacancy.id,))
        if self.sql_conn.cur.fetchone():
            return True
        else:
            return False

    async def add_vacancy_application(self, user: User, vacancy: Vacancy, application: str) -> None:
        self.sql_conn.cur.execute(
            "INSERT INTO vacancies_applications (user_id, vacancy_id, application) VALUES (?, ?, ?)",
            (user.tg_id, vacancy.id, application,))
        self.sql_conn.conn.commit()

    async def get_applications(self, vacancy: Vacancy) -> list[tuple]:
        self.sql_conn.cur.execute(
            "SELECT vacancies_applications.user_id, users.fullname, vacancies_applications.application "
            "FROM vacancies_applications "
            "JOIN users ON vacancies_applications.user_id = users.tg_id "
            "WHERE vacancies_applications.vacancy_id = ?", (vacancy.id,))
        return self.sql_conn.cur.fetchall()

    async def application_to_text(self, application: tuple) -> str:
        user_id = application[0]
        fullname = application[1]
        text = application[2]
        final_text = (f"Имя автора: {fullname}\n"
                      f"Его id: {user_id}\n\n"
                      f"{text}")
        return final_text
