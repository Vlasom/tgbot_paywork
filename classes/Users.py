class User:
    def __init__(self, tg_id: int, username: str = None, fullname: str = None):
        self.tg_id = tg_id
        self.username = username
        self.fullname = fullname



"""
class UserCommands:
    def __init__(self, sql_connection: SqlConnection):
        self.sql_conn = sql_connection

    async def add_user_to_db(self, user: User):
        # сделать возможнсть получать из аргумента пользователя которому тд и тп
        self.sql_conn.cur.execute("INSERT OR IGNORE "
                                  "INTO users (tg_id, username, fullname, active) "
                                  "VALUES (?, ?, ?, ?)",
                                  (user.tg_id, user.username, user.fullname, 1))

        self.sql_conn.cur.execute("UPDATE users "
                                  "SET username = ?, fullname = ?, active = ? "
                                  "WHERE tg_id = ?",
                                  (user.username, user.fullname, 1, user.tg_id))

        self.sql_conn.conn.commit()

"""