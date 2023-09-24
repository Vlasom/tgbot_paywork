from datetime import datetime
from .processes_db import conn, cur
from assets import texts
from methods.redis.users_history import get_history

columns_titles = ["id", "employer", "work_type", "salary", "min_age", "min_exp", "datetime", "s_dscr", "l_dscr"]


async def get_row_by_id(vacancy_id: int) -> list:
    cur.execute("SELECT * FROM vacancies WHERE id = ?", (vacancy_id,))
    row = cur.fetchone()
    return row


async def row_to_dict(row) -> dict:
    """
    :param row:
    remake an incoming data_object into a dictionary
    :return: str
    """
    diction: dict = {}
    for i, title in enumerate(columns_titles):
        diction[title] = row[i]
    return diction


async def vacancy_create(values: dict) -> bool | bool and int:
    """
    :param values:
    :return:
    """
    try:
        cur.execute(
            "INSERT INTO vacancies "
            "(employer, work_type, salary, min_age, min_exp, datetime, s_dscr, l_dscr, creator_tg_id, date_of_create)"
            f"VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (*values.values(), datetime.now().strftime("%Y-%m-%d  %H:%M:%S"),))
        conn.commit()
        cur.execute("SELECT last_insert_rowid()")
        vacancy_id = cur.fetchone()[0]

        return vacancy_id

    except Exception as ex:
        return False


async def vacancy_to_text(vacancy: int | list | tuple, type_descr: str) -> str:
    """
    :param vacancy_id: vacancy_id in database, which values need to convert into text
    :param type_descr: type of description need to get in a future vacancy
    :return: values vacancy in readable for users text
    """

    if isinstance(vacancy, int):
        vacancy = await get_row_by_id(vacancy_id=vacancy)

    values = await row_to_dict(vacancy)

    final_text = await dict_to_text(vacancy_values=values, type_descr=type_descr)

    return final_text


async def main_text():
    return "личный кабинет"


async def dict_to_text(vacancy_values: dict, type_descr: str) -> str:
    employer = vacancy_values['employer']
    work_type = vacancy_values['work_type']
    salary = vacancy_values['salary']
    min_age = f"Минимальный возраст: {vacancy_values['min_age']}\n" if vacancy_values['min_age'] is not None else ""
    min_exp = f"Минимальный опыт работы: {vacancy_values['min_exp']}\n" if vacancy_values['min_exp'] is not None else ""
    datetime = vacancy_values['datetime']
    descr = vacancy_values['s_dscr'] if type_descr == "short" else vacancy_values['l_dscr']

    final_text = (f"<b>{employer}</b>\n"
                  f"{work_type}\n"
                  f"{salary}\n"
                  f"{min_age}"
                  f"{min_exp}"
                  f"{datetime}\n"
                  f"{descr}")

    return final_text


async def get_vacancies_to_text(user_tg_id: int) -> str and int:
    if history := await get_history(user_tg_id):
        cur.execute(f"SELECT * FROM vacancies WHERE id not in ({', '.join(history)}) ORDER BY count_of_viewers ASC")
    else:
        cur.execute("SELECT * FROM vacancies ORDER BY count_of_viewers ASC")

    row = cur.fetchone()
    if row:

        vacancy_id: int = row[0]

        cur.execute("UPDATE vacancies SET count_of_viewers = count_of_viewers + 1 WHERE id = ?", (vacancy_id,))
        conn.commit()

        return await vacancy_to_text(row, "short"), vacancy_id
    else:
        return texts.no_vacancies_notification, -1


# async def get_description(id, dscr_type) -> str:
#     cur.execute(f"SELECT {dscr_type} FROM vacancies WHERE id = ?", (id,))
#     return cur.fetchone()[0]


async def add_like_vacancy(user_tg_id, vacancy_id) -> None:
    cur.execute("INSERT OR IGNORE INTO users_likes (user_tg_id, vacancy_id) VALUES (?, ?)", (user_tg_id, vacancy_id,))
    conn.commit()


async def del_like_vacancy(user_tg_id) -> None:
    cur.execute("DELETE FROM users_likes WHERE user_tg_id = ?", (user_tg_id,))
    conn.commit()


async def get_liked_vacancies(user_tg_id) -> list[tuple]:
    cur.execute("SELECT vacancies.* "
                "FROM users_likes "
                "JOIN vacancies ON users_likes.vacancy_id = vacancies.id "
                "WHERE users_likes.user_tg_id = ?", (user_tg_id,))
    return cur.fetchall()


async def get_created_vacancies(user_tg_id: int) -> list[tuple]:
    cur.execute("SELECT * FROM vacancies WHERE creator_tg_id = ?", (user_tg_id,))
    vacancies = cur.fetchall()
    return vacancies

