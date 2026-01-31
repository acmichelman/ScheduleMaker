import sys

from . import clear_screen
from .EmployeesFiles import lifeguard_list, add_lifeguard, remove_lifeguard, edit_employees
from .BeachFiles import beach_list, add_beach, remove_beach, edit_beach

def main_menu():
    """Main menu loop."""
    clear_screen.clear_screen()
    print("Welcome to the Lifeguard Schedule Maker.\n")
    print("Please type which menu to navigate to:\n")
    print("Lifeguard List[1]\nAdd Lifeguard[2]\nRemove Lifeguard[3]\nEdit Lifeguard[4]\nBeach List[5]\nAdd Beach[6]\nRemove Beach[7]\nEdit Beach[8]\nQuit[0]\n")

    running = True
    while running:
        ans = input("> ").strip()

        if ans.lower() == "lifeguard list" or ans == "1":
            lifeguard_list.lifeguard_list()
        elif ans.lower() == "add lifeguard" or ans == "2":
            add_lifeguard.add_lifeguard()
        elif ans.lower() == "remove lifeguard" or ans == "3":
            remove_lifeguard.remove_lifeguard()
        elif ans.lower() == "edit lifeguard" or ans == "4":
            edit_employees.edit_employee()
        elif ans.lower() == "beach list" or ans == "5":
            beach_list.beach_list()
        elif ans.lower() == "add beach" or ans == "6":
            add_beach.add_beach()
        elif ans.lower() == "remove beach" or ans == "7":
            remove_beach.remove_beach()
        elif ans.lower() == "edit beach" or ans == "8":
            edit_beach.edit_beach()
        elif ans.lower() == "quit" or ans == "0": 
            clear_screen.clear_screen()
            print("Thank you for scheduling with us!")
            running = False
            sys.exit(0)
        else:
            clear_screen.clear_screen()
            print("Please enter a valid option.\n")
    print("Lifeguard List[1]\nAdd Lifeguard[2]\nRemove Lifeguard[3]\nEdit Lifeguard[4]\nBeach List[5]\nAdd Beach[6]\nRemove Beach[7]\nEdit Beach[8]\nQuit[0]\n")

