import sqlite3
import time


def getResident(cursor, roomid):
    cursor.execute("SELECT FirstName,LastName "
                   "FROM Residents "
                   "WHERE RoomNumber=(?)", (roomid,))
    return cursor.fetchone()


def dohoteltask(taskname, parameter):
    dbcon = sqlite3.connect('cronhoteldb.db')
    dbcon.text_factory = bytes
    with dbcon:
        cursor = dbcon.cursor()
        if taskname == "wakeup":
            name = getResident(cursor, parameter)
            
            print_time = time.time()
            print name[0], name[1], "in room", parameter, "received a wakeup call at", print_time
            return print_time
        
        elif taskname == "breakfast":
            name = getResident(cursor, parameter)
            
            print_time = time.time()
            print name[0], name[1], "in room", parameter, "has been served breakfast at", print_time
            return print_time
        
        elif taskname == "clean":
            cursor.execute("SELECT Rooms.RoomNumber "
                           "FROM Rooms "
                           "LEFT JOIN Residents "
                           "ON Rooms.RoomNumber = Residents.RoomNumber "
                           "WHERE Residents.FirstName IS NULL "
                           "ORDER BY Rooms.RoomNumber ASC")
            rooms = cursor.fetchall()
            
            string_rooms = ""
            for room in rooms:
                string_rooms += str(room[0]) + ", "
            
            print_time = time.time()
            print "Rooms", string_rooms[:-2], "cleaned at", print_time
            return print_time
    dbcon.commit()
    dbcon.close()

