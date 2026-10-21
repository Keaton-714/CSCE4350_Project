from backend.models.User import User

class Employee(User):
    def __init__(self, userID, email, passwordHash, firstName, lastName, salary):
        super().__init__(userID, email, passwordHash, firstName, lastName)
        self.salary = salary
