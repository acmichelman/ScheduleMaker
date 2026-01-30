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
                BeachOpen TEXT NOT NULL CHECK (BeachOpen IN ('true', 'false')),
                UNIQUE(BeachName)
            );
        """)

        #   Seed data. Our list of beach info to be pre loaded into DB upon programs first run.
        beach_seed = [
            ("Civic", "medium", 2, "true"),
            ("Middle", "small", 1, "true"),
            ("2Chair", "medium", 3, "true"),
            ("Main", "large", 3, "true"),
            ("7Chair", "small", 1, "true"),
            ("Malibu", "large", 4, "true"),
            ("Nassau1", "small", 2, "true"),
            ("Nassau2", "large", 3, "true"),
            ("Nassau5", "medium", 3, "true"),
            ("Reef", "large", 4, "true"),
            ("Anchor", "small", 2, "true"),
            ("EastLido", "small", 1, "true"),
            ("MainLido", "medium", 3, "true"),
            ("WestLido", "small", 2, "true"),
            ("LidoWest", "large", 5, "true"),
            ("SurfingBay", "small", 1, "true"),
            ("EAB", "large", 4, "true"),
            ("Seaglades", "medium", 2, "true"),
        ]

        #   Our for loop. 
        # MySQLCursor.executemany() Method-This method prepares a database operation (query or command) and executes it against all parameter sequences or mappings found in the sequence seq_of_params. Its just a for loop man. figure it out
        #   para: bId (Beach ID), bN(Beach Name), bS(Beach Size), bA(Beach Activity), bO(Beach Open)
        cur.executemany("""
            INSERT OR IGNORE INTO Beaches (BeachName, BeachSize, BeachActivity, BeachOpen)
            VALUES (?, ?, ?, ?);
        """, [(bN, bS.lower(), bA, bO.lower()) for (bN, bS, bA, bO) in beach_seed])


        con.commit()

def main():
    init_db()
    clear_screen.clear_screen()
    main_menu.main_menu()



if __name__ == "__main__":
    main()