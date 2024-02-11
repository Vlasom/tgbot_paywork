from .Users import User
from .SqlConnection import SqlConnection
from classes.sql_conn import sql_connection
from .Vacancies import Vacancy

columns_titles = ("id", "employer", "work_type", "salary", "min_age", "min_exp", "datetime", "s_dscr", "l_dscr")


class DatabaseCommands:
    def __init__(self):
        self.sql_conn: SqlConnection = sql_connection

    async def get_last_insert_rowid(self) -> int:
        self.sql_conn.cur.execute("SELECT last_insert_rowid()")
        last_insert_rowid: int = self.sql_conn.cur.fetchone()[0]
        return last_insert_rowid

    async def get_row_by_id(self, row_id_in_db: int) -> tuple:
        # Получение строки из бд по передаваемому id

        self.sql_conn.cur.execute(
            "SELECT "
            "vacancies.id, employer, work_type, salary, min_age, min_exp, datetime, s_dscr, l_dscr, image_data "
            "FROM vacancies "
            "JOIN images ON images.id = vacancies.image_id "
            "WHERE vacancies.id = ?", (row_id_in_db,))
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
        vacancy_id = f"Вакансия №{vacancy_values.get('id')}" if (vacancy_id := vacancy_values.get(
            'id')) or vacancy_id == 0 else "Вакансия №__"
        employer: str = vacancy_values.get('employer')
        work_type: str = vacancy_values.get('work_type')
        salary: str = vacancy_values.get('salary')
        min_age: str = f"• Мин. возраст: {vacancy_values.get('min_age')}\n" \
            if vacancy_values.get('min_age') else ""
        min_exp: str = f"• Мин. опыт работы: {vacancy_values['min_exp']}\n" \
            if vacancy_values.get('min_exp') else ""
        datetime: str = vacancy_values.get('datetime')
        descr: str = vacancy_values.get('s_dscr') if type_descr == "short" else vacancy_values.get('l_dscr')

        final_text = (f"• <b>{vacancy_id}</b>\n"
                      f"• {employer}\n"
                      f"• {work_type}\n"
                      f"• <b>{salary}</b>\n"
                      f"{min_age}"
                      f"{min_exp}"
                      f"• Период работы: {datetime}\n"
                      f"• <b>Описание</b>\n  {descr}")

        return final_text

    async def add_user_to_db(self, user: User) -> None:
        # сделать возможнсть получать из аргумента пользователя которому тд и тп
        self.sql_conn.cur.execute("INSERT OR IGNORE "
                                  "INTO users (tg_id, username, fullname, active) "
                                  "VALUES (?, ?, ?, ?)",
                                  (user.tg_id, user.username, user.fullname, 1))

        self.sql_conn.cur.execute("UPDATE users "
                                  "SET username = ?, fullname = ?, active = ? "
                                  "WHERE tg_id = ?",
                                  (user.username, user.fullname, 1, user.tg_id))

        self.sql_conn.cur.execute("INSERT OR IGNORE "
                                  "INTO users_tg_notifications user_tg_id = ?",
                                  (user.tg_id,))

        # self.sql_conn.cur.execute("INSERT OR IGNORE "
        #                           "INTO users_mail_notifications user_tg_id = ?",
        #                           (user.tg_id,))

        self.sql_conn.conn.commit()
