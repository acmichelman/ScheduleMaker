import sqlite3
import random
from pathlib import Path
from datetime import datetime
from enum import Enum

class Day(Enum):
    MON = 0
    TUE = 1
    WED = 2
    THU = 3
    FRI = 4
    SAT = 5
    SUN = 6

def test_days_off():
    days = []
    people = [
    {"name": "Maya",   "number": None},
    {"name": "Jordan", "number": None},
    {"name": "Sofia",  "number": None},
    {"name": "Ethan",  "number": None},
    {"name": "Avery",  "number": None},
    {"name": "Noah",   "number": None},
    {"name": "Liam",   "number": None},
    {"name": "Zoe",    "number": None},
    {"name": "Hannah", "number": None},
    {"name": "Carlos", "number": None},
    ]
    count = len(people)

    while count != 0:
        

    

