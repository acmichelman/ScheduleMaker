import clear_screen
import main_menu
import re
import sqlite3
import logging

DB_PATH = "DatabaseFold/TOHLifeguardDB"

logging.basicConfig(
    filename='logging_info.log', 
    level = logging.DEBUG,
    format='%(asctime)s:%(levelname)s:%(filename)s:%(funcName)s:%(message)s')

# SQL Connect
def add_lifeguard_to_db(first_name: str, last_name: str, rank: str) -> bool:

    #Returns True if a new row was inserted, False if the name already existed.
    
    with sqlite3.connect(DB_PATH) as con:
        cur = con.cursor()
        # This will try to insert. If the unique constraint is, it does nothing.
        cur.execute("""INSERT INTO Employees 
                    (FirstName, LastName, EmployeeRank)
                    VALUES (?, ?, ?)
                    ON CONFLICT(FirstName, LastName) DO NOTHING;
                    """, (first_name, last_name, rank))
        con.commit()
        if cur.rowcount == 1:
            return -1 # SQLite Autoincrement will assign a # between 1 - 9223372036854775807. So -1 will be our indication that its a new value cause 0 is if its false.
            #return cur.rowcount # 1 meaning true dumb ass
        #elif cur.rowcount == 0: #!!! It will return 0 if it doesnt add employee or find a match. !!!
        #    return 0

        # Checks if employee has already been added
        else:
            first = first_name
            last = last_name
            cur.execute("""SELECT EmployeeID FROM Employees
                        WHERE FirstName = ? AND LastName = ?
                        LIMIT 1;
                        """, (first_name, last_name))
            row = cur.fetchone()
            return row
        #return cur.rowcount == 1 # If its True[1] then return its inserted. If False[0] if its skipped
    
def menu_options():
    print("\nMenu Options")
    print("Add[1] \nBack[2]")

def add_lifeguard():
    #Add a lifeguard to the system.
    clear_screen.clear_screen()
    print("Welcome to Add Lifeguard page")
    menu_options()

    running = True
    while running:
        ans = input("> ").strip()

        if ans.lower() == "add" or ans == "1":
            print("Please enter employee 'First Name', 'Last Name', 'Rank'")

            print("First Name: ")
            first_name = input().strip()

            print("Last Name: ")
            last_name = input().strip()

            print("Rank: ")
            rank = input().strip()

            ans = add_lifeguard_to_db(first_name, last_name, rank)
            clear_screen.clear_screen()
            if ans == -1:
                print(f"New employee{first_name} {last_name} {rank} has been added!")
            elif ans == 0: # TODO Currently not working as intended. Need edge case for when not new employee and not existing employee.
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
    