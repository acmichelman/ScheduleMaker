#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
import sqlite3

from . import clear_screen
from . import main_menu

from .db import DB_PATH, ensure_db_dir


"""
Project:    Schedule Maker
File:       main.py
Author:     Alexander Michelman
Created:    10-21-2025
Description:
    A schedule maker for Town OF Hempstead Ocean Lifeguards designed to take into account different beach staffing
        needs.

Example:
    $ python main.py

License:    MIT License2
"""

def init_db():
    ensure_db_dir()

    with sqlite3.connect(DB_PATH) as con:
        cur = con.cursor()
        # Make names not case sensitive and enforce uniqueness on (FirstName, LastNname)
        # SQLite Autoincrement will assign a # between 1 - 9223372036854775807
        #   Employee table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS Employees (
                EmployeeID INTEGER PRIMARY KEY AUTOINCREMENT,
                FirstName TEXT NOT NULL COLLATE NOCASE,
                LastName  TEXT NOT NULL COLLATE NOCASE,
                EmployeeRank       TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                DatePromoted       TEXT,
                EvaluationScore INTEGER NOT NULL DEFAULT 3,
                CanSchedule INTEGER NOT NULL CHECK (CanSchedule IN (0,1)) DEFAULT 1,    
                LastBeach       INTEGER,
                UNIQUE(FirstName, LastName)  -- prevents duplicates
            );
        """)
        con.commit()

        #   Beach table
        #   SQL normalization used for small, medium, large, between 1-5, true, false (DONT FORGET IT CANNOT BE CAPTALIZED)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS Beaches (
                BeachID INTEGER PRIMARY KEY AUTOINCREMENT,
                BeachName TEXT NOT NULL COLLATE NOCASE,
                BeachSize TEXT NOT NULL CHECK (BeachSize IN ('small', 'medium', 'large')),
                BeachActivity INTEGER NOT NULL CHECK (BeachActivity BETWEEN 1 AND 5),
                BeachOpen INTEGER NOT NULL CHECK (BeachOpen IN (0,1)) DEFAULT 1,
                UNIQUE(BeachName)
            );
        """)

        #   Seed data. Our list of beach info to be pre loaded into DB upon programs first run.
        beach_seed = [
            ("Civic", "medium", 2),
            ("Middle", "small", 1),
            ("2Chair", "medium", 3),
            ("Main", "large", 3),
            ("7Chair", "small", 1),
            ("Malibu", "large", 4),
            ("Nassau1", "small", 2),
            ("Nassau2", "large", 3),
            ("Nassau5", "medium", 3),
            ("Reef", "large", 4),
            ("Anchor", "small", 2),
            ("EastLido", "small", 1),
            ("MainLido", "medium", 3),
            ("WestLido", "small", 2),
            ("LidoWest", "large", 5),
            ("SurfingBay", "small", 1),
            ("EAB", "large", 4),
            ("Seaglades", "medium", 2),
        ]

        #   Our for loop. 
        # MySQLCursor.executemany() Method-This method prepares a database operation (query or command) and executes it against all parameter sequences or mappings found in the sequence seq_of_params. Its just a for loop man. figure it out
        #   para: bId (Beach ID), bN(Beach Name), bS(Beach Size), bA(Beach Activity), bO(Beach Open)
        cur.executemany("""
            INSERT OR IGNORE INTO Beaches (BeachName, BeachSize, BeachActivity)
            VALUES (?, ?, ?);
        """, [(bN, bS.lower(), bA) for (bN, bS, bA) in beach_seed])

        #   Schedule Table table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS Schedules (
                ScheduleID INTEGER PRIMARY KEY AUTOINCREMENT,
                SchedulePeriodID INTEGER NOT NULL,
                SchedulePeriod TEXT NOT NULL,
                BeachID INTEGER NOT NULL,
                EmpID INTEGER NOT NULL,
                EmpDaysOff TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                BeachNameText TEXT NOT NULL,
                FirstLastNameText TEXT NOT NULL,
                EmpRank TEXT NOT NULL
            );
        """)


        con.commit()

def main():
    init_db()
    clear_screen.clear_screen()
    main_menu.main_menu()



if __name__ == "__main__":
    main()