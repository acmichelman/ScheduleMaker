from pathlib import Path
import sqlite3
from datetime import datetime

from .. import clear_screen, main_menu

from ..db import DB_PATH, ensure_db_dir

def edit_employee_push_to_db(first_name: str, last_name: str, employee_rank: str, date_promoted: str, evaluation_score: int, employee_id: int, can_schedule: int):
    with sqlite3.connect(DB_PATH) as con:
        cur = con.cursor()
        cur.execute("""UPDATE Employees
                        SET FirstName = ?,
                        LastName = ?,
                        EmployeeRank = ?,
                        DatePromoted = ?,
                        EvaluationScore = ?
                        CanSchedule = ?
                        WHERE EmployeeID = ?
                        """,(first_name, last_name, employee_rank, date_promoted, evaluation_score, can_schedule, employee_id))
        con.commit()
        print("Update sucessful!")
        return cur.rowcount == 1

#   Func that searches by NAME
def pick_employee_by_name(first_name: str, last_name: str):
    with sqlite3.connect(DB_PATH) as con:
        cur = con.cursor()
        # Search by first and last name
        cur.execute("""SELECT * FROM Employees 
                    WHERE FirstName = ? AND LastName = ?;
                    """, (first_name, last_name))
    row = cur.fetchall()

    return -1 if not row else row

#   Func that searches by ID
def pick_employee_by_id(id_num: int):
    with sqlite3.connect(DB_PATH) as con:
        cur = con.cursor()
        # Search by id
        cur.execute("""SELECT * FROM Employees 
                    WHERE EmployeeID = ?;
                    """, (id_num))
    row = cur.fetchall()

    if not row:
        #print("No employee by that ID")
        return -1
    else:
        return(row)
    
    #   To be used elsewhere
def pick_employee_by_both(first_name: str, last_name: str, id_num: int):
    with sqlite3.connect(DB_PATH) as con:
        cur = con.cursor()
        # Search by id
        cur.execute("""SELECT * FROM Employees 
                    WHERE FirstName = ? AND LastName = ? AND EmployeeID = ?;
                    """, (first_name, last_name, id_num))
    row = cur.fetchall()

    if not row:
        #print("No employee with that name and ID")
        return -1
    else:
        return(row)
    
