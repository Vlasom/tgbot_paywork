import sqlite3
from methods.sqlite.sql_class import *
from methods.sqlite.user_class import *

_conn = sqlite3.connect("database//database.db")
_cur = _conn.cursor()

_sql_connection = SqlConnection(cur=_cur, conn=_conn)

redis_commands = RedisCommands()
db_commands = DatabaseCommands(sql_connection=_sql_connection)

vac_commands = VacanciesCommands(sql_connection=_sql_connection,
                                 db_commands=db_commands,
                                 redis_commands=redis_commands)

user_commands = UserCommands(sql_connection=_sql_connection)

vac_notification = VacancyNotification(sql_connection=_sql_connection)
