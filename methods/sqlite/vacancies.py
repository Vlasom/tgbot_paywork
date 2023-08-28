from methods.sqlite.users import db, cursor


async def save_vacancy(values: dict):


    cursor.execute("INSERT INTO vacancies (employer, work_type, salary, min_age, min_exp, datetime, s_dscr, l_dscr) "
                f"VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (*values.values(),))

    db.commit()
