import sqlite3
import random
from pathlib import Path
from datetime import datetime
from enum import Enum
from itertools import combinations
from . import clear_screen, main_menu

DB_PATH = Path(__file__).resolve().parent / "DatabaseFold" / "TOHLifeguardDB"

class Day(Enum):
    MON = 0
    TUE = 1
    WED = 2
    THU = 3
    FRI = 4
    SAT = 5
    SUN = 6

#------------------------Get beach/employee info into dicts-----------------------
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
#------------------------End Get beach/employee info into dicts-----------------------

#----------------------Schedule Employees on beaches logic--------------------------
#   Will assign employees to beahces in their own dict for ease of reading
#   ROUND ROBIN for random/ make sure each beach gets a SL before one gets one again
def assign_senior_lieutenants_to_beaches(senior_lieutenants: list[dict], schedule_by_beach: dict[int, dict],):
    large_beaches = []
    for beach_id, beach in schedule_by_beach.items():
        if beach["BeachSize"] == "large":
            large_beaches.append(beach)

    #   Put them in a random order to help varibility
    random.shuffle(large_beaches)
    random.shuffle(senior_lieutenants)

    sl_idx = 0

    while sl_idx < len(senior_lieutenants):#   Loop index and SL
        beach = large_beaches[(sl_idx) % len(large_beaches)] #  get how many large beaches then if remainder is 0 then you have filled each beach once
        beach["Assigned"].append(senior_lieutenants[sl_idx]["EmployeeID"])
        sl_idx += 1

#   Asign a lieutenant to beach
"""
    First add a lieutenant to each large beach while lieutenant != 0
    if lieutenant != 0 once set to large beachs add single lieutanent to medium beach
    if lieutenant != 0 once set to large/ medium beaches once set remaining lieutenants to large beaches
    -being sure to set to one beach each before setting a second
"""
def assign_lieutenants_to_beaches(lieutenants: list[dict], schedule_by_beach: dict[int, dict]):
    #   collect beaches by size
    large_beaches = []
    medium_beaches = []

    #   get all "large"/"medium" beaches to be stored in beach pool
    for beach_id, beach in schedule_by_beach.items():
        size = beach.get("BeachSize") 
        if size == "large":
            large_beaches.append(beach)
        elif size == "medium":
            medium_beaches.append(beach)

    if not lieutenants:
        return
    if not large_beaches and not medium_beaches:
        return
    
    #   randomize 
    random.shuffle(lieutenants)
    random.shuffle(large_beaches)
    random.shuffle(medium_beaches)

    #   Lieutenant index
    li_idx = 0

    #   step 1- one lieutenant to each large beach
    for beach in large_beaches:
        if li_idx >= len(lieutenants):
            return
        beach["Assigned"].append(lieutenants[li_idx]["EmployeeID"])
        li_idx += 1

    #   step 2- one lieutenant to each medium beach
    for beach in medium_beaches:
        if li_idx >= len(lieutenants):
            return
        beach["Assigned"].append(lieutenants[li_idx]["EmployeeID"])
        li_idx += 1

    #   step 3- remaining lieutenants to large beaches via round robin
    if not large_beaches:
        return
    
    while li_idx < len(lieutenants):
        beach = large_beaches[(li_idx) % len(large_beaches)] #  Same remaninder logic
        beach["Assigned"].append(lieutenants[li_idx]["EmployeeID"])
        li_idx += 1
    
    #   Assign Senior Guards to beaches
    """
    Step one & step two are the same as lieutenants
    First assign Senior guards to medium beach while senior guards != 0
    if senior guard != 0 assign single senior guard to small beach
    Now check if medium beach has lieutenant and if it DOESNT then add another senior guard to medium beach
        else senior guard != 0 & single senior guard set to medium beach/small beach assign senior guard to another small beach while senior guard != 0
    """
