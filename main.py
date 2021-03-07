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


def command_ur(command_line):
    line = command_line[2:].strip()
    arr = line.split("=")
    name = arr[1]
    output = "USER REPORT for {}".format(name)
    print("{:*^60s}".format(output))
    day = 0
    for checkout in checkouts:
        if checkout.student.student_name == name:
            days = start_date - checkout.due_date
            days = days.days
            if days > day:
                day = days
    if day > 5:
        day = 5
    penalty = penalties[day]
    if day !=0:
        print("        {} Curse: {}".format(name, penalty.curse))
    print("-------------------------CHECKOUTS--------------------------")
    lst = []
    for checkout in checkouts:
        if checkout.student.student_name == name:
            lst.append(checkout)
    lst.sort(key=lambda x: x.book.title)
    if len(lst) == 0:
        print("                       No checkouts.                        ")
    else:
        for checkout in lst:
            print("{:<35s}{:>25s}".format(checkout.book.title, checkout.due_date.strftime("%m/%d/%Y")))
    print()
    print("---------------------------HOLDS----------------------------")
    lst = []
    for title, items in holds.items():
        for item in items:
            if item[0].student_name == name:
                lst.append([title, item[0], item[1]])
    lst.sort(key=lambda x: x[0])
    if len(lst) == 0:
        print("                       No holds.                        ")
    else:
        for hold in lst:
            print("{:<35s}{:>25d}".format(hold[0], hold[2]))


def command_cr(command_line):
    print("***CURRENT CHECKOUT REPORT**************{}**********".format(
    start_date.strftime("%m/%d/%Y")))
    if len(checkouts) == 0:
        print("                   No Books Checked Out.                    ")
    print("{:<30}{:^20}{:>10}".format(
        "Book Title", "Student Name", "Due Date"))
    print("------------------------------------------------------------")
    checkouts.sort(key=lambda x: x.book.title)
    checkouts.sort(key=lambda x: x.student.student_name)
    checkouts.sort(key=lambda x: x.student.house)
    for checkout in checkouts:
        title = checkout.book.title
        if len(title)>30:
            title = title[0:30]
        print(checkout_report_format_string.format(title=title,
                                                   name=checkout.student.student_name,  due_date=checkout.due_date.strftime("%m/%d/%Y")))


def command_la(command_line):
    books = []
    titles = [item.book.title for item in checkouts]
    for book in book_collection.values():
        if book.title not in titles:
            books.append(book)
    books.sort(key=lambda x: x.title)
    print("Number of books in available: ", len(books))
    print("------------------------------------")
    for book in books:
        print("Title:", book.title)
        print("Author:", book.author)
        print("Date:", book.year_published)
        print("Subject:", book.subject)
        print("Section:", book.section)
        print("------------------------------------")



def command_dt(command_line):
    print("*******BOOKS DUE TODAY******************{}**********".format(
    start_date.strftime("%m/%d/%Y")))
    temp = []
    for checkout in checkouts:
        if checkout.due_date == start_date:
            temp.append(checkout)
    temp.sort(key=lambda x: x.book.title)
    if len(temp) == 0:
        print("                    No books due today.                     ")
    for item in temp:
        print(due_today_format_string.format(
            title=item.book.title, name=item.student.student_name))


def command_ad(command_line):
    global start_date
    start_date = start_date + timedelta(days=1)
    month = start_date.month
    day = start_date.day
    year = start_date.year
    start_date = datetime(year, month, day)
    weekDays = ("Monday", "Tuesday", "Wednesday",
                "Thursday", "Friday", "Saturday", "Sunday")
    month_names = ["January",  "February",  "March",  "April",   "May",    "June",  "July",    "August",
                   "September", "October", "November", "December"]
    thisXMasDay = start_date.weekday()
    thisXMasDayAsString = weekDays[thisXMasDay]
    print("*************HOGWARTS LIBRARY MANAGEMENT SYSTEM*************")
    output = "{} {:02d}, {} {}".format(thisXMasDayAsString,day, month_names[month-1], year)
    print("{:*^60s}".format(output))


