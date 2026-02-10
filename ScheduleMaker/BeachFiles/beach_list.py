from pathlib import Path
import sqlite3

from .. import clear_screen, main_menu

DB_PATH = Path(__file__).resolve().parents[1] / "DatabaseFold" / "TOHLifeguardDB"

def viewBeachList():
    with sqlite3.connect(DB_PATH) as con:
        cur = con.cursor()
        # TODO: Should have different functions on differing ways to sort
        cur.execute("""SELECT BeachID, BeachName, BeachSize, BeachActivity, BeachOpen
                    FROM Beaches
                    ORDER BY BeachID
                    """)
        rows = cur.fetchall()

        if not rows: # TODO: Edge case. Should present option to add employee or something
            print("No beaches added to database")
        else:
            print("Beach ID | Beach Name    |Size    |Activity| Opened ")
            print("----------------------------------------------------------")
            for b_id, b_name, b_size, b_activity, b_open in rows:
                if b_open == 1:
                    b_open = 'True'
                elif b_open == 0:
                    b_open = 'False'
                name = f"{b_name}"
                print(f"{b_id:<8} | {name:<13} | {b_size:<6} | {b_activity:<6} | {b_open:<5}")

        #con.close()

def menu_options():
    print("\nMenu Options")
    print("View[1] \nBack[2]")

def beach_list():
    """Display the Beach List menu."""
    clear_screen.clear_screen()
    print("Welcome to Beach List page")
    menu_options()

    running = True
    while running:
        ans = input("> ").strip()
        if ans.lower() == "view" or ans == "1":
            clear_screen.clear_screen()
            viewBeachList()
            menu_options()
        elif ans.lower() == "back" or ans == "2":
            running = False
            main_menu.main_menu()
        else:
            print("Please pick a different option")
   