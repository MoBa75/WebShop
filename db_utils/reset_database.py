import subprocess
import sys
from db_utils import drop_tables, init_tables

def reset_database():
    """
    Resets the database:
    1. Create database if not exists
    2. Drop all tables
    3. Create all tables
    """
    print("Creating database if it doesn't exist...")
    # create_database.py mit Python aufrufen
    subprocess.run([sys.executable, "db_utils/create_database.py"], check=True)

    print("Dropping tables...")
    drop_tables.drop_tables()

    print("Creating tables...")
    init_tables.init_db()

    print("Database reset complete.")

if __name__ == "__main__":
    reset_database()
