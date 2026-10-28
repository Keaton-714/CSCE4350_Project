class OrderItem:
    def __init__(self, order_item_id, part_id, quantity, unit_price):
        self.order_item_id = order_item_id
        self.part_id = part_id
        self.quantity = quantity
        self.unit_price = unit_price

    def calculateSubtotal(self):
        return self.quantity * self.unit_price