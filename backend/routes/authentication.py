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
    
        pass
    
    def logout(self):
        # TODO: Clear the authenticated session
        session.pop("user_id", None)
        pass