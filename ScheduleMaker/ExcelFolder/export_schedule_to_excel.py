import sqlite3
import logging
from pathlib import Path
from datetime import datetime
from openpyxl import load_workbook

from .. import clear_screen, main_menu

def menu_options():
    print("\nMenu Options")
    print("Export Employees (Export)[1] \nBack[2]")

def import_emp_from_excel_menu():

    clear_screen.clear_screen()
    print("Welcome to the export employee page\n.")
    menu_options()

    running = True
    
    while running:
        ans = input("> ").strip()

        if ans.lower() == "Export" or ans == "1":
            print("Export Excel")

        elif ans.lower() == "back" or ans == "2":
            running = False
            main_menu.main_menu()

        else:
            print("Please pick a different option")
        menu_options()