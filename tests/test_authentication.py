from backend.routes.authentication import Authentication
from flask import session 
from backend.app import app 
import backend.database.connection as db_connection

# Python built-in testing utilities
import sqlite3
import tempfile
from pathlib import Path
from unittest.mock import patch

auth = Authentication()

print("Authentication object created successfully!")

# Testing code only !!!

# Testing password verification and pass word hashing, Correct and Incorrect passwords
password = "TestPassword123!"
password_hash = auth.hash_password(password)
print ("Password verification:", auth.verify_password(password, password_hash)) 
print("Generated password hash: " , password_hash)
print("Wrong password:", auth.verify_password("WrongPassword!", password_hash))

# Testing session recording and removal by user_id
with app.test_request_context("/"):
    session["user_id"] = 1
    print("Session user ID:", session["user_id"])

    auth.logout()
    print("Session after logout: ", session.get("user_id"))

# Testing email that doesn't exist
with app.test_request_context("/"):
    result = auth.login("notarealuser@example.com", "WrongPassword123!")
    print("Unknown user login:", result)


# Build a temporary test database for testing, this does not affect autoone.db, 
with tempfile.TemporaryDirectory() as temp_dir:
    test_db = Path(temp_dir) / "test_auth.db"

    connection = sqlite3.connect(test_db)
    connection.execute("""
        CREATE TABLE User (
            user_id INTEGER PRIMARY KEY,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    """)
    connection.commit()
    connection.close()

    print("Temporary test database created!")

    connection = sqlite3.connect(test_db)

    test_password = "TestPassword123!"
    test_hash = auth.hash_password(test_password)

    connection.execute(
        """
        INSERT INTO User (email, password_hash)
        VALUES (?, ?)
        """,
        ("test@example.com", test_hash)
    )

    connection.commit()
    connection.close()

    print("Temporary test user created!")

    with patch.object(db_connection, "DB_PATH", test_db):
        with app.test_request_context("/"):
            result = auth.login("test@example.com", "TestPassword123!")

            print("Successful login:", result)
            print("Logged-in user ID:", session.get("user_id"))

            # Test login with an incorrect password
            auth.logout()

            result = auth.login("test@example.com", "WrongPassword!")
            print("Incorrect login:", result)
            print("Session after failed login:", session.get("user_id"))