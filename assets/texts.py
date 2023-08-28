import sqlite3

welcome_text = "приветствие"
employ_or_employer = "Выберите работодатель вы или работник"
employ_warn_info = "as"

start_create = "Заполните форму для создания ваканcии\n для отмены напишите /cancel"
fill_employer = "Напишите организацию"
fill_job = "Напишите необходимую должность или работу для выполнения"
fill_salary = "Напишите предлагаемую зарплату"
fill_minage = "Напишите требуемого минимального возраста"
fill_minexp = "Напишите требуемый минимальный опыт работы"
fill_date = "Напишите время или период работы"
fill_short_dsp = "Напишите краткое описание вакансии"
fill_long_dsp = "Напишите развёрнутое описание вакансии"
confirm_vacancy = "Ваша вакансия:"
cancel_create_vacancy = "Создание вакансии отменено, ваша вакансия удалена"
sure_cancel_create_vacancy = "Вы точно хотите отменить создание вакансии?"
mess12dsh = "Что вы хотите сделать?"


edit_employer = "обновлена организацию\nВаша вакансия:"
edit_job = "обновлена должность\nВаша вакансия:"
edit_salary = "обновлена зарплату\nВаша вакансия:"
edit_minage = "обновлена минимальный возраст\nВаша вакансия:"
edit_minexp = "обновлена минимальный опыт работы\nВаша вакансия:"
edit_date = "обновлена время или период работы\nВаша вакансия:"
edit_short_dsp = "обновлена краткое описание вакансии\nВаша вакансия:"
edit_long_dsp = "обновлена развёрнутое описание вакансии\nВаша вакансия:"

warning_msg = "ТЫ ШО, ТУПОЙ ЧТОЛЕ о_О?\nЧИТАТЬ НЕ УМЕЕШЬ?\nИДИ ОБРАТНО В ШКОЛУ, УПЫРЬ"


class Vacancy:
    def __init__(self, vac_id: int = 0):
        self.vac_id = vac_id
        self.value: dict = {}

        # self.employer = values['employer']
        # self.job = values['job']
        # self.salary = values['salary']
        # self.min_age = values['min_age']
        # self.min_exp = values['min_exp']
        # self.s_dscr = values['s_dscr']
        # self.l_dscr = values['l_dscr']

    def create(self, values):

        self.value: dict = values

        conn = sqlite3.connect("database/database.db")
        cur = conn.cursor()

        cur.execute("INSERT INTO vacancies (employer, work_type, salary, min_age, min_exp, datetime, s_dscr, l_dscr) "
                    f"VALUES ({values['employer']}, {values['work_type']},"
                            f"{values['salary']}, {values['min_age']},"
                            f"{values['min_exp']}, {values['datetime']},"
                            f"{values['s_dscr']}, {values['l_dscr']})")

        conn.commit()
        conn.close()

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

        conn = sqlite3.connect("database/database.db")
        cur = conn.cursor()
        def _get_db_row():


            if self.vac_id == 0:
                cur.execute("SELECT * FROM vacancies")
            else:
                cur.execute(f"SELECT * FROM vacancies WHERE id = {self.vac_id}")

            row = cur.fetchone()
            conn.close()

            return row

        dic = self._to_dict(cur, _get_db_row())
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



def main_text():
    return "личный кабинет"





def confirm_vacancy_txt(data, type_descr):
    return str(f"*{data.get('employer')}*\n"
               f"{data.get('job')}\n"
               f"{data.get('salary')}\n"
               
               f"Минимальный возраст \- {data.get('minage')}\n"
               
               f"Минимальный опыт работы \- {data.get('minexp')}\n"
               
               f"Время \- {data.get('date')}\n\n"
               f"{data.get('short_dsp' if type_descr == 'short' else 'long_dsp')}")



