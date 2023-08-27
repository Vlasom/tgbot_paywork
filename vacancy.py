from datetime import datetime
import sqlite3

# placeholder in sql requests
# при получении данных из бд, сделать скрипт который будет отправлять вакансии с наименьшим кол-вом просмотров


class VacanciesEmploy:

    def __init__(self, asf):

        self.l_descr = asf

    @staticmethod
    def open_db(inner_def):
        def _():
            conn = sqlite3.connect("database/database.db")
            cur = conn.cursor()

            text = inner_def(cur)

            conn.close()
            return text

        return _

    @staticmethod
    @open_db
    def get_db_row(cur):

        cur.execute("SELECT * FROM vacancys")

        res = cur.fetchone()

        return list(res)


    def get_next_one(self):

        pass


    def get_next_many(self, count):
        pass


    def vac_to_text(self):
        pass


class VacancyEmployer:
    def __init__(self):
        pass
