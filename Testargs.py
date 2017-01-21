import sqlite3
import os
import sys


def main(args):
    inputconfilname = args[1]
    print(inputconfilname)
    with open(inputconfilname) as inputfile:
        index = 0
        for line in inputfile:
            input_array = line.split(',')
            print(input_array[2])
            if len(input_array) < 3:
                print(len(input_array))
            

if __name__ == '__main__':
    main(sys.argv)