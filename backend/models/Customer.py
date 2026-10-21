from backend.models.User import User

class Customer(User):
    def __init__(self, userID, email, passwordHash, firstName, lastName):
        super().__init__(userID, email, passwordHash, firstName, lastName)