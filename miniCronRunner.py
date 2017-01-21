import hotelWorker
import sqlite3
import os


databaseexisted = os.path.isfile('cronhoteldb.db')
dbcon = sqlite3.connect('cronhoteldb.db')

with dbcon:
    cursor = dbcon.cursor()
    cursor.execute("SELECT TaskId FROM TaskTimes WHERE NumTimes != (?)",(0))

    if databaseexisted:
