import timeit
import asyncio
from methods.sqlite.processes_db import conn, cur


# async def add_user(tg_id: int, username: str, fullname: str) -> None:
#     cur.execute("INSERT OR IGNORE INTO users (tg_id, username, fullname, active) VALUES (?, ?, ?, ?)", (int(tg_id), username, fullname, 1))
#     cur.execute("UPDATE users SET username = ?, fullname = ?, active = ? WHERE tg_id = ?", (username, fullname, 1, tg_id))
#     conn.commit()
#
#
# def a():
#     asyncio.run(add_user(555, "ww", "22"))
#
# time = timeit.timeit('a()', globals={"a": a}, number=1000)
# print(time)


# INSERT OR IGNORE 1.8867482000496238
# INSERT OR REPLACE  12.485583700006828

# async def add_user(tg_id: int, username: str, fullname: str) -> None:
#     cur.execute("INSERT OR IGNORE INTO users (tg_id, username, fullname) VALUES (?, ?, ?)", (int(tg_id), username, fullname))
#     cur.execute("UPDATE users SET username = ?, fullname = ? WHERE tg_id = ?", (username, fullname, tg_id))
#     conn.commit()   1.7756901000393555

# сумма времени 2 опреаций не 3,6 из-за того что они проходят в рамках одной транзакции conn.commit()


async def create_table(name_table: str):
    cur.execute(f"CREATE TABLE IF NOT EXISTS [{name_table}] ("
                "user_tg_id INTEGER PRIMARY KEY UNIQUE NOT NULL,"
                "status_notification TEXT DEFAULT waiting NOT NULL,"
                "error TEXT)")
    print(cur.fetchone())
    print(bool(cur.fetchone()))

asyncio.run(create_table("12"))


