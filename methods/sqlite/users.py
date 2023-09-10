from .processes_db import conn, cur


async def add_user(tg_id: int, username: str, fullname: str) -> None:
    cur.execute("INSERT OR IGNORE INTO users (tg_id, username, fullname, active) VALUES (?, ?, ?, ?)", (int(tg_id), username, fullname, 1))
    cur.execute("UPDATE users SET username = ?, fullname = ?, active = ? WHERE tg_id = ?", (username, fullname, 1, tg_id))
    conn.commit()




