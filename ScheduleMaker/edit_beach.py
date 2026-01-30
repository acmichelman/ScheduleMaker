import clear_screen
import main_menu
import sqlite3
from datetime import datetime

DB_PATH = "DatabaseFold/TOHLifeguardDB"

def menu_options():
    print("\nMenu Options")
    print("Remove[1] \nBack[2]")

def edit_beach():
    #   Add a lifeguard to the system.
    clear_screen.clear_screen()
    print("Welcome to Edit Beach page")
    menu_options()

    running = True
    
    while running:
        ans = input("> ").strip()

        if ans.lower() == "edit" or ans == "1":
            print("TODO add EDIT functionallity")
            
            menu_options()
        
        elif ans.lower() == "back" or ans == "2":
            running = False
            main_menu.main_menu()

        else:
            print("Please pick a different option")
    