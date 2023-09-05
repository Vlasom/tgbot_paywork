import sqlite3

conn = sqlite3.connect("database//database.db")
cur = conn.cursor()


async def close_db():
    conn.close()
