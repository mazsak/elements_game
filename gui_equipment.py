from direct.gui.DirectLabel import DirectFrame
from direct.gui.DirectScrolledFrame import DirectScrolledFrame
from direct.gui.DirectScrolledList import DirectButton
from panda3d.core import LVecBase3f, LPoint3f

import window
from item.category import CategoryItem

numItemsVisible = 4
itemHeight = 0.11


class GUIEquipment:

    def __init__(self, items, **kw):
        self.master = window.Window.get_instance()

        self.frame = DirectFrame(
            frameColor=(0, 0, 0, 0.5),
            frameSize=(-0.95, 0.3, -0.95, 0.95),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(-0.8, 0, 0))

        self.elements_gui = {}
        position_button = 0.825
        c = 0.0

        for element in CategoryItem:
            list_items = DirectScrolledFrame(
                frameColor=(c, 0.0, 0.0, 1.0),
                frameSize=(-0.72, 0.28, -0.93, 0.93),
                hpr=LVecBase3f(0, 0, 0),
                pos=LPoint3f(0, 0, 0),
                parent=self.frame)
            list_items.hide()

            self.elements_gui[element.name] = list_items

            DirectButton(
                frameColor=(c, 0.0, 0.0, 1.0),
                frameSize=(-1.0, 1.0, -1.0, 1.0),
                hpr=LVecBase3f(0, 0, 0),
                pos=LPoint3f(-0.825, 0, position_button),
                scale=LVecBase3f(0.1, 0.1, 0.1),
                command=lambda: self.__change_visible_element(element.name),
                parent=self.frame)

            position_button -= 0.2
            c = 1.0

    def __change_visible_element(self, name):
        print(name)
        for element in CategoryItem:
            self.elements_gui[element.name].hide()
        self.elements_gui[name].show()

    def hide(self):
        self.frame.hide()

    def show(self):
        self.frame.show()
