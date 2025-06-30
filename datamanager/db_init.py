from datamanager.database import engine
from datamanager.models import Base


def init_db():
    """
    Initializes the database by creating all tables defined in the models.

    This function uses SQLAlchemy's metadata to create all tables based on
    the Base model definitions and binds them to the configured database engine.
    """
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    # Run the database initialization when this file is executed directly
    init_db()
