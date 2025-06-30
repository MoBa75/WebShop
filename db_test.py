# db_test.py

from datamanager.database import SessionLocal
from sqlalchemy import text

def test_connection():
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        print("✅ Verbindung zur PostgreSQL-Datenbank erfolgreich!")
    except Exception as e:
        print("❌ Verbindungsfehler:", e)
    finally:
        db.close()

if __name__ == "__main__":
    test_connection()
