import sys

import lifeguard_list
import add_lifeguard
import remove_lifeguard
import clear_screen

def main_menu():
    """Main menu loop."""
    clear_screen.clear_screen()
    print("Welcome to the Lifeguard Schedule Maker.\n")
    print("Please type which menu to navigate to:\n")
    print("Lifeguard List[1]\nAdd Lifeguard[2]\nRemove Lifeguard[3]\nQuit[4]\n")

    running = True
    while running:
        ans = input("> ").strip()

        if ans.lower() == "lifeguard list" or ans == "1":
            lifeguard_list.lifeguard_list()
        elif ans.lower() == "add lifeguard" or ans == "2":
            add_lifeguard.add_lifeguard()
        elif ans.lower() == "remove lifeguard" or ans == "3":
            remove_lifeguard.remove_lifeguard()
        elif ans.lower() == "quit" or ans == "4": 
            clear_screen.clear_screen()
            print("Thank you for scheduling with us!")
            running = False
            sys.exit(0)
        else:
            clear_screen.clear_screen()
            print("Please enter a valid option.\n")
            print("Lifeguard List\nAdd Lifeguard\nRemove Lifeguard\nQuit\n")
