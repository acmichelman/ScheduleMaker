import sqlite3
from datetime import datetime
import clear_screen, main_menu

def menu_options():
    print("\nMenu Options")
    print("Make Schedule[1] \nBack[2]")

def make_schedule():
    #   Finally we reach our make schedule page. Haza
    clear_screen.clear_screen()
    print("Welcome to the schedule making page")
    menu_options()

    running = True
    
    while running:
        print("Make Schdeule called")
        ans = input("> ").strip()

        if ans.lower() == "Make Schdeule" or ans == "1":
            print("Make Schdeule called")
        menu_options()