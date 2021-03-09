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



def command_pl(line):
    print(line[3:])


if __name__ == "__main__":
    fname = sys.argv[1]
    # fname = "Stage5Commands.txt"
    hogwarts_library(open(fname).read())
