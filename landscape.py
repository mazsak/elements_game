from direct.showbase.DirectObject import DirectObject
from panda3d.core import CollisionNode, BitMask32, CollisionHandlerQueue

import window


class Landscape(DirectObject):

    def __init__(self):
        super().__init__()
        self.master = window.Window.get_instance()

        self.model = self.master.loader.loadModel("models/landscape/landscape")
        self.model.reparentTo(self.master.render)
        self.model.setScale(100)

        self.collCount = 0

        self.model.setCollideMask(BitMask32.allOff())
        heart_collider = self.model.find("**/Grid")
        heart_collider.node().setIntoCollideMask(BitMask32.bit(0))
        self.cnode_path = self.model.attachNewNode(CollisionNode('cnode'))

        self.deltaTimeAccumulator = 0.0
        self.stepSize = 1.0 / 90.0
