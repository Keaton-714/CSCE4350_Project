from backend.models.user import User

class Employee(User):
    def __init__(self, user_id, employee_id, email, password_hash, fname, lname, phone_number, store_id):
        super().__init__(user_id, email, password_hash, fname, lname, phone_number)
        self.store_id = store_id
        self.employee_id = employee_id
