
class User:
    def __init__(self, user_id, email, password_hash, fname, lname):
        self.user_id = user_id # TODO: Database will handle userId creation (users will sign in with email and pass)
        self.email = email
        self.password_hash = password_hash
        self.fname = fname
        self.lname = lname
