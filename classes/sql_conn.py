import sqlite3

from classes.SqlConnection import SqlConnection

conn = sqlite3.connect("database//database.db")
cur = conn.cursor()
sql_connection = SqlConnection(cur=cur, conn=conn)