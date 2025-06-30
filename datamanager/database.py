import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

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