def assign_senior_guards_to_beaches(senior_guards: list[dict], schedule_by_beach: dict[int, dict], lieutenant_ids: set[int],):   #    Get IDs of lieutenants that exist in your schedule pool. Get it. Lifeguard joke. Ha.
    medium_beaches = []
    small_beaches = []

    for beach_id, beach in schedule_by_beach.items():
        size = beach.get("BeachSize")
        if size == "medium":
            medium_beaches.append(beach)
        elif size == "small":
            small_beaches.append(beach)

    if not senior_guards:
        return
    if not medium_beaches and not small_beaches:
        return
    
    #   Randomizer
    random.shuffle(senior_guards)
    random.shuffle(medium_beaches)
    random.shuffle(small_beaches)

    #   Senior Guard index
    sg_idx = 0

    #   step 1- one SG to each medium beach
    for beach in medium_beaches:
        if sg_idx >= len(senior_guards):
            return
        beach["Assigned"].append(senior_guards[sg_idx]["EmployeeID"])
        sg_idx += 1

    #   step 2- one SG to each small beach
    for beach in small_beaches:
        if sg_idx >= len(senior_guards):
            return
        beach["Assigned"].append(senior_guards[sg_idx]["EmployeeID"])
        sg_idx += 1

    #   step 3- check if beach already has lieutenant (A nested function kinda like c++ Lambdas)
    def has_lieutenant(beach: dict) -> bool:
        assigned_ids = beach.get("Assigned", [])
        return any(emp_id in lieutenant_ids for emp_id in assigned_ids)
    
    #   step 4- remaining SG get added to SMALL beaches with NO lieutenant. We need to do same thing cause otherwise it falls outside logic above
    beaches_no_lt_small = []
    for beach_id, beach in schedule_by_beach.items():
        if beach.get("BeachSize") == "small" and not has_lieutenant(beach):
            beaches_no_lt_small.append(beach)

    random.shuffle(beaches_no_lt_small)

    if not beaches_no_lt_small:
        return

    while sg_idx < len(senior_guards):
        beach = beaches_no_lt_small[sg_idx % len(beaches_no_lt_small)]
        beach["Assigned"].append(senior_guards[sg_idx]["EmployeeID"])
        sg_idx += 1

#   Lifeguards will be assigned at beaches by large beach- 3 lifeguards, medium beach- 2 lifeguards, small beach- 1 lifeguard
def required_lifeguards_for_size(size: str) -> int:
    s = str(size).strip().lower()
    if s == "large":
        return 3
    if s == "medium":
        return 2
    if s == "small":
        return 1
    return 1  # default safety

#   Asign a lifeguard to beach
def assign_lifeguard_to_beaches(lifeguards: list[dict], schedule_by_beach: dict[int, dict],):
    if not lifeguards:
        return
    if not schedule_by_beach:
        return
    
    #   Build a list of beach dicts
    beaches = []
    for beach_id, beach in schedule_by_beach.items():
        beaches.append(beach)

    random.shuffle(lifeguards)
    random.shuffle(beaches)

    #   Lifeguard indeex
    lg_idx = 0
    beach_idx = 0 #   For round robin index

    while lg_idx < len(lifeguards):
        beach = beaches[beach_idx % len(beaches)]
        beach_idx += 1

        size = str(beach.get("BeachSize", "")).strip().lower()
        #   how many lifeguards to try to add (Large = 3, Medium = 2, Small = 1)
        if size == "large":
            to_add = 3
        elif size == "medium":
            to_add = 2
        else:
            to_add = 1  #   small or default

        #   add up to to_add lifeguards but don't go past the list length
        added = 0
        while added < to_add and lg_idx < len(lifeguards):
            beach["Assigned"].append(lifeguards[lg_idx]["EmployeeID"])
            lg_idx += 1
            added += 1
#----------------------End Schedule Employees on beaches logic--------------------------

#-----------------------Assign Days off------------------------------------------------
#   This will get us two random days off from the pool and know to reset once each day off has been used
#def days_off_cycle(shuffle: bool = True):
#    days = list(Day)
#    day_pair = list(combinations(days, 2))
#    if shuffle == True:
#        random.shuffle(day_pair)
#    return day_pair

#   Will assign two days off and add it to beach_bucket_dict["Assigned"] section
def assign_days_off(schedule_by_beach: dict[int, dict], emp_dict: dict[int, dict]):
    for beach_id, beach in schedule_by_beach.items():
        day_pool = list(Day)

        #   Loop employees in the order assigned to this beach
        for emp_id in beach.get("Assigned", []):
            emp = emp_dict.get(emp_id)
            if not emp:
                continue

            #   reset pool if empty (safety)
            if not day_pool:
                day_pool = list(Day)

            #   pick first day and remove it from pool
            first_day_off = random.choice(day_pool)
            day_pool.remove(first_day_off)

            #   reset pool if empty (safety)
            if not day_pool:
                day_pool = list(Day)

            #   pick second day (can't equal first because first was removed)
            second_day_off = random.choice(day_pool)
            day_pool.remove(second_day_off)

            #   assign to employee (store as a set of 2 days)
            emp["DaysAssigned"] = {first_day_off, second_day_off}
    

