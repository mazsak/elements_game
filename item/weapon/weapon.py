from item.category import CategoryItem
from item.item import Item


class Weapon(Item):

    def __init__(self, name, price=0, weight=2, category=CategoryItem.WEAPON, damage=10, durability=100):
        super().__init__(name, price, weight, category)
        self.damage = damage
        self.durability = durability
