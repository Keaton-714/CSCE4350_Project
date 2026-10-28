from backend.models.user import User

class Employee(User):
    def __init__(self, user_id, employee_id, email, password_hash, fname, lname, store_id, salary):
        super().__init__(user_id, email, password_hash, fname, lname)
        self.store_id = store_id
        self.employee_id = employee_id
