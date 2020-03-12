from direct.gui.DirectLabel import DirectLabel, DirectFrame, WindowProperties
from direct.gui.DirectScrolledList import DirectScrolledList

import window
from gui_equipment import GUIEquipment
from item.category import CategoryItem

numItemsVisible = 4
itemHeight = 0.11


class Equipment:

    def __init__(self, player):
        self.master = window.Window.get_instance()
        self.items = {}
        for category in CategoryItem:
            self.items[category.name] = []
        self.gui = GUIEquipment(self.items)
        self.visible = False

        self.gui.hide()

    def equipment_change_visibility(self, player):
        if self.visible:
            self.gui.hide()
            self.master.change_mouse_visibility()
            self.master.taskMgr.add(player.camera_control, "Camera Control")
            self.visible = False
        else:
            self.gui.items = self.items
            self.gui.show()
            self.master.change_mouse_visibility()
            self.master.taskMgr.remove("Camera Control")
            self.visible = True
