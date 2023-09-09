from .processes_db import conn, cur


async def add_user(tg_id):
    cur.execute("INSERT OR IGNORE INTO users (tg_id) VALUES (?)", (int(tg_id),))
    conn.commit()
