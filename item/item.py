from item.category import CategoryItem


class Item:

    def __init__(self, name='Undefined', icon=None, price=0, weight=0, category=CategoryItem.ITEM):
        self.name = name
        self.icon = icon
        self.price = price
        self.weight = weight
        self.category = category
