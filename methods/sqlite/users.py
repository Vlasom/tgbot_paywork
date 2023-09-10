from .processes_db import conn, cur


async def add_user(tg_id: int, username: str, fullname: str) -> None:
    cur.execute("INSERT OR IGNORE INTO users (tg_id, username, fullname, active) VALUES (?, ?, ?, ?)",
                (int(tg_id), username, fullname, 1))
    cur.execute("UPDATE users SET username = ?, fullname = ?, active = ? WHERE tg_id = ?",
                (username, fullname, 1, tg_id))
    conn.commit()


async def cheak_table(name_table: int) -> bool:
    cur.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name= {name_table}")
    return bool(cur.fetchone())


async def create_table(name_table: int, creator) -> None:
    cur.execute(f"CREATE TABLE IF NOT EXISTS [{name_table}] ("
                "user_tg_id INTEGER PRIMARY KEY UNIQUE NOT NULL,"
                "status_notification TEXT DEFAULT waiting NOT NULL,"
                "error TEXT)")
    cur.execute(f"INSERT INTO [{name_table}] (user_tg_id) "
                f"SELECT tg_id FROM users WHERE active = 1 AND notification_status = 1 AND tg_id <> {creator}")
    conn.commit()

async def delete_table(name_table: int) -> None:
    cur.execute(f"DROP TABLE [{name_table}]")
    conn.commit()


async def get_users_with_notification(name_table: int) -> list:
    cur.execute(f"SELECT user_tg_id FROM [{name_table}] WHERE status_notification = 'waiting'")
    res = [id[0] for id in cur.fetchall()]
    return res


async def update_status(id_vacancy_notification: int, user_tg_id: int, statuse, description) -> None:
    cur.execute(f"UPDATE [{id_vacancy_notification}] SET status_notification = '{statuse}', error = '{description}' WHERE user_tg_id = {user_tg_id}")
    conn.commit()

async def update_active(user_tg_id: int) -> None:
    cur.execute(f"UPDATE user SET activa = 0 WHERE tg_id = {user_tg_id}")
    conn.commit()