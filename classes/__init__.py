from classes.Users import User
from classes.SqlConnection import SqlConnection
from classes.RedisCommands import RedisCommands
from classes.Vacancies import Vacancy, VacanciesCommands
from classes.DataBaseCommands import DatabaseCommands
from classes.Notifications import NotificationsSender, VacancyNotification

import sqlite3


_conn = sqlite3.connect("database//database.db")
_cur = _conn.cursor()
_sql_connection = SqlConnection(cur=_cur, conn=_conn)


redis_commands = RedisCommands()
db_commands = DatabaseCommands()
vac_notification = VacancyNotification()


vac_commands = VacanciesCommands(sql_connection=_sql_connection,
                                 db_commands=db_commands,
                                 redis_commands=redis_commands)


