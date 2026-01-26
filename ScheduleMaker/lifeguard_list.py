import clear_screen
import main_menu
import sqlite3
import logging

DB_PATH = "DatabaseFold/TOHLifeguardDB"

# SQL Connect
def viewEmployeeList():
    with sqlite3.connect(DB_PATH) as con:
        cur = con.cursor()
        # TODO: Should have different functions on differing ways to sort
        cur.execute("""SELECT EmployeeID, FirstName, LastName, EmployeeRank, DatePromoted, EvaluationScore
                    FROM Employees
                    ORDER BY LastName, FirstName
                    """)
        rows = cur.fetchall()

        if not rows: # TODO: Edge case. Should present option to add employee or something
            print("No employees added to database")
        else:
            print("EmployeeID | First Name    Last Name| Rank    | Date Promoted | Eval Score")
            print("-------------------------------------------")
            for emp_id, first, last, rank, promo_date, eval_date in rows:
                name = f"{first}, {last}"
                print(f"{emp_id:<10} | {name:<18} | {rank} | {promo_date} | {eval_date}")

        #con.close()

def menu_options():
    print("\nMenu Options")
    print("View[1] \nBack[2]")

def lifeguard_list():
    """Display the Lifeguard List menu."""
    clear_screen.clear_screen()
    print("Welcome to Lifeguard List page")
    menu_options()

    running = True
    while running:
        ans = input("> ").strip()
        if ans.lower() == "view" or ans == "1":
            clear_screen.clear_screen()
            viewEmployeeList()
            menu_options()
        elif ans.lower() == "back" or ans == "2":
            running == False
            main_menu.main_menu()
        else:
            print("Please pick a different option")
    # TODO: Load and display lifeguard list from file or database 