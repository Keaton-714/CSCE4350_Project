from pathlib import Path
from backend.database.connection import get_connection

# Get the directory containing this Python file
DATABASE_DIR = Path(__file__).resolve().parent

def initialize_database():
    connection = get_connection()

    try:
        # Read the SQL schema
        schema = (DATABASE_DIR / "schema.sql").read_text()

        # Create the tables
        connection.executescript(schema)

        # Read the sample data
        test_data = (DATABASE_DIR / "test_data.sql").read_text()

        # Insert the sample records
        connection.executescript(test_data)

        connection.commit()

        print("Database initialized successfully!")

    finally:
        connection.close()


if __name__ == "__main__":
    initialize_database()