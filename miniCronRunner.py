import hotelWorker
import sqlite3
import os
import time


databaseexisted = os.path.isfile('cronhoteldb.db')
dbcon = sqlite3.connect('cronhoteldb.db')


def checkTasksToExecute(lastUpdated):
    with dbcon:
        cursor = dbcon.cursor()
        cursor.execute("SELECT * FROM TaskTimes WHERE NumTimes != 0")
        tasks = cursor.fetchall()
        if len(tasks) <= 0:
            return False
        for task in tasks:
            if (lastUpdated % int(task[1])) == 0:
                cursor.execute("SELECT * FROM Tasks WHERE TaskId = (?)",(task[0],))
                tasknameparam = cursor.fetchone()
                hotelWorker.dohoteltask(str(tasknameparam[1]), int(tasknameparam[2]))
        return True


start_time = time.time()
curr_time = start_time
lastUpdated = -1
moretasks = True
while moretasks:
    curr_time = time.time()
    newUpdated = int(curr_time - start_time)
    if newUpdated != lastUpdated:
        lastUpdated = newUpdated
        moretasks = checkTasksToExecute(lastUpdated)

