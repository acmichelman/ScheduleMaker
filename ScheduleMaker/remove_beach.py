import clear_screen
import main_menu
import sqlite3
import edit_beach
from datetime import datetime

DB_PATH = "DatabaseFold/TOHLifeguardDB"

def remove_beach_from_db(beach_name:str) -> bool:
    with sqlite3.connect(DB_PATH) as con:
        cur = con.cursor()
        cur.execute("""DELETE FROM Beaches
                    WHERE BeachName = ?
                    """, (beach_name,))
        con.commit()
        removed = cur.rowcount # To check how many removed  
        return removed

def validate_info(row):
    beach_id_db, beach_name_db, beach_size_db, beach_activity_db, beach_open_db = row[0]
    print("Beach Name: ", beach_name_db)
    print("Beach Id: ", beach_id_db)
    print("Beach size: ", beach_size_db)
    print("Beach activity: ",beach_activity_db)
    print("Beach open: ",beach_open_db)


def menu_options():
    print("\nMenu Options")
    print("Remove[1] \nBack[2]")

def removing_functionallity():
    print("Please enter beach name you wish to remove: ")
    beach_name_ans = input().strip()

    row = edit_beach.pick_beach_by_name(beach_name_ans)

    validate_info(row)
    print ("\nIs this the beach you wish to remove? (Y/N) ")
    while True:
        ans_correct_info = input().strip().lower()
        if ans_correct_info == "yes" or ans_correct_info == "y":
            ans = remove_beach_from_db(beach_name_ans)
            break
        elif ans_correct_info == "no" or ans_correct_info == "n":
            ans = 0
            break
        else:
            print("Please enter Yes or No (Y/N)")

    if ans == 1:
        print(f"Removed {ans} beach named '{beach_name_ans}'.")
    else:
        print(f"No beach found named '{beach_name_ans}'.")


def remove_beach():
    #   Remove beach from DB
    clear_screen.clear_screen()
    print("Welcome to Remove Beach page")
    menu_options()

    running = True
    
    while running:
        ans = input("> ").strip()

        if ans.lower() == "remove" or ans == "1":
            removing_functionallity()
            
            menu_options()
        
        elif ans.lower() == "back" or ans == "2":
            running = False
            main_menu.main_menu()

        else:
            print("Please pick a different option")
    