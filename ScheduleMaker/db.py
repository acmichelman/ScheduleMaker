from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "DatabaseFold" / "TOHLifeguardDB"

def ensure_db_dir() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

