class Order:
    def __init__(self, order_id, customer_id, store_id, order_date, status):
        self.order_id = order_id
        self.customer_id = customer_id
        self.store_id = store_id
        self.order_date = order_date
        self.status = status

        self.items = []

    # Needs OrderItem object
    def add_item(self, item):
        self.items.append(item)


    def calculate_total(self):
        total = 0
        for item in self.items:
            total+= item.calculate_subtotal()

        return total