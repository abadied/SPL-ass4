import sqlite3
import time


def dohoteltask(taskname, parameter):
    dbcon = sqlite3.connect('cronhoteldb.db')
    with dbcon:
        cursor = dbcon.cursor()
        if taskname == "wakeup":
            cursor.execute("SELECT FirstName FROM Residents WHERE RoomNumber=(?)", (parameter))
            firstname = cursor.fetchone()
            cursor.execute("SELECT LastName FROM Residents WHERE RoomNumber=(?)", (parameter))
            lastname = cursor.fetchone()
            print lastname
            cursor.execute("SELECT TaskId FROM Tasks WHERE TaskName=(?) AND Parameter=(?)", (taskname,parameter))
            taskid = cursor.fetchone()
            cursor.execute("UPDATE TaskTimes SET NumTimes = NumTimes -1 WHERE TaskId = (?)" , (taskid,))
            #check if writen correctly
            print_time = time.time()
            print(firstname, " ", lastname, " in room", parameter , " received a wakeup call at ", print_time)
            return print_time
        elif taskname == "breakfast":
            cursor.execute("SELECT FirstName FROM Residents WHERE RoomNumber=(?)", (parameter))
            firstname = cursor.fetchone()
            cursor.execute("SELECT LastName FROM Residents WHERE RoomNumber=(?)", (parameter))
            lastname = cursor.fetchone()
            cursor.execute("SELECT TaskId FROM Tasks WHERE TaskName=(?) AND Parameter=(?)", (taskname, parameter))
            taskid = cursor.fetchone()
            cursor.execute("UPDATE TaskTimes SET NumTimes = NumTimes -1 WHERE TaskId = (?)", (taskid))
            print_time = time.time()
            print(firstname, " ", lastname, " in room", parameter, " has been served breakfast at ", print_time)
            return print_time
        elif taskname == "clean":
            cursor.execute("SELECT * FROM Rooms")
            rooms = cursor.fetchall()
            cursor.execute("SELECT TaskId FROM Tasks WHERE TaskName=(?) AND Parameter=(?)", (taskname, parameter))
            taskid = cursor.fetchone()
            cursor.execute("UPDATE TaskTimes SET NumTimes = NumTimes -1 WHERE TaskId = (?)", (taskid))
            string_rooms = ""
            for room in rooms:
                string_rooms += str(room)
            print_time = time.time()
            print("Rooms ", string_rooms, " cleaned at ", print_time)
            return print_time

dohoteltask("clean" , 0)
