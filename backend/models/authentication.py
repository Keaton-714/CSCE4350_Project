from werkzeug.security import (generate_password_hash, check_password_hash)
from backend.database.connection import get_connection 
from flask import session


class Authentication:
    def __init__(self):
        pass
    
    def hash_password(self, password: str) -> str:
        return generate_password_hash(password)
    
    def verify_password(self, password: str, password_hash: str) -> bool:
        return check_password_hash(password_hash, password)

    def register_customer(self, email, password, fname, lname, phone_number):
        connection = get_connection()

        try:
            # Check whether the email already exists
            existing_user = connection.execute(
                """
                SELECT user_id
                FROM User
                WHERE email = ?
                """,
                (email,)
            ).fetchone()

            if existing_user is not None:
                return False

            # Hash the password
            password_hash = self.hash_password(password)

            # Insert the new user
            cursor = connection.execute(
                """
                INSERT INTO User (email, password_hash, fname, lname, phone_number)
                VALUES (?, ?, ?, ?, ?)
                """,
                (email, password_hash, fname, lname, phone_number)
            )

            # Retrieve the generated user ID
            user_id = cursor.lastrowid

            # Insert the customer record
            connection.execute(
                """
                INSERT INTO Customer (user_id)
                VALUES (?)
                """,
                (user_id,)
            )

            connection.commit()
            return True

        except Exception:
            connection.rollback()
            raise

        finally:
            connection.close()
    
    def login(self, email: str, password: str) -> bool:

        # Query the SQLite database for a user matching the provided email.
        # Retrieve the matching record and close the database connection
        connection = get_connection()

        try:
            cursor = connection.execute(
            
                """
                SELECT user_id, email, password_hash
                FROM User
                WHERE email = ? 
                """,
                (email,)
            )

            user = cursor.fetchone()
        finally:
            connection.close()
        
        # Reject the login attemp if no matching user exists.
        if user is None:
            return False

        # Verify the entered password against the stored password hash.
        # Reject the login attempt if the password is incorrect.
        if not self.verify_password(password, user["password_hash"]):
            return False

        # Store the authenticated user's ID in the Flask session
        session["user_id"] = user["user_id"]
        return True
    
    
    def logout(self):
        # TODO: Clear the authenticated session
        session.pop("user_id", None)
        pass