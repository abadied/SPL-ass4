import sqlite3
import os
import sys


def main(args):
    databaseexisted = os.path.isfile('cronhoteldb.db')
    dbcon = sqlite3.connect('cronhoteldb.db')
    with dbcon:
        cursor = dbcon.cursor()
        if not databaseexisted:
            inputconfilname = args[1]
            if (not os.path.isfile(inputconfilname)):  # check if file exists
                return
            # create table TaskTimes
            cursor.execute("CREATE TABLE TaskTimes (TaskId INTEGER PRIMARY KEY NOT NULL ,DoEvery INTEGER NOT NULL,NumTimes INTEGER NOT NULL)")

            # create table Tasks
            cursor.execute("CREATE TABLE Tasks (TaskId INTEGER NOT NULL REFERENCES TaskTimes(TaskId) ,TaskName TEXT NOT NULL,Parameter INTEGER)")
                           
            # create table Rooms
            cursor.execute("CREATE TABLE Rooms (RoomNumber INTEGER PRIMARY KEY NOT NULL)")
            
            # create table Residents
            cursor.execute("CREATE TABLE Residents (RoomNumber INTEGER NOT NULL REFERENCES Rooms(RoomNumber), FirstName TEXT NOT NULL, LastName TEXT NOT NULL)")
                           
            

            with open(inputconfilname) as inputfile:
                index = 0
                for line in inputfile:
                    input_array = line.split(',')
                    if input_array[0] == "wakeup" :
                        cursor.execute("INSERT INTO TaskTimes VALUES(? , ? ,?)", (index, input_array[1], input_array[3]))
                        cursor.execute("INSERT INTO Tasks VALUES(? , ? ,?)",(index, input_array[0], input_array[2]))
                        index += 1
                        
                    elif input_array[0] == "room":
                        cursor.execute("INSERT INTO Rooms VALUES(?)", (input_array[1],))
                        if len(input_array)  > 3:
                            cursor.execute("INSERT INTO Residents VALUES(? , ? , ?)", (input_array[1],input_array[2], input_array[3]))
                                                                                       
			
                    elif input_array[0] == "breakfast" :
                        cursor.execute("INSERT INTO TaskTimes VALUES(? , ? ,?)", (index, input_array[1], input_array[3]))
                        cursor.execute("INSERT INTO Tasks VALUES(? , ? ,?)",(index, input_array[0], input_array[2]))
                        index += 1

                    elif input_array[0] == "clean":
                        cursor.execute("INSERT INTO TaskTimes VALUES(? , ? ,?)", (index, input_array[1], input_array[2]))
                        cursor.execute("INSERT INTO Tasks VALUES(? , ? ,?)",(index, input_array[0], 0))
                        index += 1

if __name__ == '__main__':
    main(sys.argv)



