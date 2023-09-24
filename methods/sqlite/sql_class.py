import sqlite3
from datetime import datetime

columns_titles = ["id", "employer", "work_type", "salary", "min_age", "min_exp", "datetime", "s_dscr", "l_dscr"]


class SqlConnection:
    def __init__(self, cur: sqlite3, conn: sqlite3):
        self.cur: sqlite3 = cur
        self.conn: sqlite3 = conn


class DatabaseCommands:
    def __init__(self, sql_conn: SqlConnection):
        self.sql_conn: SqlConnection = sql_conn

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


class Vacancy:
    def __init__(self,
                 values: dict = None,
                 vacancy_id: int = None):

        if values:
            self.values: dict = values

        if vacancy_id:
            self.vacancy_id: int = vacancy_id


class VacanciesCommands:
    def __init__(self,
                 sql_connection: SqlConnection,
                 db_commands: DatabaseCommands,
                 vacancy: Vacancy):

        self.sql_conn: SqlConnection = sql_connection
        self.db_cmd: DatabaseCommands = db_commands
        self.vacancy: Vacancy = vacancy

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
            vacancy_id: int = self.sql_conn.cur.fetchone()[0]
            return vacancy_id

        except Exception as ex:
            return False

    async def to_text(self, vacancy: Vacancy, type_descr: str) -> str:
        # !!!!!!!!!!!!!! Почему бы не работать сразу с values вакансии, нежели с id

        if vacancy.vacancy_id:  # если у вакансии id, а не ряд
            row: tuple = await self.db_cmd.get_row_by_id(vacancy.vacancy_id)
            self.vacancy.values = await self.db_cmd.row_to_dict(row)

        final_text: str = await self.db_cmd.dict_to_text(vacancy_values=vacancy.values, type_descr=type_descr)

        return final_text


