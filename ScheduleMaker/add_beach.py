import clear_screen
import main_menu
import sqlite3
import logging

DB_PATH = "DatabaseFold/TOHLifeguardDB"

logging.basicConfig(
    filename='logging_info.log', 
    level = logging.DEBUG,
    format='%(asctime)s:%(levelname)s:%(filename)s:%(funcName)s:%(message)s')

# SQL Connect
def add_beach_to_db(beach_name: str, beach_size: str, beach_activity: int, beach_open: str) -> bool:

    #Returns True if a new row was inserted, False if the name already existed.
    
    with sqlite3.connect(DB_PATH) as con:
        cur = con.cursor()
        # This will try to insert. If the unique constraint is, it does nothing.
        cur.execute("""INSERT INTO Beaches
                    (BeachName, BeachSize, BeachActivity, BeachOpen)
                    VALUES (?, ?, ?, ?)
                    ON CONFLICT(BeachName) DO NOTHING;
                    """, (beach_name, beach_size, beach_activity, beach_open))
        con.commit()
        if cur.rowcount == 1:
            return -1 

        # Checks if employee has already been added
        else: 
            cur.execute("""SELECT BeachID FROM Beaches
                        WHERE BeachName = ?
                        LIMIT 1;
                        """, (beach_name,))
            row = cur.fetchone()
            return row
        #   return cur.rowcount == 1 # If its True[1] then return its inserted. If False[0] if its skipped
    
def menu_options():
    print("\nMenu Options")
    print("Add[1] \nBack[2]")

def add_beach():
    #   Add a Beach to the system.
    clear_screen.clear_screen()
    print("Welcome to Add Beach page")
    menu_options()

    running = True
    
    while running:

        ans = input("> ").strip()

        if ans.lower() == "add" or ans == "1":
            print("Please enter 'Beach Name', 'Beach Size' (small, medium, large), 'Beach Activity' (1-5), Beach Open (true or false)")
            
            #   Beach Name 
            print("Beach Name: ")
            beach_name = input().strip()

            #   Beach Size (small, medium, large)
            print("Beach Size: ")
            while True:
                beach_size = input().strip().lower()
                if beach_size == "s" or beach_size == "m" or beach_size == "l":
                    if beach_size == "s":
                        beach_size = "small"
                    elif beach_size == "m":
                        beach_size = "medium"
                    elif beach_size == "l":
                        beach_size = "large"
                    break
                elif beach_size == "small" or beach_size == "medium" or beach_size == "large":
                    break
                else:
                    print("Invalid size. Please pick 'Small' or 's', 'Medium' or 'm', 'Large' or 'l': ")

            #   Beach Activity (1-5)
            print("Beach Activity: ")
            while True:
                beach_activity = input().strip()
                beach_activity = int(beach_activity)
                if beach_activity <= 0 or beach_activity >= 6:
                    print("Invalid activity score. Please enter a score 1-5: ")
                else:
                    break
            
            #   Beach Open (true, false)
            print("Beach Open: ")
            while True:
                beach_open = input().strip().lower()
                if beach_open == "t" or beach_open == "f":
                    if beach_open == "t":
                        beach_open = "true"
                    elif beach_open == "f":
                        beach_open = "false"
                    break
                elif beach_open == "true" or beach_open == "false":
                    break
                else:
                    print("Invalid choice. Please enter 'True' or 't', 'False' or 'f': ")
            
            ans = add_beach_to_db(beach_name, beach_size, beach_activity, beach_open)
            clear_screen.clear_screen

            if ans == -1:
                print(f"New Beach {beach_name} has been opened. Beach size: {beach_size}, Beach activity: {beach_activity}, Beach open: {beach_open}!")
            elif ans == 0:
                print("Beach failed to add. Please try again.")
            else:
                stripped_ans = ans[0]
                print(f"{beach_name} has already been added. Beach Id is {stripped_ans}")
            menu_options()
        
        elif ans.lower() == "back" or ans == "2":
            running = False
            main_menu.main_menu()

        else:
            print("Please pick a different option")
    