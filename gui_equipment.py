from direct.gui.DirectLabel import DirectLabel, DirectFrame
from direct.gui.DirectScrolledList import DirectScrolledList

numItemsVisible = 4
itemHeight = 0.11


class Equipment(DirectFrame):

    def __init__(self, items, **kw):
        super().__init__(frameColor=(0, 0, 0, 1), frameSize=(-1, 1, -1, 1), **kw)
        l1 = DirectLabel(text="Test1", text_scale=0.1)
        l2 = DirectLabel(text="Test2", text_scale=0.1)
        l3 = DirectLabel(text="Test3", text_scale=0.1)
        myScrolledList = DirectScrolledList(
            decButton_pos=(0.35, 0, 0.53),
            decButton_text="Dec",
            decButton_text_scale=0.04,
            decButton_borderWidth=(0.005, 0.005),
            incButton_pos=(0.35, 0, -0.02),
            incButton_text="Inc",
            incButton_text_scale=0.04,
            incButton_borderWidth=(0.005, 0.005),
            frameSize=(0.0, 0.7, -0.05, 0.59),
            frameColor=(1, 0, 0, 0.5),
            pos=(-1, 0, 0),
            parent=self,
            numItemsVisible=numItemsVisible,
            forceHeight=itemHeight,
            itemFrame_frameSize=(-0.2, 0.2, -0.37, 0.11),
            itemFrame_pos=(0.35, 0, 0.4),
        )

        myScrolledList.addItem(l1)
        myScrolledList.addItem(l2)
        myScrolledList.addItem(l3)
