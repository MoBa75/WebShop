from datamanager.database import engine
from datamanager.models import Base

def drop_tables():
    """
    Drops all tables in the database.
    Use with caution as this deletes all data!
    """
    print("Dropping all tables...")
    Base.metadata.drop_all(bind=engine)
    print("All tables dropped.")

if __name__ == "__main__":
    drop_tables()
