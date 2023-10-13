import sqlite3


class SqlConnection:

    def __init__(self, cur: sqlite3, conn: sqlite3):
        self.cur: sqlite3 = cur
        self.conn: sqlite3 = conn

    async def close_conn(self):
        self.conn.close()
