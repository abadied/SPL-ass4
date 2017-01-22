import hotelWorker
import sqlite3
import os
import time

databaseexisted = os.path.isfile('cronhoteldb.db')
dbcon = sqlite3.connect('cronhoteldb.db')

with dbcon:
    cursor = dbcon.cursor()
   # print str(tasks[0][0]) #Test
    while databaseexisted:
        cursor.execute("SELECT * FROM TaskTimes WHERE NumTimes != 0")
        tasks = cursor.fetchall()
        if len(tasks) <= 0:
            break



