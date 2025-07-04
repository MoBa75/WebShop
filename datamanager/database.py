import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# Load environment variables from a .env file
load_dotenv()

# Retrieve the PostgreSQL password from the environment variable
postgres_password = os.getenv("POSTGRESQL_PW")

# Define the PostgreSQL database connection URL
DATABASE_URL = f"postgresql://postgres:{postgres_password}@localhost:5432/webshop"

# Create a SQLAlchemy engine to connect to the PostgreSQL database
engine = create_engine(DATABASE_URL)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for declarative class definitions (models will inherit from this)
Base = declarative_base()


def get_db():
    """
    Provides a database session for dependency injection in FastAPI routes.

    This generator function creates a SQLAlchemy session using SessionLocal and yields it.
    After the route function completes, the session is automatically closed.

    Usage:
        Add as a dependency in FastAPI routes using `Depends(get_db)`.

    Yields:
        Session: A SQLAlchemy database session.
    """
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()

