from .processes_db import conn, cur
import sqlite3


async def add_user(tg_id: int, username: str, fullname: str) -> None:
    cur.execute("INSERT OR IGNORE INTO users (tg_id, username, fullname, active) VALUES (?, ?, ?, ?)",
                (int(tg_id), username, fullname, 1))
    cur.execute("UPDATE users SET username = ?, fullname = ?, active = ? WHERE tg_id = ?",
                (username, fullname, 1, tg_id))
    conn.commit()


class ProcessDbNotification:
    def __init__(self, conn: sqlite3.connect, cur: conn.cursor):
        self.conn = conn
        self.cur = cur

    async def check_table(self, name_table: int) -> bool:
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name= ?", (name_table,))
        return bool(cur.fetchone())

    async def create_table(self, name_table, creator) -> None:

        cur.execute(f"CREATE TABLE IF NOT EXISTS [{name_table}] ("
                    "user_tg_id INTEGER PRIMARY KEY UNIQUE NOT NULL,"
                    "status_notification TEXT DEFAULT waiting NOT NULL,"
                    "error TEXT)")
        cur.execute(f"INSERT INTO [{name_table}] (user_tg_id) "
                    "SELECT tg_id FROM users WHERE active = 1 AND notification_status = 1 AND tg_id <> ?", (creator,))
        conn.commit()

    async def delete_table(self, name_table) -> None:
        cur.execute(f"DROP TABLE [{name_table}]")
        conn.commit()

    async def get_users_with_notification(self, name_table) -> list:
        cur.execute(f"SELECT user_tg_id FROM [{name_table}] WHERE status_notification = 'waiting'")
        res = [id[0] for id in cur.fetchall()]
        return res

    async def update_status(self, name_table, user_tg_id: int, statuse, description) -> None:
        cur.execute(
            f"UPDATE [{name_table}] SET status_notification = '{statuse}', error = '{description}' WHERE user_tg_id = {user_tg_id}")
        conn.commit()

    async def update_active(self, user_tg_id: int) -> None:
        cur.execute("UPDATE users SET active = 0 WHERE tg_id = ?", (user_tg_id,))
        conn.commit()


async def on_nitifi_in_db(user_tg_id: int) -> None:
    cur.execute("UPDATE users SET notification_status = 1 WHERE tg_id = ?", (user_tg_id,))
    conn.commit()


async def off_nitifi_in_db(user_tg_id: int) -> None:
    cur.execute("UPDATE users SET notification_status = 0 WHERE tg_id = ?", (user_tg_id,))
    conn.commit()


process_db_notifi = ProcessDbNotification(conn, cur)