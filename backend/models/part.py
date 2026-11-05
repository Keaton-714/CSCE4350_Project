class Part:
    def __init__(self, part_id, name, description, price, category):
        self.part_id = part_id
        self.name = name
        self.description = description
        self.price = price
        self.category = category

    def to_dict(self):
        return {
            "part_id": self.part_id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "category": self.category
        }