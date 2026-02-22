import sqlite3
import random
from pathlib import Path
from datetime import datetime, timedelta
from enum import Enum
from . import clear_screen, main_menu

#DB_PATH = Path(__file__).resolve().parent / "DatabaseFold" / "TOHLifeguardDB"
from .db import DB_PATH, ensure_db_dir

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

#--------------------------Get Beach Name/ Emp First/ Last Name--------
#   Two helper functions. Just to make exporting to Excel easier so I dont need to get info from 3 different DB
#   Return the beach name as TEXT (Maked Exporting easier with excel so its all on one DB)
def get_beach_name_text(beach: dict) -> str:
    
    return str(beach.get("BeachName", ""))

#   Return 'FirstLastName' as TEXT which is a combination of FirstName & LastName from Employees DB once again for exporting
def get_first_last_name_text(emp: dict) -> str:
    first = str(emp.get("FirstName", ""))
    last  = str(emp.get("LastName", ""))
    if not first and not last:
        return ""
    first_initial = first[0].upper() if first else "" # Remove last name spaces if any. Dont remeber if I stripped these off
    last_clean = "".join(last.split())
    return f"{first_initial}. {last_clean}"

def get_emp_rank(emp: dict) -> str:

    return str(emp.get("EmployeeRank", ""))

#--------------------------End Get Beach Name/ Emp First/ Last Name--------

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
            print("Please enter yes or no")

#   Helper function that will get the last SchedulePeriodID if it exists so we can increment/ get SchedulePeriod (2 week block) to auto get date
def get_last_schedule_period():
    with sqlite3.connect(DB_PATH) as con:
        cur = con.cursor()
        cur.execute("""
            SELECT SchedulePeriodID, SchedulePeriod
            FROM Schedules
            ORDER BY SchedulePeriodID DESC
            LIMIT 1;
        """)
        row = cur.fetchone()
        if row is None:
            return None, None
        return row[0],row[1]
        
    
def get_pay_period_prompt():
    #   This will get our two week work period
    print("Please enter the pay period starting with your first week (MM/DD/YYYY): ")
    while True:
        first_week_period = input().strip()
        try:
            start_dt = datetime.strptime(first_week_period, "%m/%d/%Y")
            break
        except ValueError:
            print("Invalid date. Please use MM/DD/YYYY: ")
    second_week_period = start_dt + timedelta(days=13)
    second_week_period = second_week_period.date()    
    second_week_period = second_week_period.strftime("%m/%d/%Y")
    return first_week_period, second_week_period
    

def save_schedule_to_db(schedule_by_beach: dict[int,dict], emp_dict: dict[int,dict],):
    """
    ScheduleID INTEGER PRIMARY KEY AUTOINCREMENT,
    SchedulePeriodID INTEGER NOT NULL,
    SchedulePeriod TEXT NOT NULL,
    BeachID INTEGER NOT NULL,
    EmpID INTEGER NOT NULL,
    EmpDaysOff TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    BeachName TEXT NOT NULL,
    FirstLastName TEXT NOT NULL,
    EmpRank TEXT NOT NULL


    get set sechdulePeriodID here
    for loop where we connect to DB 
        get each piece of data
        set it to db to be saved
    """
    #   Gets last SchedulePeriodID/ SchedulePeriod for auto increment
    #   Also used to check if user wants to enter new pay period (Check if its null then get first set one. else prompt user if they want to use)
    sp_id_db = get_last_schedule_period() #    Gets SchedulePeriodID & SchedulePeriod
    sp_id, sp = sp_id_db
    if sp_id != None:
        sp_id += 1
    else:
        sp_id = 1

    if sp is not None and " - " in sp:
        prev_first_str, prev_second_str = (s.strip() for s in sp.split(" - ", 1))

        #   prev_second_str is the end marker we stored 13 days after start (monday - sunday twice)
        prev_second_dt = datetime.strptime(prev_second_str, "%m/%d/%Y").date()

        #   Next pay period
        next_first_dt  = prev_second_dt + timedelta(days=1)
        next_second_dt = next_first_dt + timedelta(days=13)

        first_week_period  = next_first_dt.strftime("%m/%d/%Y")
        second_week_period = next_second_dt.strftime("%m/%d/%Y")

        sp = f"{first_week_period} - {second_week_period}"
    else:
        first_week_period, second_week_period = get_pay_period_prompt()
        sp = f"{first_week_period} - {second_week_period}"

    #   Confirm with user if period date is correct
    while True:
        
        print(f"Is this the correct schedule period: {first_week_period}, {second_week_period} (Yes/No)")
        confirm_date = input().strip().lower()
        if confirm_date == 'yes' or confirm_date == 'y':
            sp = f"{first_week_period} - {second_week_period}"   #  Convert to text from tuple TEXT
            break
        elif confirm_date == 'no' or confirm_date == 'n':
            first_week_period, second_week_period = get_pay_period_prompt()
            sp = f"{first_week_period} - {second_week_period}"
            
        else:
            print("Please enter yes or no")
    
    #   Save each beach/ employee/ 2 days off combination
    with sqlite3.connect(DB_PATH) as con:
        cur = con.cursor()
        for beach_id in sorted(schedule_by_beach.keys()):
            beach = schedule_by_beach[beach_id]
            beach_name_text = get_beach_name_text(beach) 
            for emp_id in beach.get("Assigned", []):
                emp = emp_dict.get(emp_id)
                if not emp:
                    continue
                first_last_text = get_first_last_name_text(emp)
                emp_rank = get_emp_rank(emp) 
                days_off_text = convert_days_off_to_text(emp.get("DaysAssigned", set()))
                cur.execute("""INSERT INTO Schedules
                            (SchedulePeriodID, SchedulePeriod, BeachID, EmpID, EmpDaysOff, BeachNameText, FirstLastNameText, EmpRank)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                            """, (sp_id, sp, beach_id, emp_id, days_off_text, beach_name_text, first_last_text, emp_rank))
    con.commit()
    print(f"Schedule saved under schedule period ID: {sp_id}")




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