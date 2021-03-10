############ IMPORT HERE #############

############## IMPLEMENT FUNCTIONS HERE ############
from utilities import *
from datetime import datetime
from datetime import timedelta
import sys

book_collection = {}
library_members = {}
checkouts = []
holds = {}
start_date = None


def hogwarts_library(text):
    global start_date
    commands = text.splitlines()
    for command_line in commands:
        command_line = command_line.strip()
        if command_line != "":
            command = command_line[0:2].upper()
            if command == "PL":
                command_pl(command_line)
            elif command == "NB":
                command_nb(command_line)
            elif command == "LI":
                command_li()
            elif command == "DB":
                command_db(command_line)
            elif command == "FB":
                command_fb(command_line)
            elif command == "AS":
                command_as(command_line)
            elif command == "LM":
                command_lm()
            elif command == "SD":
                command_sd(command_line)
            elif command == "CB":
                command_cb(command_line)
            elif command == "CR":
                command_cr(command_line)
            elif command == "LA":
                command_la(command_line)
            elif command == "DT":
                command_dt(command_line)
            elif command == "AD":
                command_ad(command_line)
            elif command == "RH":
                command_rh(command_line)
            elif command == "HR":
                command_hr()
            elif command == "RB":
                command_rb(command_line)
            elif command == "OR":
                command_or()
            elif command == "UR":
                command_ur(command_line)
            elif command == "DR":
                command_dr(command_line)
            elif command == "**":
                pass


def command_dr(command_line):
    line = command_line[2:].strip()
    arr = line.split(",")
    data = {}
    for item in arr:
        tokens = item.split("=")
        data[tokens[0]] = tokens[1]
    start_time_str = data["start_date"]
    end_time_str = data["end_date"] 

    arr = start_time_str.split("/")
    month = int(arr[0])
    day = int(arr[1])
    year = int(arr[2])
    start_time = datetime(year, month, day)

    arr = end_time_str.split("/")
    month = int(arr[0])
    day = int(arr[1])
    year = int(arr[2])
    end_time = datetime(year, month, day)

    lst = []
    for checkout in checkouts:
        due_date = checkout.due_date
        if due_date >= start_time and due_date <= end_time:
            lst.append(checkout)
    print("***BOOKS DUE BETWEEN********{} to {}********".format(start_time_str, end_time_str))
    if len(lst) == 0:
        print("{:^60s}".format("No books due for the given dates."))
    else:
        lst.sort(key=lambda x: x.book.title)
        for item in lst:
            print(due_report_format_string.format(title=item.book.title, name=item.student.student_name))
        print()


def command_pl(line):
    print(line[3:])


if __name__ == "__main__":
    fname = sys.argv[1]
    # fname = "Stage5Commands.txt"
    hogwarts_library(open(fname).read())
