from direct.showbase.DirectObject import DirectObject
from direct.showbase.ShowBaseGlobal import globalClock
from panda3d.core import CollisionSphere, CollisionNode, CollisionHandlerQueue, CollisionTraverser, BitMask32, \
    CollisionRay

import window
from bind import Bind
from equipment import Equipment

SPEED = 40


class Player(DirectObject):

    def __init__(self):
        super().__init__()
        self.master = window.Window.get_instance()

        self.keyMap = {self.master.bind[Bind.FWD.value]: False, self.master.bind[Bind.BWD.value]: False,
                       self.master.bind[Bind.RIGHT.value]: False, self.master.bind[Bind.LEFT.value]: False,
                       self.master.bind[Bind.UP.value]: False, self.master.bind[Bind.DOWN.value]: False}
        self.equipment = Equipment(self)

        self.rotation = [0, 0]

        self.camera_model = self.master.loader.loadModel("mesh/models/person/person")
        self.camera_model.reparentTo(self.master.render)
        self.camera_model.setPos(0, 15, 200)

        self.master.camera.reparentTo(self.camera_model)
        self.master.camera.setY(self.master.camera, -5)

        self.bind()

        self.master.taskMgr.add(self.camera_control, "Camera Control")

        self.camera_model.setCollideMask(BitMask32.allOff())
        player_sphere = CollisionRay(0, 0, 0, 0, 0, -1)
        self.cnode_path = self.camera_model.attachNewNode(CollisionNode('cnode'))
        self.cnode_path.node().addSolid(player_sphere)
        self.cnode_path.node().setFromCollideMask(BitMask32.bit(1))
        self.cnode_path.node().setIntoCollideMask(BitMask32.allOff())
        self.cnode_path.show()

    def set_key(self, key, value):
        self.keyMap[key] = value

    def camera_control(self, task):
        dt = globalClock.getDt()
        if dt > .20:
            return task.cont

        if self.master.mouseWatcherNode.hasMouse():
            mouse_position = self.master.mouseWatcherNode.getMouse()
            self.rotation[0] += mouse_position.getY() * 30
            self.rotation[1] += mouse_position.getX() * -50
            self.master.camera.setP(self.rotation[0])
            self.master.camera.setH(self.rotation[1])

            self.camera_model.setH(self.camera_model.getH() + mouse_position.getX() * -1)

        self.master.win.movePointer(0, int(self.master.win.getXSize() / 2), int(self.master.win.getYSize() / 2))

        if self.keyMap["w"]:
            self.camera_model.setY(self.camera_model, SPEED * dt)
        if self.keyMap["s"]:
            self.camera_model.setY(self.camera_model, -SPEED * dt)
        if self.keyMap["a"]:
            self.camera_model.setX(self.camera_model, -SPEED * dt)
        if self.keyMap["d"]:
            self.camera_model.setX(self.camera_model, SPEED * dt)
        if self.keyMap["shift"]:
            self.camera_model.setZ(self.camera_model, SPEED * dt)
        if self.keyMap["control"]:
            self.camera_model.setZ(self.camera_model, -SPEED * dt)

        return task.cont

    def bind(self):
        self.accept("w", self.set_key, ["w", True])
        self.accept("s", self.set_key, ["s", True])
        self.accept("a", self.set_key, ["a", True])
        self.accept("d", self.set_key, ["d", True])
        self.accept("shift", self.set_key, ["shift", True])
        self.accept("control", self.set_key, ["control", True])
        self.accept("e", self.equipment.equipment_change_visibility)

        self.accept("w-up", self.set_key, ["w", False])
        self.accept("s-up", self.set_key, ["s", False])
        self.accept("a-up", self.set_key, ["a", False])
        self.accept("d-up", self.set_key, ["d", False])
        self.accept("shift-up", self.set_key, ["shift", False])
        self.accept("control-up", self.set_key, ["control", False])
