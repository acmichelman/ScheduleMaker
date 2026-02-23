import sys

from . import clear_screen, make_schedule
from .EmployeesFiles import lifeguard_list, add_lifeguard, remove_lifeguard, edit_employees
from .BeachFiles import beach_list, add_beach, remove_beach, edit_beach
from .ExcelFolder import import_employees_excel, export_schedule_to_excel

#   Lifeguard navigation page
def lifeguard_page():
    clear_screen.clear_screen()
    print("Please select a option\nView Lifeguards[1]\nAdd Single Lifeguard[2]\nImport Lifeguards With Excel[3]\nRemove Lifeguard[4]\nEdit Lifeguard Infromation[5]\nBack[0]")
    while True:
        ans = input("> ").strip()
        if ans.lower() == "lifeguard list" or ans.lower == "list" or ans == "1":
            lifeguard_list.lifeguard_list()
        elif ans.lower() == "add single lifeguard" or ans.lower() == "add" or ans == "2":
            add_lifeguard.add_lifeguard()
        elif ans.lower() == "import lifeguards with excel" or ans.lower() == "import" or ans == "3":
            import_employees_excel.import_emp_from_excel_menu()
        elif ans.lower() == "remove lifeguard" or ans.lower() == "remove" or ans == "4":
            remove_lifeguard.remove_lifeguard()
        elif ans.lower() == "edit lifeguard infromation" or ans.lower == "edit" or ans == "5":
            edit_employees.edit_employee()
        elif ans.lower() == "back" or ans == "0":
            break
        else:
            clear_screen.clear_screen()
            print("Please enter a valid option.\n")
            print("View Lifeguards[1]\nAdd Single Lifeguard[2]\nImport Lifeguards With Excel[3]\nRemove Lifeguard[4]\nEdit Lifeguard Infromation[5]\nBack[0]")
    main_menu()

#   Beach navigation page
def beach_page():
    clear_screen.clear_screen()
    print("Please select a option\nView Beachs[1]\nAdd Beach[2]\nRemove Beach[3]\nEdit Beach[4]\nBack[0]")
    while True:
        ans = input("> ").strip()
        if ans.lower() == "beach list" or ans.lower == "list" or ans == "1":
            beach_list.beach_list()
        elif ans.lower() == "add beach" or ans.lower() == "add" or ans == "2":
            add_beach.add_beach()
        elif ans.lower() == "remove beach" or ans.lower() == "remove" or ans == "3":
            remove_beach.remove_beach()
        elif ans.lower() == "edit beach" or ans.lower == "edit" or ans == "4":
            edit_beach.edit_beach()
        elif ans.lower() == "back" or ans == "0":
            break
        else:
            clear_screen.clear_screen()
            print("Please enter a valid option.\n")
            print("View Beachs[1]\nAdd Beach[2]\nRemove Beach[3]\nEdit Beach[4]\nBack[0]")
    main_menu()

#   Main menu navigation page
def main_menu():
    """Main menu loop."""
    clear_screen.clear_screen()
    print("Welcome to the Lifeguard Schedule Maker.\n")
    print("Please enter which menu to navigate to:\n")
    print("Lifeguard Page[1]\nBeach Page[2]\nMake Schedule[3]\nExport Schedule[4]\nQuit[0]")
    running = True
    while running:
        ans = input("> ").strip()

        if ans.lower() == "lifeguard page" or ans == "1":
            lifeguard_page()
        elif ans.lower() == "beach page" or ans == "2":
            beach_page()
        elif ans.lower() == "make schedule" or ans == "3":
            make_schedule.make_schedule()
        elif ans.lower() == "export schedule" or ans == "4":
            export_schedule_to_excel.export_emp_to_excel_menu()
        elif ans.lower() == "quit" or ans == "0": 
            clear_screen.clear_screen()
            print("Thank you for scheduling with us!")
            running = False
            sys.exit(0)
        else:
            clear_screen.clear_screen()
            print("Please enter a valid option.\n")
        print("Lifeguard Page[1]\nBeach Page[2]\nMake Schedule[3]\nExport Schedule[4]\nQuit[0]")