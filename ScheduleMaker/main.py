#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import clear_screen
import main_menu
import sqlite3

"""
Project:    Schedule Maker
File:       main.py
Author:     Alexander Michelman
Created:    10-21-2025
Description:
    A schedule maker for Town OF Hempstead Ocean Lifeguards designed to take into account different beach staffing
        needs, Jr Lifeguard instructors, special requests, experience, events, ect

Example:
    $ python main.py

License:    MIT License2
"""

DB_PATH = "DatabaseFold/TOHLifeguardDB"

def init_db():
    with sqlite3.connect(DB_PATH) as con:
        cur = con.cursor()
        # Make names not case sensitive and enforce uniqueness on (FirstName, LastNname)
        # SQLite Autoincrement will assign a # between 1 - 9223372036854775807
        cur.execute("""
            CREATE TABLE IF NOT EXISTS Employees (
                EmployeeID INTEGER PRIMARY KEY AUTOINCREMENT,
                FirstName TEXT NOT NULL COLLATE NOCASE,
                LastName  TEXT NOT NULL COLLATE NOCASE,
                EmployeeRank       TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                DatePromoted       TEXT,
                EvaluationScore INTEGER NOT NULL DEFAULT 3,
                UNIQUE(FirstName, LastName)  -- prevents duplicates
            );
        """)
        con.commit()

def main():
    init_db()
    clear_screen.clear_screen()
    main_menu.main_menu()



if __name__ == "__main__":
    main()