def command_cb(command_line):
    arr = command_line[2:].strip().split(",")
    data = {}
    for item in arr:
        key, value = item.split("=")
        data[key] = value
    if data["student_name"] not in library_members:
        print( data["student_name"] , "is not a registered library member.")
        return
    if data["title"] not in book_collection:
        print("{} not in inventory.".format(data["title"]))
        return
    book = book_collection[data["title"]]
    if book.section == "Restricted":
        if "pass_code" not in data:
            print(book.title, "is a Restricted book, and requires a pass code to be checked out.")
            return
        else:
            if data["pass_code"] not in library_passcodes:
                print("{} is not a valid pass code.".format(data["pass_code"]))
                return
    titles = [item.book.title for item in checkouts]
    if book.title in titles:
        print("{} is currently unavailable to be checked out.".format(book.title))
        return 
    student = library_members[data["student_name"]]
    number_of_days = int(data.get("number_of_days", 14))
    due_date = start_date + timedelta(days=number_of_days)
    checkout = Checkout(book, student, due_date)
    checkouts.append(checkout)

def command_sd(command_line):
    global start_date
    line = command_line[2:].strip()
    arr = line.split("/")
    month = int(arr[0])
    day = int(arr[1])
    year = int(arr[2])
    start_date = datetime(year, month, day)
    weekDays = ("Monday", "Tuesday", "Wednesday",
                "Thursday", "Friday", "Saturday", "Sunday")
    month_names = ["January",  "February",  "March",  "April",   "May",    "June",  "July",    "August",
                   "September", "October", "November", "December"]
    thisXMasDay = start_date.weekday()
    thisXMasDayAsString = weekDays[thisXMasDay]
    print("*************HOGWARTS LIBRARY MANAGEMENT SYSTEM*************")
    output = "{} {:02d}, {} {}".format(thisXMasDayAsString,day, month_names[month-1], year)
    print("{:*^60s}".format(output))

def command_or():
    print("********OVERDUE REPORT*************{}*******# Days**".format(start_date.strftime("%m/%d/%Y")))
    overdue_checkouts = []
    for checkout in checkouts:
        if checkout.due_date < start_date:
            overdue_checkouts.append(checkout)
    if len(overdue_checkouts) == 0:
        print("                  No books overdue today.                   ")
        return
    overdue_checkouts.sort(key=lambda x: x.book.title)
    for checkout in overdue_checkouts:
        name = checkout.student.student_name
        if len(name) > 15:
            name = name[0:15]
        print("{title:<35}{name:^16}{days:^4}".format(title=checkout.book.title, name=name, 
            days=(start_date- checkout.due_date).days))
    print()

def command_rb(line):
    line = line[3:]
    title = line.split("=")[1]
    if title not in book_collection:
        print("Invalid Return Request for {}.".format(title))
        return
    else:
        checkout = None
        for item in checkouts:
            if item.book.title == title:
                checkout = item
        if checkout is not None:
            checkouts.remove(checkout)
            if checkout.book.title in holds:
                student, number_of_days = holds[checkout.book.title].pop(0)
                due_date = start_date + timedelta(days=number_of_days)
                item = Checkout(checkout.book, student, due_date)
                checkouts.append(item)
        else:
            print("Invalid Return Request for {}.".format(title))



def command_rh(command_line):
    arr = command_line[2:].strip().split(",")
    data = {}
    for item in arr:
        key, value = item.split("=")
        data[key] = value
    if data["student_name"] not in library_members:
        print( data["student_name"] , "is not a registered library member.")
        return
    if data["title"] not in book_collection:
        print("{} not in inventory.".format(data["title"]))
        return
    for checkout in checkouts:
        if checkout.book.title == data["title"] and checkout.student.student_name == data["student_name"]:
            print("{} currently has checked out {}.".format(checkout.student.student_name, checkout.book.title))
            return

    reservations = []
    for title, item_lst in holds.items():
        for item in item_lst:
            reservations.append([title, item[0], item[1]])
    for r in reservations:
        if r[0] == data["title"] and r[1].student_name == data["student_name"]:
             print("{} has already requested a hold for {}.".format(r[1].student_name, r[0]))
             return 

    book = book_collection[data["title"]]
    titles = [item.book.title for item in checkouts]
    if book.title  not in titles:
        print("{} is available to be checked out. Use command to checkout book.".format(book.title))
        return
    student = library_members[data["student_name"]]
    number_of_days = int(data.get("number_of_days", 14))
    checkout = [student, number_of_days]
    if book.title not in holds:
        holds[book.title] = [checkout]
    else:
        holds[book.title].append(checkout)


