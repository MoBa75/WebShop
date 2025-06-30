import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()  # .env-Datei laden

postgres_password = os.getenv("POSTGRESQL_PW")

DATABASE_URL = f"postgresql://postgres:{postgres_password}@localhost:5432/webshop"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
