import hotelWorker
import sqlite3
import os
import time


dbcon = None
if os.path.isfile('cronhoteldb.db'):
    dbcon = sqlite3.connect('cronhoteldb.db')


def deduceNumTimes(taskid):
    cursor = dbcon.cursor()
    cursor.execute("UPDATE TaskTimes "
                   "SET NumTimes = NumTimes -1 "
                   "WHERE TaskId = (?)", (taskid, ))


def checkTasksToExecute(lastUpdated):
    with dbcon:
        cursor = dbcon.cursor()
        cursor.execute("SELECT Tasks.TaskId, Tasks.TaskName, Tasks.Parameter, TaskTimes.DoEvery  "
                       "FROM Tasks "
                       "INNER JOIN TaskTimes "
                       "ON TaskTimes.TaskId = Tasks.TaskId "
                       "WHERE TaskTimes.NumTimes != 0")
        tasks = cursor.fetchall()
        if len(tasks) <= 0:
            return False
        for task in tasks:
            if (lastUpdated % int(task[3])) == 0:
                hotelWorker.dohoteltask(str(task[1]), int(task[2]))  # tell worker to do the task
                deduceNumTimes(task[0])  # update number of times left to execute this task
        return True

if dbcon != None:
    start_time = time.time()
    curr_time = start_time
    lastUpdated = -1
    moretasks = True
    while moretasks:
        curr_time = time.time()
        newUpdated = int(curr_time - start_time)  # get time in round seconds
        if newUpdated != lastUpdated:  # if advanced a second
            lastUpdated = newUpdated  # update last round second
            moretasks = checkTasksToExecute(lastUpdated)  # run tasks and check if more work is due
    dbcon.close()
