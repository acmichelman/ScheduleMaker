from pathlib import Path
import re
import sqlite3
import logging
from datetime import datetime

from .. import clear_screen, main_menu

from ..db import DB_PATH, ensure_db_dir


logging.basicConfig(
    filename='logging_info.log', 
    level = logging.DEBUG,
    format='%(asctime)s:%(levelname)s:%(filename)s:%(funcName)s:%(message)s')

#   SQL Connect
def add_lifeguard_to_db(first_name: str, last_name: str, rank: str, date_promoted: str, eval_score: int, can_schedule: int) -> bool:

    #   Returns True if a new row was inserted, False if the name already existed.
    
    with sqlite3.connect(DB_PATH) as con:
        cur = con.cursor()
        #   This will try to insert. If the unique constraint is, it does nothing.
        cur.execute("""INSERT INTO Employees 
                    (FirstName, LastName, EmployeeRank, DatePromoted, EvaluationScore, CanSchedule)
                    VALUES (?, ?, ?, ?, ?, ?)
                    ON CONFLICT(FirstName, LastName) DO NOTHING;
                    """, (first_name, last_name, rank, date_promoted, eval_score, can_schedule))
        con.commit()
        if cur.rowcount == 1:
            return -1 # SQLite Autoincrement will assign a # between 1 - 9223372036854775807. So -1 will be our indication that its a new value cause 0 is if its false.
            #return cur.rowcount # 1 meaning true dumb ass
        #elif cur.rowcount == 0: #!!! It will return 0 if it doesnt add employee or find a match. !!!
        #    return 0

        #   Checks if employee has already been added
        else:
            cur.execute("""SELECT EmployeeID FROM Employees
                        WHERE FirstName = ? AND LastName = ?
                        LIMIT 1;
                        """, (first_name, last_name))
            row = cur.fetchone()
            return row
        #   return cur.rowcount == 1 # If its True[1] then return its inserted. If False[0] if its skipped
    
def menu_options():
    print("\nMenu Options")
    print("Add[1] \nBack[2]")

def add_lifeguard():
    #   Add a lifeguard to the system.
    clear_screen.clear_screen()
    print("Welcome to Add Lifeguard page")
    menu_options()

    running = True
    
    while running:
        answered_rank = False
        answered_promotion_date = False
        answered_proper_rank = False
        ans = input("> ").strip()

        if ans.lower() == "add" or ans == "1":
            print("Please enter employee 'First Name', 'Last Name', 'Rank', 'Date promoted if employee is a promoted guard', 'Evaluation Score', and 'If the employee can be scheduled'")

            print("First Name: ")
            first_name = input().strip()

            print("Last Name: ")
            last_name = input().strip()

            #   Rank will only take valid lifeguard rank
            print("Rank. LG for unpromoted guard. SG for Senior Guard. LT for Lieutenant. SL for Senior Lieutenant: ")
            while answered_rank == False:
                rank = input().strip().lower()
                if rank == "lg" or rank == "sg" or rank == "lt" or rank == "sl":
                    if rank == "lg":
                        rank = "lifeguard"
                    elif rank == "sg":
                        rank = "senior guard"
                    elif rank == "lt":
                        rank = "lieutenant"
                    elif rank == "sl":
                        rank = "senior lieutenant"
                    answered_rank = True
                elif rank == "lifeguard" or rank == "senior guard" or rank == "lieutenant" or rank == "senior lieutenant":
                    answered_rank = True
                else:
                    print("LG for unranked lifeguard, SG for senior guard, LT for lieutenant, SL for senior lieutenant \nPlease enter a valid rank.: ")
            
            #   This way is probally skitzo but fuck it we ballin
            #   datetime.striptime should strip ans into proper MM/DD/YYY form to be stored. Need to try except to do but could change to if for formatting sake
            if rank != "lifeguard":
                print("Date promoted (MM/DD/YYYY): ")
                while answered_promotion_date == False:
                    answered_promotion_date = True
                    date_promoted = input().strip()
                    try:
                        datetime.strptime(date_promoted, "%m/%d/%Y")
                    except ValueError:
                        print("Invalid date. Please use MM/DD/YYYY: ")
                        answered_promotion_date = False
            else:
                date_promoted = "NA"

            #   Eval score should be stored in 1-5
            print("Evaluation score (1-5). Default is 4: ")
            while answered_proper_rank == False:
                eval_score = input().strip()
                eval_score = int(eval_score)
                if eval_score <= 0 or eval_score >= 6:
                    print("Please enter proper eval score (1-5): ")
                else:
                    answered_proper_rank = True

            #   Can employee be added to the schedule or should they be excluded
            print("Can schedule the employee (True or False)")
            while True:
                can_schedule = input().strip().lower()
                if can_schedule == 'true' or can_schedule == 't':
                    can_schedule = 1
                    break
                elif can_schedule == 'false' or can_schedule == 'f':
                    can_schedule = 0
                    break
                else:
                    print("Please enter true or false")

            ans = add_lifeguard_to_db(first_name, last_name, rank, date_promoted, eval_score, can_schedule)
            clear_screen.clear_screen()
            if ans == -1:
                print(f"New employee {first_name} {last_name} {rank} {date_promoted} {eval_score} {can_schedule} has been added!")
            elif ans == 0: 
                print("Employee failed to add. Please try again.")
            else:
                stripped_ans = ans[0] # Just cleaning up the number. Use to look like (1, ) do to fetching employee id num
                print(f"{first_name} {last_name} {rank} Has already been added\nEmployee id is {stripped_ans}")
            
            menu_options()
        
        elif ans.lower() == "back" or ans == "2":
            running = False
            main_menu.main_menu()

        else:
            print("Please pick a different option")
    