import sqlite3 as sq

db = sq.connect("database//database.db")
cursor = db.cursor()


async def add_user(tg_id):
    cursor.execute("INSERT OR IGNORE INTO users (tg_id) VALUES (?)", (int(tg_id),))
    db.commit()
