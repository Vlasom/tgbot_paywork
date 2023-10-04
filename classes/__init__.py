from classes.Users import User
from classes.Vacancies import Vacancy
from classes.SqlConnection import SqlConnection
from classes.RedisCommands import RedisCommands
from classes.VacanciesCommands import VacanciesCommands
from classes.DataBaseCommands import DatabaseCommands
from classes.Notifications import NotificationsSender, VacancyNotification
from classes.sql_conn import sql_connection

redis_commands = RedisCommands()
db_commands = DatabaseCommands()
vac_notification = VacancyNotification()

vac_commands = VacanciesCommands(sql_connection=sql_connection,
                                 db_commands=db_commands,
                                 redis_commands=redis_commands)
