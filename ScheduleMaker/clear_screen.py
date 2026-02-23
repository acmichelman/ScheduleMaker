import os

def clear_screen():
    #   Clear the console screen depending on OS.
    os.system('cls' if os.name == 'nt' else 'clear')