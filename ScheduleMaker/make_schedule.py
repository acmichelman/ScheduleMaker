import sqlite3
from pathlib import Path
from datetime import datetime
from . import clear_screen, main_menu

DB_PATH = Path(__file__).resolve().parent / "DatabaseFold" / "TOHLifeguardDB"

#   This func is to get all relevent employee info and store it in a dictionary
def call_employee_info_to_store_in_dict() -> dict:
    with sqlite3.connect(str(DB_PATH)) as con:
        cur = con.cursor()
        cur.execute("""SELECT EmployeeID, FirstName, LastName, EmployeeRank, DatePromoted, EvaluationScore, CanSchedule, LastBeach
                    FROM Employees
                    WHERE CanSchedule = 1
                    ORDER BY LastName, FirstName
                    """)
        rows = cur.fetchall()

    #   Our employee info will be stored in this dict. Be sure to refrence when making schedule
    employees_by_id: dict[int, dict] = {}
    
    for (emp_id, first, last, rank, date_promoted, eval_score, can_schedule, last_beach) in rows:
        employees_by_id[emp_id] = {
            "EmployeeID": emp_id,
            "FirstName": first,
            "LastName": last,
            "EmployeeRank": rank,
            "DatePromoted": date_promoted,
            "EvaluationScore": eval_score,
            "CanSchedule": bool(can_schedule),   #  No longer getting this if flase :)
            "LastBeach": last_beach,
            #   FIELDS TO BE USED LATRER
            "DaysAssigned": set(),
        }

    return employees_by_id

#   This func is to get all relevent beach info and store it in a dictionary
def call_beach_info_to_store_in_dict() -> dict:
    with sqlite3.connect(str(DB_PATH)) as con:
        cur = con.cursor()
        cur.execute("""SELECT BeachID, BeachName, BeachSize, BeachActivity, BeachOpen
                    FROM Beaches
                    ORDER BY BeachID
                    """)
        rows = cur.fetchall()

    #   Our beach info will be stored in this dict
    beach_by_id: dict[int, dict] = {}
    
    for (beach_id, beach_name, beach_size, beach_activity, beach_open) in rows:
        beach_by_id[beach_id] = {
            "BeachID": beach_id,
            "BeachName": beach_name,
            "BeachSize": beach_size,
            "BeachActivity": beach_activity,
            "BeachOpen": bool(beach_open),
        }

    return beach_by_id

#   Takes our beach_by_id dict which contains all info stored in DB and alters it to now be a dict of a dict and store lifeguards in
def build_schedule_buckets(beach_by_id: dict[int, dict]) -> dict[int, dict]:
    schedule_by_beach: dict[int, dict] = {}

    for beach_id, b_open in beach_by_id.items():
        #   Only schedule beaches that are open
        if not b_open["BeachOpen"]:
            continue

        schedule_by_beach[beach_id] = {
            "BeachID": beach_id,
            "BeachName": b_open["BeachName"],
            "BeachSize": b_open["BeachSize"],
            "BeachActivity": b_open["BeachActivity"],
            "Required": size_to_required(b_open["BeachSize"]),  #   1/2/3
            "Assigned": [],  #  list of EmployeeID assigned here
        }

    return schedule_by_beach

#   Just truns beach_size (small, medium, large) and turn it into (1,2,3)
def size_to_required(size: str) -> int:
    s = str(size).strip().lower()
    if s == "small":
        return 1
    if s == "medium":
        return 2
    if s == "large":
        return 3
    #   default 4 safety
    return 1

#   Logic that creates actueal schedule
def schedule_emp_logic():
    #   Get each dict for useage
    emp_dict = call_employee_info_to_store_in_dict()
    beach_dict = call_beach_info_to_store_in_dict()
    beach_bucket_dict = build_schedule_buckets(beach_dict)

    # all guards as individueal dicts
    senior_lieutenants = []
    lieutenants = []
    senior_guards = []
    lifeguards = []

    for emp_id, emp in emp_dict.items():
        rank = str(emp.get("EmployeeRank", "")).strip().lower()

        if rank == "senior lieutenant":
            senior_lieutenants.append(emp)
        elif rank == "lieutenant":
            lieutenants.append(emp)
        elif rank == "senior guard":
            senior_guards.append(emp)
        elif rank == "lifeguard":
            lifeguards.append(emp)
    print(" ")

def menu_options():
    print("\nMenu Options")
    print("Make Schedule[1] \nBack[2]")

#   Our menu that user gets brought to when switching pages.
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
            schedule_emp_logic()
        elif ans.lower() == "back" or ans == "2":
            running = False
            main_menu.main_menu()
        else:
            print("Please pick a different option")
        menu_options()