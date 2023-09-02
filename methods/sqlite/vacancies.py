from .open_db import conn, cur


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
        cur.execute("INSERT INTO vacancies (employer, work_type, salary, min_age, min_exp, datetime, s_dscr, l_dscr) "
                    f"VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (*values.values(),))
        conn.commit()
        return True

    except Exception as ex:
        return False


async def vacancy_to_text(vacancy_id: int, type_descr: str) -> str:
    """
    :param vacancy_id: vacancy_id in database, which values need to convert into text
    :param type_descr: type of description need to get in a future vacancy
    :return: values vacancy in readable for users text
    """

    try:
        vacancy_values = _vacancy_get_dict(vacancy_id=vacancy_id)
    except Exception as ex:
        return "vacancy_id must be int"

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


async def vacancy_view_next():

    cur.execute("SELECT * FROM vacancies")
    res = cur.fetchone()
    return list(res)


def main_text():
    return "личный кабинет"

def confirm_vacancy_txt(data, type_descr):
    return str(f"*{data.get('employer')}*\n"
               f"{data.get('work_type')}\n"
               f"{data.get('salary')}\n"

               f"Минимальный возраст \- {data.get('min_age')}\n"

               f"Минимальный опыт работы \- {data.get('min_exp')}\n"

               f"Время \- {data.get('datetime')}\n\n"
               f"{data.get('s_dscr' if type_descr == 'short' else 'l_dscr')}")