def command_hr():
    print("*****HOLD REQUEST REPORT****************{}**********".format( start_date.strftime("%m/%d/%Y")))
    print("Student Name                         # of Days Requested    ")
    print("------------------------------------------------------------")
    if len(holds) == 0:
        print("                    No Holds Requested.                     ")
    else:
        
        titles = list(holds.keys())
        titles.sort()
        for title in titles:
            print(title)
            lst = holds[title]
            # lst.sort(key=lambda x: x[0].student_name, reverse=True)
            for item in lst:
                print("   {name:<30}{number_of_days:^27}".format(name=item[0].student_name, number_of_days=item[1]))
            print("------------------------------------------------------------")


def command_nb(line):
    '''
    add new book to the library
    '''
    line = line[2:].strip()
    lst = line.split(",")
    data = {}
    for item in lst:
        tokens = item.split("=")
        data[tokens[0]] = tokens[1]
    book = Book(data["title"], 
                data["author"],
                data["year_published"], 
                data["subject"], 
                data["section"])
    if data["title"] not in book_collection:
        book_collection[data["title"]] = book
    else:
        print("{} already present.".format(data["title"]))


def command_li():
    '''
    list all the books in inventory
    '''
    print("*********************LIBRARY INVENTORY**********************")
    print("Number of books available: ", len(book_collection))
    print("------------------------------------")
    titles = list(book_collection.keys())
    titles.sort()
    for title in titles:
        book = book_collection[title]
        print("Title:", book.title)
        print("Author:", book.author)
        print("Date:", book.year_published)
        print("Subject:", book.subject)
        print("Section:", book.section)
        print("------------------------------------")


def command_db(line):
    '''
    delete book from the library
    '''
    line = line[3:].strip()
    title = line.split("=")[1]
    if title not in book_collection:
        print("{} Not Found. Cannot be deleted.".format(title))
    else:
        del book_collection[title]
    pos = -1
    for i in range(len(checkouts)):
        if checkouts[i].book.title==title:
            pos = i
    if pos!=-1:
        checkouts.remove(checkouts[pos])
    if title in holds:
        del holds[title]


def command_fb(line):
    '''
    search the book by title
    '''
    line = line[2:].strip()
    print("************************BOOK SEARCH*************************")
    if len(line) == 0:
        # no search criteria
        print("Number of books found: ", len(book_collection))
        titles = list(book_collection.keys())
        titles.sort()
        print("------------------------------------")
        for title in titles:
            book = book_collection[title]
            print("Title:", book.title)
            print("Author:", book.author)
            print("Date:", book.year_published)
            print("Subject:", book.subject)
            print("Section:", book.section)
            print("------------------------------------")
    else:
        lst = line.split(",")
        data = {}
        for item in lst:
            tokens = item.split("=")
            data[tokens[0]] = tokens[1]
        records = list(book_collection.values())
        for key, value in data.items():
            if key == "subject":
                records = [item for item in records if item.subject == value]
            if key == "section":
                records = [item for item in records if item.section == value]
            if key == "title":
                records = [item for item in records if item.title == value]
            if key == "year_published":
                records = [item for item in records if item.year_published == value]
            if key == "author":
                records = [item for item in records if item.author == value]
        records.sort(key=lambda x: x.title)
        if len(records) == 0:
            print("No Books Found.")
        else:
            print("Number of books found: ", len(records))
            print("------------------------------------")
            for book in records:
                print("Title:", book.title)
                print("Author:", book.author)
                print("Date:", book.year_published)
                print("Subject:", book.subject)
                print("Section:", book.section)
                print("------------------------------------")


def command_as(line):
    '''
    Add a new student to the library
    '''
    line = line[3:]
    lst = line.split(",")
    data = {}
    for item in lst:
        tokens = item.split("=")
        data[tokens[0]] = tokens[1]
    student = Student(data["student_name"], data["house"], [])
    if data["student_name"] not in library_members:
        library_members[data["student_name"]] = student
    else:
        print("{} is already present.".format(data["student_name"]))


def command_lm():
    '''
    list all the library memebers
    '''
    print("**********************LIBRARY MEMBERS***********************")
    houses = list(house_penalties.keys())
    houses.sort()
    for house in houses:
        print(house + ":")
        students = []
        for student in library_members.values():
            if student.house == house:
                students.append(student)
        if len(students) == 0:
            print("{:>30s}".format("No Registered Members"))
        else:
            students.sort(key=lambda x: x.student_name)
            for student in students:
                print("{:>30s}".format(student.student_name))
    

def command_pl(line):
    print(line[3:])


if __name__ == "__main__":
    fname = sys.argv[1]
    # fname = "Stage5Commands.txt"
    hogwarts_library(open(fname).read())
