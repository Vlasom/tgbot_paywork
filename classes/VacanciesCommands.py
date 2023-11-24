import os

from .SqlConnection import SqlConnection
from .RedisCommands import RedisCommands
from .DataBaseCommands import DatabaseCommands
from .Vacancies import Vacancy
from .Users import User

from datetime import datetime


class VacanciesCommands:
    def __init__(self,
                 sql_connection: SqlConnection,
                 db_commands: DatabaseCommands,
                 redis_commands: RedisCommands):

        self.sql_conn: SqlConnection = sql_connection
        self.db_cmd: DatabaseCommands = db_commands
        self.redis_cmd: RedisCommands = redis_commands

    async def create(self, vacancy: Vacancy) -> None:
        # Создаем в бд вакансию по словарю
        self.sql_conn.cur.execute(
            "INSERT INTO vacancies "
            "(employer, work_type, salary, min_age, min_exp, datetime,"
            " s_dscr, l_dscr, image_id, creator_tg_id, date_of_create)"
            f"VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (*vacancy.values.values(), datetime.now().strftime("%Y-%m-%d  %H:%M:%S"),))
        self.sql_conn.conn.commit()

    async def save_image(self, path: str) -> None:
        with open(file=path, mode="rb") as file:
            self.sql_conn.cur.execute("INSERT INTO images (image_data) VALUES (?)", (file.read(),))
        os.remove(path)
        self.sql_conn.conn.commit()

    async def delete_image_by_vacancy_id(self, vacancy: Vacancy) -> None:
        self.sql_conn.cur.execute("SELECT images.id "
                                  "FROM images "
                                  "JOIN vacancies ON images.id = vacancies.image_id "
                                  "WHERE vacancies.id = ?", (vacancy.id,))
        image_id = self.sql_conn.cur.fetchone()[0]
        if image_id != 0:
            self.sql_conn.cur.execute("DELETE FROM images WHERE id = ?", (image_id,))

        self.sql_conn.conn.commit()

    async def to_text(self, vacancy: Vacancy, type_descr: str) -> str:
        # !!!!!!!!!!!!!! Почему бы не работать сразу с values вакансии, нежели с id

        if not vacancy.values:  # если у вакансии id, а не ряд
            row: tuple = await self.db_cmd.get_row_by_id(vacancy.id)

            vacancy.values = await self.db_cmd.row_to_dict(row)

        final_text: str = await self.db_cmd.dict_to_text(vacancy_values=vacancy.values, type_descr=type_descr)

        return final_text

    async def get_photo_by_vacancy_id(self, id) -> bytes:
        self.sql_conn.cur.execute("SELECT image_data "
                                  "FROM images "
                                  "JOIN vacancies ON images.id = WHERE id = ?", (id,))
        photo = self.sql_conn.cur.fetchone()
        return photo

    async def get_not_viewed(self, user: User) -> Vacancy | bool:
        # получаем множество уже просмотренных пользователем вакансий
        if history_of_viewed_vac := await self.redis_cmd.user_get_history(user):

            # получаем из базы данных вакансии которых он не видел (list[tuple])
            # и сортируем по кол-ву просмотрам
            self.sql_conn.cur.execute(
                "SELECT "
                "vacancies.id, employer, work_type, salary, min_age, min_exp, datetime, s_dscr, l_dscr, image_data "
                "FROM vacancies "
                "JOIN images ON images.id = vacancies.image_id "
                f"WHERE vacancies.id NOT IN ({', '.join(history_of_viewed_vac)}) "
                "ORDER BY count_of_viewers ASC")
        else:
            # если история пуста, получаем все вакансии и сортируем по кол-ву просмотрам
            self.sql_conn.cur.execute(
                "SELECT "
                "vacancies.id, employer, work_type, salary, min_age, min_exp, datetime, s_dscr, l_dscr, image_data "
                "FROM vacancies "
                "JOIN images ON images.id = vacancies.image_id "
                "ORDER BY count_of_viewers ASC ")

        # записываем в переменную вакансию с наименьшим кол-вом просмотров
        not_viewed_vacancy = self.sql_conn.cur.fetchone()
        #  id vacany

        if not_viewed_vacancy:

            # получаем её id
            not_viewed_vacancy_id: int = not_viewed_vacancy[0]
            photo = not_viewed_vacancy[9]

            # добавляем этой вакансии в бд один просмотр
            self.sql_conn.cur.execute("UPDATE vacancies "
                                      "SET count_of_viewers = count_of_viewers + 1 "
                                      "WHERE id = ?", (not_viewed_vacancy_id,))
            self.sql_conn.conn.commit()

            # возвращаем текст вакансии и её id
            vacancy = Vacancy(id=not_viewed_vacancy_id,
                              photo=photo,
                              values=await self.db_cmd.row_to_dict(not_viewed_vacancy))
            vacancy.text = await self.to_text(vacancy=vacancy,
                                              type_descr="short")

            return vacancy
        else:
            return False

    async def add_to_user_likes(self, user: User, vacancy: Vacancy) -> None:
        self.sql_conn.cur.execute("INSERT OR IGNORE "
                                  "INTO users_likes "
                                  "(user_tg_id, vacancy_id) "
                                  "VALUES (?, ?)",
                                  (user.tg_id, vacancy.id,))

        self.sql_conn.conn.commit()

    async def del_from_user_likes(self, user: User, vacancy: Vacancy) -> None:
        self.sql_conn.cur.execute("DELETE "
                                  "FROM users_likes "
                                  "WHERE user_tg_id = ? "
                                  "AND vacancy_id = ?",
                                  (user.tg_id, vacancy.id,))

        self.sql_conn.conn.commit()

    async def get_user_likes(self, user: User) -> list[tuple]:
        self.sql_conn.cur.execute(
            "SELECT "
            "vacancies.id, employer, work_type, salary, min_age, min_exp, datetime, s_dscr, l_dscr, image_data "
            "FROM vacancies "
            "JOIN users_likes ON users_likes.vacancy_id = vacancies.id "
            "JOIN images ON images.id = image_id "
            "WHERE users_likes.user_tg_id = ?",
            (user.tg_id,))

        users_liked_vacancies = self.sql_conn.cur.fetchall()
        return users_liked_vacancies

    async def check_user_like(self, user: User, vacancy: Vacancy) -> bool:
        self.sql_conn.cur.execute("SELECT * FROM users_likes WHERE user_tg_id = ? AND vacancy_id = ?",
                                  (user.tg_id, vacancy.id,))
        return bool(self.sql_conn.cur.fetchone())

    async def get_user_creates(self, user: User) -> list[tuple]:
        self.sql_conn.cur.execute(
            "SELECT "
            "vacancies.id, employer, work_type, salary, min_age, min_exp, datetime, s_dscr, l_dscr, image_data "
            "FROM vacancies "
            "JOIN images ON images.id = image_id "
            "WHERE creator_tg_id = ?",
            (user.tg_id,))

        created_by_user_vacancies = self.sql_conn.cur.fetchall()
        return created_by_user_vacancies

    async def edit_vacancy_data(self, vacancy: Vacancy, value, column_name) -> None:
        self.sql_conn.cur.execute(f"UPDATE vacancies SET {column_name} = ? WHERE id = ?", (value, vacancy.id,))
        self.sql_conn.conn.commit()

    async def delete_vacancy(self, vacancy: Vacancy) -> None:
        self.sql_conn.cur.execute(f"DELETE FROM vacancies WHERE id = ?", (vacancy.id,))
        self.sql_conn.conn.commit()

    async def check_application(self, user: User, vacancy: Vacancy) -> bool:
        self.sql_conn.cur.execute(
            "SELECT 1 FROM vacancies_applications WHERE user_id = ? AND vacancy_id = ?",
            (user.tg_id, vacancy.id,))
        if self.sql_conn.cur.fetchone():
            return True
        else:
            return False

    async def add_application(self, user: User, vacancy: Vacancy, application: str) -> None:
        self.sql_conn.cur.execute(
            "INSERT INTO vacancies_applications (user_id, vacancy_id, application, status) VALUES (?, ?, ?, 'Ожидает')",
            (user.tg_id, vacancy.id, application,))
        self.sql_conn.conn.commit()

    async def get_vacancy_applications(self, vacancy: Vacancy) -> list[tuple]:
        self.sql_conn.cur.execute(
            "SELECT vacancies_applications.user_id, users.fullname, "
            "vacancies_applications.application, vacancies.employer, vacancies.work_type "
            "FROM vacancies_applications "
            "JOIN users ON vacancies_applications.user_id = users.tg_id "
            "JOIN vacancies ON vacancies_applications.vacancy_id = vacancies.id "
            "WHERE vacancies_applications.vacancy_id = ?", (vacancy.id,))
        return self.sql_conn.cur.fetchall()

    async def get_user_applications(self, user: User) -> list[tuple]:
        self.sql_conn.cur.execute(
            "SELECT "
            "vacancies.id, employer, work_type, salary, min_age, min_exp, datetime, s_dscr, l_dscr, image_data, "
            "vacancies_applications.application, vacancies_applications.status "
            "FROM vacancies "
            "JOIN vacancies_applications ON vacancies.id = vacancies_applications.vacancy_id "
            "JOIN images ON images.id = image_id "
            "WHERE vacancies_applications.user_id = ?", (user.tg_id,))
        return self.sql_conn.cur.fetchall()

    async def delete_application(self, user_id: int, vacancy_id: int) -> None:
        self.sql_conn.cur.execute("DELETE FROM vacancies_applications WHERE user_id = ? AND vacancy_id = ?",
                                  (user_id, vacancy_id,))
        self.sql_conn.conn.commit()

    async def application_to_text(self, application: tuple) -> str:
        user_id = application[0]
        fullname = application[1]
        text = application[2]
        final_text = (f"Имя автора: {fullname}\n"
                      f"Его id: {user_id}\n\n"
                      f"{text}")
        return final_text

    async def vacancy_miniature_text(self, id: int = None, employer: str = None, work_type: str = None):
        if (id or id) == 0 and not (employer and employer):
            row = await self.db_cmd.get_row_by_id(id)
            values = await self.db_cmd.row_to_dict(row)
            employer = values['employer']
            work_type = values['work_type']
        final_text = (f"<b>{employer}</b>\n"
                      f"{work_type}\n...\n\n")
        return final_text

    async def application_decline(self, user_id: int, vacancy_id: int) -> None:
        self.sql_conn.cur.execute(
            "UPDATE vacancies_applications SET status = 'Отклонено' WHERE user_id = ? AND vacancy_id = ?",
            (user_id, vacancy_id))
        self.sql_conn.conn.commit()

    async def application_confirm(self, user_id: int, vacancy_id: int) -> None:
        self.sql_conn.cur.execute(
            "UPDATE vacancies_applications SET status = 'Принято' WHERE user_id = ? AND vacancy_id = ?",
            (user_id, vacancy_id))
        self.sql_conn.conn.commit()

    async def get_creator_id(self, vacancy: Vacancy) -> int:
        self.sql_conn.cur.execute(f"SELECT creator_tg_id FROM vacancies WHERE id = ?", (vacancy.id,))
        return self.sql_conn.cur.fetchone()[0]
