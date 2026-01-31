import clear_screen
import main_menu
import sqlite3
from datetime import datetime

DB_PATH = "DatabaseFold/TOHLifeguardDB"

def edit_beach_push_to_db(beach_name:str, beach_size: str, beach_activity: int, beach_open: str, beach_id: int):
    with sqlite3.connect(DB_PATH) as con:
        cur = con.cursor()
        cur.execute("""UPDATE Beaches
                        SET BeachName = ?,
                        BeachSize = ?,
                        BeachActivity = ?,
                        BeachOpen = ?
                        WHERE BeachID = ?
                        """,(beach_name, beach_size, beach_activity, beach_open, beach_id))
        con.commit()
        print("Update sucessful!")
        return cur.rowcount == 1

def pick_beach_by_name(beach_name: str):
    with sqlite3.connect(DB_PATH) as con:
        cur = con.cursor()
        # Search by beach name. We use this for user to validate correct beach
        cur.execute("""SELECT * FROM Beaches 
                    WHERE BeachName = ? ;
                    """, (beach_name,))
    row = cur.fetchall()
    if not row:
        #print("No employee by that name")
        return -1
    else:
        return(row)
    
def edit_beach_info(row):
    did_anything_change = False
    if row == -1:
        print("No employee with this infromation")
    else:
        beach_id_db, beach_name_db, beach_size_db, beach_activity_db, beach_open_db = row[0]
        print(f"Beach {beach_name_db} found. Please enter new infromation when prompted.\n If you dont wish to change something please leave it blank and press ENTER.")

        #   Beach Name
        print("Beach name: ", beach_name_db)
        beach_name_db_temp = input().strip()
        if beach_name_db_temp == "":
            beach_name_db_temp = beach_name_db
        else:
            did_anything_change = True

        #   Beach Size
        print("Beach size. Enter 'small', 'medium', or 'large': ", beach_size_db)
        while True:
            beach_size_db_temp = input().strip().lower()
            if beach_size_db_temp == "":
                beach_size_db_temp = beach_size_db
                break
            else:
                did_anything_change = True
            if beach_size_db_temp == "s" or beach_size_db_temp == "m" or beach_size_db_temp == "l":
                if beach_size_db_temp == "s":
                    beach_size_db_temp = "small"
                elif beach_size_db_temp == "m":
                    beach_size_db_temp = "medium"
                elif beach_size_db_temp == "l":
                    beach_size_db_temp = "large"
                break
            elif beach_size_db_temp == "small" or beach_size_db_temp == "medium" or beach_size_db_temp == "large":
                break
            else:
                print("Invalid size. Please pick 'Small' or 's', 'Medium' or 'm', 'Large' or 'l': ")

        #   Beach activity
        print("Beach activity. Please enter a number 1-5 with 1 being the least active and 5 being most: ", beach_activity_db)
        while True:
            beach_activity_db_temp = input().strip()
            if beach_activity_db_temp == "":
                beach_activity_db_temp = beach_activity_db
                break
            else:
                did_anything_change = True
            beach_activity_db_temp = int(beach_activity_db_temp)
            if beach_activity_db_temp <= 0 or beach_activity_db_temp >= 6:
                print("Invalid activity score. Please enter a score 1-5: ")
            else:
                break

        #   Beach Open
        print("Beach open. Please enter 'true'/'t' or 'false'/'f': ", beach_open_db)
        while True:
            beach_open_db_temp = input().strip().lower()
            if beach_open_db_temp == "":
                beach_open_db_temp = beach_open_db
                break
            else:
                did_anything_change = True
            if beach_open_db_temp == 't' or beach_open_db_temp == 'f':
                if beach_open_db_temp == "t":
                    beach_open_db_temp = "true"
                elif beach_open_db_temp == 'f':
                    beach_open_db_temp = "false"
                break
            elif beach_open_db_temp == "true" or beach_open_db_temp == "false":
                break
            else:
                print("Please enter 'true' or 'false': ")

        if did_anything_change == True:
            #   Push the info here
            print(f"Beach name: {beach_name_db_temp}\nBeach size: {beach_size_db_temp}\nBeach activity: {beach_activity_db_temp}\nBeach open: {beach_open_db_temp}\n\nIs this infromation correct (Y/N)")
            while True:
                ans_correct_info = input().strip().lower()
                if ans_correct_info == "yes" or ans_correct_info == "y":
                    edit_beach_push_to_db(beach_name_db_temp, beach_size_db_temp, beach_activity_db_temp, beach_open_db_temp, beach_id_db)
                    break
                elif ans_correct_info == "no" or ans_correct_info == "n":
                    break
                else:
                    print("Please enter Yes or No (Y/N)")
        else:
            print("No infromation changed")


def menu_options():
    print("\nMenu Options")
    print("Edit[1] \nBack[2]")

def edit_beach():
    #   Add a lifeguard to the system.
    clear_screen.clear_screen()
    print("Welcome to Edit Beach page")
    menu_options()

    running = True
    
    while running:
        ans = input("> ").strip()

        if ans.lower() == "edit" or ans == "1":
            print("Please enter beach name: ")
            beach_name = input().strip()
            if beach_name != "":
                row = pick_beach_by_name(beach_name)
                edit_beach_info(row)
            
            menu_options()
        
        elif ans.lower() == "back" or ans == "2":
            running = False
            main_menu.main_menu()

        else:
            print("Please pick a different option")
    