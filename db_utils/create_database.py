import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve PostgreSQL password from environment variable
postgres_password = os.getenv("POSTGRESQL_PW")

# Database connection configuration
db_name = "webshop"
user = "postgres"
host = "localhost"
port = 5432

def create_database():
    """
    Creates the PostgreSQL database if it does not already exist.

    Connects to the default 'postgres' database and checks whether the database
    named `db_name` exists. If not, it creates the database.

    Prints confirmation messages or error information.
    """
    try:
        # Connect to PostgreSQL instance (default 'postgres' database)
        connection = psycopg2.connect(
            user=user,
            password=postgres_password,
            host=host,
            port=port,
            dbname="postgres"
        )
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = connection.cursor()

        # Check if database already exists
        cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{db_name}'")
        exists = cursor.fetchone()

        if not exists:
            cursor.execute(f"CREATE DATABASE {db_name}")
            print(f"✅ Database '{db_name}' was successfully created.")
        else:
            print(f"ℹ️  Database '{db_name}' already exists.")

        cursor.close()
        connection.close()

    except Exception as e:
        print("❌ Error occurred while creating the database:", e)

if __name__ == "__main__":
    create_database()