#-----------------------End Assign Days off------------------------------------------------


#----------------------------Display schdule logic-----------------
def print_schedule_via_text(schedule_by_beach: dict[int, dict], emp_dict: dict[int, dict]):
    #print(beach_bucket_dict)
        for beach_id in sorted(schedule_by_beach.keys()):
            beach = schedule_by_beach[beach_id]
            beach_name = beach.get("BeachName", "")
            assigned_ids = beach.get("Assigned", [])

            print(f"\n{beach_name}")

            for emp_id in assigned_ids:
                emp = emp_dict.get(emp_id)
                if not emp:
                    continue 
                first = emp.get("FirstName", "")
                last = emp.get("LastName", "")
                days_off = emp.get("DaysAssigned", set)
                if isinstance(days_off, set): # Should break up {<Day.FRI: 4>, <Day.MON: 0>} into something readable
                    days_off_str = "(" + ", ".join(d.name for d in sorted(days_off, key=lambda d: d.value)) + ")" 
                else:
                    days_off_str = str(days_off)
                print(f"  {first} {last} {days_off_str}")

#----------------------------End Display schdule logic-----------------
#   Logic that creates actueal schedule
def schedule_emp_logic():
    #   Get each dict for useage
    emp_dict = call_employee_info_to_store_in_dict()
    beach_dict = call_beach_info_to_store_in_dict()
    beach_bucket_dict = build_schedule_buckets(beach_dict)

    #   all guards as individueal dicts
    senior_lieutenants = []
    lieutenants = []
    senior_guards = []
    lifeguards = []

    #   all beaches as individueal sizes
    small_beach = []
    medium_beach = []
    large_beach = []

    for emp_id, emp in emp_dict.items():
        rank = str(emp.get("EmployeeRank", ""))

        if rank == "senior lieutenant":
            senior_lieutenants.append(emp)
        elif rank == "lieutenant":
            lieutenants.append(emp)
        elif rank == "senior guard":
            senior_guards.append(emp)
        elif rank == "lifeguard":
            lifeguards.append(emp)
    print(" ")

    #   CALL FUNCTIONS TO GET EMPLOYEES HERE
    #   Every employee id gets saved in beach_dict Assigned dict. Access this for our list of employees
    assign_senior_lieutenants_to_beaches(senior_lieutenants, beach_bucket_dict)
    assign_lieutenants_to_beaches(lieutenants, beach_bucket_dict)
    #   For senior guard. When we check if a medium beach has a LT or not
    lieutenant_ids = set()
    for lt in lieutenants:
        lieutenant_ids.add(lt["EmployeeID"])
    assign_senior_guards_to_beaches(senior_guards,beach_bucket_dict, lieutenant_ids)
    assign_lifeguard_to_beaches(lifeguards, beach_bucket_dict)

    assign_days_off(beach_bucket_dict, emp_dict)

    print_schedule_via_text(beach_bucket_dict, emp_dict)
    ans = save_schedule_to_db_prompt()
    if ans == 1:
        save_schedule_to_db(beach_bucket_dict,emp_dict)
    
   
#   Helper func to be used when storing days off in DB
def convert_days_off_to_text(days_off):
    if not isinstance(days_off, set) or not days_off:
        return ""

    ordered = sorted(days_off, key=lambda d: d.value)  #    MON before TUE ect...
    return ", ".join(d.name for d in ordered)

def save_schedule_to_db_prompt(): # Just asking user if we can save this or not. Important cause SchedulePeriod will increment
    print("Can save schedule? (Yes or No)")
    while True:
        can_save = input().strip().lower()
        if can_save == 'yes' or can_save == 'y':
            can_save = 1
            return 1
        elif can_save == 'no' or can_save == 'n':
            can_save = 0
            return 0
        else:
            print("Please enter true or false")

def save_schedule_to_db(beach_bucket_dict: dict[int,dict], emp_dict: dict[int,dict],):
    """
    ScheduleID INTEGER PRIMARY KEY AUTOINCREMENT,
    SchedulePeriodID INTEGER NOT NULL,
    SchedulePeriod TEXT NOT NULL,
    BeachID INTEGER NOT NULL,
    EmpID INTEGER NOT NULL,
    EmpDaysOff TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    """





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
        ans = input("> ").strip()

        if ans.lower() == "Make Schdeule" or ans == "1":
            schedule_emp_logic()
        elif ans.lower() == "back" or ans == "2":
            running = False
            main_menu.main_menu()
        else:
            print("Please pick a different option")
        menu_options()