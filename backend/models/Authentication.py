from werkzeug.security import (generate_password_hash, check_password_hash)

class Authentication:
    def __init__(self):
        pass
    
    def hash_password(self, password: str) -> str:
        return generate_password_hash(password)
    
    def verify_password(
        self, password: str, password_hash: str) -> bool:
        return check_password_hash(password_hash, password)
    
    def login(self, email: str, password: str) -> bool:
        # TODO: Look up the user in SQLite
        # TODO: Verify the stored password hash
        # TODO: Create an authenticated session
        pass
    
    def logout(self):
        # TODO: Clear the authenticated session
        pass