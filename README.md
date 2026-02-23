# Schedule Maker (Town of Hempstead Ocean Lifeguards)

A schedule maker for Town of Hempstead Ocean Lifeguards designed to account for different beach staffing needs.

## Features
- Employee management
  - Add a single employee or bulk import from Excel
  - Remove employees
  - Edit employee information
  - View employee list
- Beach management
  - Add beaches
  - Remove beaches
  - Edit beach information
  - View beach list
- Scheduling
  - Generate a two-week work schedule
  - Export the schedule to a single Excel file

## Requirements
- Python **3.13.1**
- Dependencies: see `requirements.txt` (currently `openpyxl`)

## Database
A SQLite database is created automatically on first run.
The database file is stored in the `DatabaseFold/` directory (created if it doesn’t exist).

## Installation & Run
```bash
python3 -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
python -m ScheduleMaker.main
```

## Excel file formatting
When program reads from a Excel file please make sure your headers match this formatting
- FirstName
- LastName
- EmployeeRank
- DatePromoted
- EvaluationScore