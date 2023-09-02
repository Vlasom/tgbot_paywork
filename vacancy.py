from datetime import datetime
import sqlite3

# placeholder in sql requests
# при получении данных из бд, сделать скрипт который будет отправлять вакансии с наименьшим кол-вом просмотров




class Vacancy():

    def __init__(self, vac_id: int = 0):
        self.vac_id = vac_id
        self.value: dict = {}

        self.conn = sqlite3.connect("database/database.db")
        self.cur = self.conn.cursor()

        # self.employer = values['employer']
        # self.job = values['job']
        # self.salary = values['salary']
        # self.min_age = values['min_age']
        # self.min_exp = values['min_exp']
        # self.s_dscr = values['s_dscr']
        # self.l_dscr = values['l_dscr']

    def create(self, values: dict):

        self.value: dict = values

        try:
            self.cur.execute("INSERT INTO vacancies (employer, work_type, salary, min_age, min_exp, datetime, s_dscr, l_dscr) "
                        f"VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (*values.values(),))
            self.conn.commit()
            return True

        except Exception as ex:
            return False

        finally:
            self.conn.close()


    @staticmethod
    def _to_dict(cur, row) -> dict:
        diction = {}
        for elem, col in enumerate(cur.description):
            diction[col[0]] = row[elem]
        return diction



    def get_dic(self) -> str:
        """
        :return: str
        """

        def _get_db_row():


            if self.vac_id == 0:
                self.cur.execute("SELECT * FROM vacancies")
            else:
                self.cur.execute(f"SELECT * FROM vacancies WHERE id = {self.vac_id}")

            row = self.cur.fetchone()
            self.conn.close()

            return row

        dic = self._to_dict(self.cur, _get_db_row())
        return dic

    def get_text1(self, type_descr):

        self.value = self.get_dic()

        employer = self.value['employer']
        work_type = self.value['work_type']
        salary = self.value['salary']
        min_age = f"Минимальный возраст: {self.value['min_age']}\n" if self.value['min_age'] is not None else ""
        min_exp = f"Минимальный опыт работы: {self.value['min_exp']}\n" if self.value['min_exp'] is not None else ""
        datetime = self.value['datetime']
        descr = self.value['s_dscr'] if type_descr == "short" else self.value['l_dscr']

        text = (f"*{employer}*\n"
                f"{work_type}\n"
                f"{salary}\n"
                f"{min_age}"
                f"{min_exp}"
                f"{datetime}\n"
                f"{descr}")

        return text


