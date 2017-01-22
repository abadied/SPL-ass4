import sqlite3
import time

def deduceNumTimes(cursor, taskname, parameter):
    cursor.execute("SELECT TaskId FROM Tasks WHERE TaskName=(?) AND Parameter=(?)", (taskname,parameter))
    taskid = cursor.fetchone()
    cursor.execute("UPDATE TaskTimes SET NumTimes = NumTimes -1 WHERE TaskId = (?)", taskid,)

def dohoteltask(taskname, parameter):
    dbcon = sqlite3.connect('cronhoteldb.db')
    dbcon.text_factory = bytes
    with dbcon:
        cursor = dbcon.cursor()
        if taskname == "wakeup":
            cursor.execute("SELECT FirstName,LastName FROM Residents WHERE RoomNumber=(?)", (parameter,))
            name = cursor.fetchone()
            
            deduceNumTimes(cursor,taskname,parameter)
            
            print_time = time.time()
            print name[0], name[1], "in room", parameter, "received a wakeup call at", print_time
            return print_time
        
        elif taskname == "breakfast":
            cursor.execute("SELECT FirstName,LastName FROM Residents WHERE RoomNumber=(?)", (parameter,))
            name = cursor.fetchone()
            
            deduceNumTimes(cursor,taskname,parameter)
            
            print_time = time.time()
            print name[0], name[1], "in room", parameter, "has been served breakfast at", print_time
            return print_time
        
        elif taskname == "clean":
            cursor.execute("SELECT * FROM Rooms")
            rooms = cursor.fetchall()
            
            deduceNumTimes(cursor,taskname,parameter)
            
            string_rooms = ""
            for room in rooms:
                string_rooms += str(room)
            
            print_time = time.time()
            print "Rooms ", string_rooms, " cleaned at ", print_time
            return print_time

dohoteltask("breakfast" , 112)
