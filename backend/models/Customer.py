from backend.models.user import User

class Customer(User):
    def __init__(self, user_id, customer_id, email, password_hash, fname, lname, phone_number):
        super().__init__(user_id, email, password_hash, fname, lname, phone_number)
        self.customer_id = customer_id