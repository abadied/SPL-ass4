
import sqlite3
import os


databaseexisted = os.path.isfile('cronhoteldb.db')
dbcon = sqlite3.connect('cronhoteldb.db')

with dbcon:
    cursor = dbcon.cursor()
    cursor.execute("SELECT * FROM TaskTimes")
    print str(cursor.fetchall())