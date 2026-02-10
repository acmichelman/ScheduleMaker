from pathlib import Path
import sqlite3

from .. import clear_screen, main_menu

DB_PATH = Path(__file__).resolve().parents[1] / "DatabaseFold" / "TOHLifeguardDB"

# SQL Connect
def viewEmployeeList():
    with sqlite3.connect(DB_PATH) as con:
        cur = con.cursor()
        # TODO: Should have different functions on differing ways to sort
        cur.execute("""SELECT EmployeeID, FirstName, LastName, EmployeeRank, DatePromoted, EvaluationScore, CanSchedule
                    FROM Employees
                    ORDER BY LastName, FirstName
                    """)
        rows = cur.fetchall()

        if not rows: # TODO: Edge case. Should present option to add employee or something
            print("No employees added to database")
        else:
            print("EmployeeID | First Name    Last Name| Rank            | Date Promoted | Eval Score | Can Schedule")
            print("-------------------------------------------")
            for emp_id, first, last, rank, promo_date, eval_score, can_schedule in rows:
                if can_schedule == 1:
                    can_schedule = 'True'
                elif can_schedule == 0:
                    can_schedule = 'False'
                name = f"{first}, {last}"
                print(f"{emp_id:<10} | {name:<22} | {rank:<15} | {promo_date:<13} | {eval_score:<10} | {can_schedule:<5}")

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
            running = False
            main_menu.main_menu()
        else:
            print("Please pick a different option")
    # TODO: Load and display lifeguard list from file or database 