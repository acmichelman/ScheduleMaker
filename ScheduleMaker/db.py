from pathlib import Path

#   Database path so we wont need to call path each time

DB_PATH = Path(__file__).resolve().parent / "DatabaseFold" / "TOHLifeguardDB"

def ensure_db_dir() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

