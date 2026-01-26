import clear_screen
import main_menu
import sqlite3
import lifeguard_list
import edit_employees

DB_PATH = "DatabaseFold/TOHLifeguardDB"

def remove_lifeguard_from_db(first_name: str, last_name: str, emp_id: int) -> bool:
    
    with sqlite3.connect(DB_PATH) as con:
        cur = con.cursor()
        cur.execute("""DELETE FROM Employees
                    WHERE FirstName = ? AND LastName = ? AND EmployeeID = ?
                    """, (first_name, last_name, emp_id))
        con.commit()

        removed = cur.rowcount # To check how many removed  
        return removed
    
    #For clarification we want this to return either first/last name (type str) or employee ID(type int) to be passed into remove func above
def validate_info(row, we_getting_a_id):
    employee_id_db, first_name_db, last_name_db, rank_db, time_added_db, date_promoted_db, eval_score_db = row[0]
    print("First name: ",first_name_db)
    print("Last name: ",last_name_db)
    print("Employee ID: ",employee_id_db)
    print("Employee rank:",rank_db)
    print("Time added to dayabase: ",time_added_db)
    print("Date employee was promoted: : ",date_promoted_db)
    print("Employee evaluation score (1-5): ", eval_score_db)

    if we_getting_a_id == 1:
        #   If True we have the first and last name. 
        return (employee_id_db, None)
    elif we_getting_a_id == 0:
        #   If False we have employee_id
        return(first_name_db, last_name_db)
    elif we_getting_a_id == 2:
        return 

def menu_options():
    print("\nMenu Options")
    print("Remove[1]\nView Employees[2]\nBack[3]")

def removing_functionallity():
    print("Please enter employee's first name you wish to remove: ")
    first_name_ans = input().strip()
    print("Please enter employee's last name you wish to remove: ")
    last_name_ans = input().strip()
    #This checks if just first/ last name has been entered
    print("Please enter employee's ID in known: ")
    emp_id_ans = input().strip()
    if emp_id_ans == "":
        row = edit_employees.pick_employee_by_name(first_name_ans, last_name_ans)
        #   When we search by credentials and cant find someone
        if row == -1:
            print("No employee with that infromation")
            return 
            
        #   This is a check to either get missing first/last name or ID
        missing_first_name_or_int, missing_last_name_or_extra = validate_info(row, we_getting_a_id=1)
        #   if missing_last_name_or_extra is None then we know we only got back employee_id so we can add first_name and last_nameto remove_lifeguard_from_db
        if missing_last_name_or_extra is None:
            emp_id_ans = missing_first_name_or_int
        print ("\nIs this the employee you wish to remove? (Y/N) ")
        #   Will prompt the user if they are removing the correct employee
        while True:
            ans_correct_info = input().strip().lower()
            if ans_correct_info == "yes" or ans_correct_info == "y":
                ans = remove_lifeguard_from_db(first_name_ans, last_name_ans, emp_id_ans)
                break
            elif ans_correct_info == "no" or ans_correct_info == "n":
                break
            else:
                print("Please enter Yes or No (Y/N)")

    #   This checks if the user has just entered ID
    elif first_name_ans == "" and last_name_ans == "":
        row = edit_employees.pick_employee_by_id(emp_id_ans)
        #   This is a check to either get missing first/last name or ID
        if row == -1:
            print("No employee with that infromation")
            return (-1)
        missing_first_name_or_int, missing_last_name_or_extra = validate_info(row, we_getting_a_id=0)
        if missing_last_name_or_extra is not None:
            first_name_ans = missing_first_name_or_int
            last_name_ans = missing_last_name_or_extra
        print ("\nIs this the employee you wish to remove? (Y/N) ")
        #   Will prompt the user if they are removing the correct employee
        while True:
            ans_correct_info = input().strip().lower()
            if ans_correct_info == "yes" or ans_correct_info == "y":
                ans = remove_lifeguard_from_db(first_name_ans, last_name_ans, emp_id_ans)
                break
            elif ans_correct_info == "no" or ans_correct_info == "n":
                break
            else:
                print("Please enter Yes or No (Y/N)")

    #   If user entered all first name, last name, and id. Good user. sstay on the rails.
    elif first_name_ans != "" and last_name_ans != "" and emp_id_ans != "":
        row = edit_employees.pick_employee_by_both(first_name_ans, last_name_ans, emp_id_ans)
        if row == -1:
            print("No employee with that infromation")
            return (-1)
        while True:
            validate_info(row, we_getting_a_id=2)
            print ("\nIs this the employee you wish to remove? (Y/N) ")
            ans_correct_info = input().strip().lower()
            if ans_correct_info == "yes" or ans_correct_info == "y":
                ans = remove_lifeguard_from_db(first_name_ans, last_name_ans, emp_id_ans)
                break
            elif ans_correct_info == "no" or ans_correct_info == "n":
                break
            else:
                print("Please enter Yes or No (Y/N)")

    #   Edge cast time
    elif first_name_ans == "" and last_name_ans != "" and emp_id_ans != "":
        print("Please either enter employee 'First Name' and 'Last Name' or 'Employee ID'")
    elif first_name_ans != "" and last_name_ans == "" and emp_id_ans != "":
        print("Please either enter employee 'First Name' and 'Last Name' or 'Employee ID'")
    else:
        print("Please either enter employee 'First Name' and 'Last Name' or 'Employee ID'")
    if ans == 1:
        print(f"Removed {ans} employee named {first_name_ans} {last_name_ans} {emp_id_ans}.")
    else:
        print(f"No employee found named {first_name_ans} {last_name_ans} {emp_id_ans}.")

def remove_lifeguard():
    """Remove a lifeguard from the system."""
    clear_screen.clear_screen()
    print("Welcome to Remove Lifeguard page")
    menu_options()

    running = True
    while running:
        ans = input("> ").strip()

        if ans.lower() == "remove" or ans.lower() == "1":
            removing_functionallity()
            menu_options()
        elif ans.lower() == "view" or ans.lower() == "2":
            print("view")
            lifeguard_list.viewEmployeeList()
            menu_options()
        elif ans.lower() == "back" or ans.lower() == "3":
            running = False
            main_menu.main_menu()
        else:
            print("Please pick a different option")