#   EDIT func (This is our main piece of edit employee code you can stop looking now)
def edit_employee_info(row):
    did_anything_change = False
    if row == -1:
        print("No employee with this infromation")
    else:
        employee_id_db, first_name_db, last_name_db, rank_db, time_added_db, date_promoted_db, eval_score_db, can_schedule = row[0]
        print (f"Employee {first_name_db} {last_name_db} found. Please enter new infromation when prompted.\n If you dont wish to change something please leave it blank and press ENTER.")

        #   First name
        print("First name: ",first_name_db)
        first_name_db_temp = input().strip()
        if first_name_db_temp == "":
            first_name_db_temp = first_name_db
        else:
            did_anything_change = True

        #   Last name
        print("Last name: ",last_name_db)
        last_name_db_temp = input().strip()
        if last_name_db_temp == "":
            last_name_db_temp = last_name_db
        else:
            did_anything_change = True

        #   Employee rank
        print("Employee rank:",rank_db)
        while True:
            rank_db_temp = input().strip()
            if rank_db_temp == "":
                rank_db_temp = rank_db
                break
            else:
                did_anything_change = True
            if rank_db_temp == "lg" or rank_db_temp == "sg" or rank_db_temp == "lt" or rank_db_temp == "sl":
                if rank_db_temp == "lg":
                    rank_db_temp = "lifeguard"
                elif rank_db_temp == "sg":
                    rank_db_temp = "senior guard"
                elif rank_db_temp == "lt":
                    rank_db_temp = "lieutenant"
                elif rank_db_temp == "sl":
                    rank_db_temp == "senior lieutenant"
                break
            elif rank_db_temp == "lifeguard" or rank_db_temp == "senior guard" or rank_db_temp == "lieutenant" or rank_db_temp == "senior lieutenant":
                break
            else:
                print("LG for unranked lifeguard, SG for senior guard, LT for lieutenant, SL for senior lieutenant \nPlease enter a valid rank.: ")


        #   Date promoted if has rank other then Lifeguard
        if rank_db_temp != "lifeguard":
            print("Date employee was promoted (MM/DD/YYYY): ",date_promoted_db)
            answered_promotion_date = False
            while answered_promotion_date == False:
                answered_promotion_date = True
                date_promoted_db_temp = input().strip()
                if date_promoted_db_temp == "":
                    date_promoted_db_temp = date_promoted_db
                    break
                else:
                    did_anything_change = True
                try:
                    datetime.strptime(date_promoted_db_temp, "%m/%d/%Y")
                except ValueError:
                    print("Invalid date. Please use MM/DD/YYYY: ")
                    answered_promotion_date = False
        else:
            date_promoted_db_temp = "NA"

        #   Eval score 1-5
        print("Employee evaluation score (1-5): ", eval_score_db)
        while True:
            eval_score_db_temp = input().strip()
            if eval_score_db_temp == "":
                eval_score_db_temp = eval_score_db
                break
            else:
                did_anything_change = True
            eval_score_db_temp = int(eval_score_db_temp)
            if eval_score_db_temp <= 0 or eval_score_db_temp >= 6:
                print("Please enter proper eval score (1-5): ")
            else:
                break

            #   Can Schedule 1 = true/ 0 = false
            print("Can schedule employee (True/False)", can_schedule)
            while True:
                can_schedule = input().strip().lower()
                if can_schedule == 'true' or can_schedule == 't':
                    can_schedule = 1
                    did_anything_change == True
                    break
                elif can_schedule == 'false' or can_schedule == 'f':
                    can_schedule = 0
                    did_anything_change == True
                    break
                elif can_schedule == "":
                    break
                else:
                    print("Please enter true or false")
        
        if did_anything_change == True:
            #   Push the info here
            print(f"First name: {first_name_db_temp}\nLast name: {last_name_db_temp}\nEmployee rank: {rank_db_temp}\nDate employee was promoted: {date_promoted_db_temp}\nEmployee evaluation score: {eval_score_db_temp}\nCan schedule employee: {can_schedule}\n\nIs this infromation correct (Y/N)")
            while True:
                ans_correct_info = input().strip().lower()
                if ans_correct_info == "yes" or ans_correct_info == "y":
                    edit_employee_push_to_db(first_name_db_temp, last_name_db_temp, rank_db_temp, date_promoted_db_temp, eval_score_db_temp,can_schedule, employee_id_db)
                    break
                elif ans_correct_info == "no" or ans_correct_info == "n":
                    break
                else:
                    print("Please enter Yes or No (Y/N)")
        else:
            print("No infromation changed")
        

def menu_options():
    print("\nMenu Options")
    print("Search by First and Last (name)[1] \nSearch by (Id)[2] \nBack[3]")

def edit_employee():
    #   Edit a lifeguard to the system.
    clear_screen.clear_screen()
    print("Welcome to Edit Lifeguard page")
    menu_options()

    running = True
    while running:
        ans = input("> ").strip()

        if ans.lower() == "name" or ans == "1":
            print("Please enter employee FIRST name: ")
            first_name = input().strip()

            print("Please enter employee LAST name: ")
            last_name = input().strip()

            if first_name != "" or last_name != "":

                row = pick_employee_by_name(first_name, last_name)
                edit_employee_info(row)

            menu_options()

        elif ans.lower() == "id" or ans == "2":
            print("id called")

            print("Please enter employee ID number: ")
            employee_id = input().strip()

            row = pick_employee_by_id(employee_id)
            edit_employee_info(row)

            menu_options()


        elif ans.lower() == "back" or ans == "3":
            running = False
            main_menu.main_menu()
        else:
            print("Please pick a different option")

    menu_options()