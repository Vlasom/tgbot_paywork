from .Users import User
from .SqlConnection import SqlConnection
from classes.sql_conn import sql_connection

columns_titles = ["id", "employer", "work_type", "salary", "min_age", "min_exp", "datetime", "s_dscr", "l_dscr"]


class DatabaseCommands:
    def __init__(self):
        self.sql_conn: SqlConnection = sql_connection

    async def get_last_insert_rowid(self):
        self.sql_conn.cur.execute("SELECT last_insert_rowid()")
        last_insert_rowid: int = self.sql_conn.cur.fetchone()[0]
        return last_insert_rowid

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
        min_age: str = f"Минимальный возраст: {vacancy_values['min_age']}\n" if vacancy_values['min_age'] is not None else ""
        min_exp: str = f"Минимальный опыт работы: {vacancy_values['min_exp']}\n" if vacancy_values['min_exp'] is not None else ""
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

    async def add_user_to_db(self, user: User):

        # сделать возможнсть получать из аргумента пользователя которому тд и тп
        self.sql_conn.cur.execute("INSERT OR IGNORE "
                                  "INTO users (tg_id, username, fullname, active) "
                                  "VALUES (?, ?, ?, ?)",
                                  (user.tg_id, user.username, user.fullname, 1))

        self.sql_conn.cur.execute("UPDATE users "
                                  "SET username = ?, fullname = ?, active = ? "
                                  "WHERE tg_id = ?",
                                  (user.username, user.fullname, 1, user.tg_id))

        self.sql_conn.conn.commit()
