import clear_screen
import main_menu
import sqlite3
import lifeguard_list

DB_PATH = "DatabaseFold/TOHLifeguardDB"

def remove_lifeguard_from_db(first_name: str, last_name: str, id: int) -> bool:
    

    with sqlite3.connect(DB_PATH) as con:
        cur = con.cursor()
        cur.execute(
            "DELETE FROM Employees WHERE FirstName = ? AND LastName = ? AND EmployeeID = ?",
            (first_name, last_name, id)
        )
        con.commit()

        removed = cur.rowcount # To check how many removed  
        return removed
        #if removed > 0:
        #    print(f"Removed {removed} employee(s) named {first_name} {last_name} {id}.")
        #else:
        #    print(f"No employee found named {first_name} {last_name} {id}.")

def menu_options():
    print("\nMenu Options")
    print("Remove[1]\nView Employees[2]\nBack[3]")

def remove_lifeguard():
    """Remove a lifeguard from the system."""
    clear_screen.clear_screen()
    print("Welcome to Remove Lifeguard page")
    menu_options()

    running = True
    while running:
        ans = input("> ").strip()

        if ans.lower() == "remove" or ans.lower() == "1":
            print("Please enter employee's first name you wish to remove: ")
            first_name_ans = input().strip()
            print("Please enter employee's last name you wish to remove: ")
            last_name_ans = input().strip()
            print("Please enter employee's ID in known: ")
            emp_id_ans = input().strip()

            ans = remove_lifeguard_from_db(first_name_ans, last_name_ans, emp_id_ans)
            if ans > 0:
                print(f"Removed {ans} employee(s) named {first_name_ans} {last_name_ans} {emp_id_ans}.")
            else:
                print(f"No employee found named {first_name_ans} {last_name_ans} {emp_id_ans}.")

            menu_options()
        elif ans.lower() == "view" or ans.lower() == "2":
            # TODO import the view list logic to be used for now. Need to be used when view menu is made
            print("view")
        elif ans.lower() == "back" or ans.lower() == "3":
            running = False
            main_menu.main_menu()
        else:
            print("Please pick a different option")
    # TODO: Implement logic to remove lifeguard details