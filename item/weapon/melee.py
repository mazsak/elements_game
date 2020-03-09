from item.category import CategoryItem
from item.weapon.weapon import Weapon


class Melee(Weapon):

    def __init__(self, name, price=0, weight=2, category=CategoryItem.WEAPON, damage=10, durability=100):
        super().__init__(name, price, weight, category, damage, durability)
