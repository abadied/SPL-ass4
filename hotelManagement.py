import sqlite3
import os
import sys


def main(args):
    databaseexisted = os.path.isfile("cronhoteldb.db")
    dbcon = sqlite3.connect("cronhoteldb.db")
    with dbcon:
        cursor = dbcon.cursor()
        if not databaseexisted:
            inputconfilname = args[1]
            if (not os.path.isfile(inputconfilname)):  # check if file exists
                return
            cursor.execute("CREATE TABLE TaskTimes (TaskId integer PRIMARY KEY NOT NULL,"
                           " DoEvery integer NOT NULL,NumTimes integer NOT NULL)")
            # create table TaskTimes
            cursor.execute("CREATE TABLE Tasks (TaskId integer NOT NULL REFERENCES TaskTimes(TAskId),"
                           " TaskName text NOT NULL,Parameter integer)")
            # create table TaskTimes
            cursor.execute("CREATE TABLE Rooms (RoomNumber integer PRIMARY KEY NOT NULL)")
            # create table Rooms
            cursor.execute("CREATE TABLE Residents (RoomNumber integer NOT NULL REFERENCES Rooms(RoomNumber),"
                           " FirstName text NOT NULL, LastName text NOT NULL)")
            # create table Residents

            with open(inputconfilname) as inputfile:
                index = 0
                for line in inputfile:
                    input_array = line.split(',')
                    if input_array[0] == "room":
                        cursor.execute("INSERT INTO Rooms VALUES(?)", (input_array[1]))
                        if input_array[2] and not input_array.isspace():
                            cursor.execute("INSERT INTO Residents VALUES(? , ? , ?)", (input_array[1],
                                                                                       input_array[2], input_array[3]))

                    if input_array[0] == "breakfast" or "wakeup":
                        cursor.execute("INSERT INTO TasksTimes VALUES(? , ? ,?)", (index, input_array[1], input_array[3]))
                        cursor.execute("INSERT INTO Tasks VALUES(? , ? ,?)",(index, input_array[0], input_array[2]))
                        index += 1
                    if input_array[0] == "clean":
                        cursor.execute("INSERT INTO TasksTimes VALUES(? , ? ,?)", (index, input_array[1], input_array[2]))
                        cursor.execute("INSERT INTO Tasks VALUES(? , ? ,?)",(index, input_array[0], 0))
                        index += 1

if __name__ == '__main__':
    main(sys.argv)



