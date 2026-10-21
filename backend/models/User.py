
class User:
    def __init__(self, userId, email, passwordHash, firstName, lastName):
        self.userId = userId # TODO: Database will handle userId creation (users will sign in with email and pass)
        self.email = email
        self.passwordHash = passwordHash
        self.firstName = firstName
        self.lastName = lastName
