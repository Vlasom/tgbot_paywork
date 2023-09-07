from datetime import datetime
from .processes_db import conn, cur
from methods.redis.users_history import get_history

__all__ = ["vacancy_create", "vacancy_get_text", "vacancy_to_text", "vacancy_get_next", "main_text"]


def _vacancy_get_dict(vacancy_id: int) -> dict:
    """
    :param vacancy_id: vacancy_id in database, which need to get
    :return: dictionary of ...
    """

    def row_to_dict(row) -> dict:
        """
        :param row:
        remake an incoming data_object into a dictionary
        :return: str
        """
        diction: dict = {}
        for elem, col in enumerate(cur.description):
            diction[col[0]] = row[elem]
        return diction

    def get_db_row():
        cur.execute(f"SELECT * FROM vacancies WHERE id = {vacancy_id}")
        row = cur.fetchone()
        return row

    if type(vacancy_id) is int:
        values: dict = row_to_dict(row=get_db_row())
    else:
        raise ValueError("vacancy_id must be int")

    return values


async def vacancy_create(values: dict) -> bool:
    """
    :param values:
    :return:
    """
    try:
        cur.execute("INSERT INTO vacancies (employer, work_type, salary, min_age, min_exp, datetime, s_dscr, l_dscr, date_of_create)"
                    f"VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (*values.values(), datetime.now().strftime("%Y-%m-%d  %H:%M:%S"),))
        conn.commit()
        return True

    except Exception as ex:
        return False


async def vacancy_get_text(vacancy_id: int, type_descr: str) -> str:
    """
    :param vacancy_id: vacancy_id in database, which values need to convert into text
    :param type_descr: type of description need to get in a future vacancy
    :return: values vacancy in readable for users text
    """

    try:
        vacancy_values = _vacancy_get_dict(vacancy_id=vacancy_id)
    except ValueError as error:
        print(error)
        return "vacancy_id must be int"

    final_text = vacancy_to_text(vacancy_values=vacancy_values, type_descr=type_descr)

    return final_text


async def vacancy_get_next(count: int | str):

    cur.execute(f"SELECT * FROM vacancies")
    if type(count) is int:
        res = cur.fetchmany(count)
    elif count == "all":
        res = cur.fetchall()
    else:
        res = ""

    return list(res)


def main_text():
    return "личный кабинет"


def vacancy_to_text(vacancy_values: dict, type_descr: str) -> str:

    employer = vacancy_values['employer']
    work_type = vacancy_values['work_type']
    salary = vacancy_values['salary']
    min_age = f"Минимальный возраст: {vacancy_values['min_age']}\n" if vacancy_values['min_age'] is not None else ""
    min_exp = f"Минимальный опыт работы: {vacancy_values['min_exp']}\n" if vacancy_values['min_exp'] is not None else ""
    datetime = vacancy_values['datetime']
    descr = vacancy_values['s_dscr'] if type_descr == "short" else vacancy_values['l_dscr']

    final_text = (f"*{employer}*\n"
                  f"{work_type}\n"
                  f"{salary}\n"
                  f"{min_age}"
                  f"{min_exp}"
                  f"{datetime}\n"
                  f"{descr}")

    return final_text

def get_vacancies(user_tg_id):
    history = ",".join(get_history(user_tg_id))
    cur.execute("SELECT * FROM vacancies WHERE id not in (?) ORDER BY count_of_viewers ASC", (history,))
    row = cur.fetchall()
    return row

