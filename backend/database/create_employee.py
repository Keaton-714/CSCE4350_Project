from getpass import getpass
from werkzeug.security import generate_password_hash
from backend.database.connection import get_connection

# One time employee creation. Doing this to put an employee correctly into the database with hashed password so we can login with this account
def create_employee():
    email = input("Employee email: ").strip()
    password = getpass("Employee password: ")
    fname = input("First name: ").strip()
    lname = input("Last name: ").strip()
    phone = input("Phone number: ").strip()
    store_id = int(input("Store ID: "))

    password_hash = generate_password_hash(password)

    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            INSERT INTO User
                (email, password_hash, fname, lname, phone_number)
            VALUES (?, ?, ?, ?, ?)
            """,
            (email, password_hash, fname, lname, phone)
        )

        user_id = cursor.lastrowid

        connection.execute(
            """
            INSERT INTO Employee (user_id, store_id)
            VALUES (?, ?)
            """,
            (user_id, store_id)
        )

        connection.commit()

        print(f"Employee created successfully. User ID: {user_id}")

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


if __name__ == "__main__":
    create_employee()