from direct.showbase.DirectObject import DirectObject
from direct.showbase.ShowBaseGlobal import globalClock
from panda3d.bullet import BulletCapsuleShape, BulletCharacterControllerNode, ZUp
from panda3d.core import BitMask32

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
                       self.master.bind[Bind.UP.value]: False, self.master.bind[Bind.DOWN.value]: False,
                       self.master.bind[Bind.SPACE.value]: False}
        self.equipment = Equipment(self)

        self.rotation = [-70, 140]

        height = 2.5
        radius = 0.4
        character_shape = BulletCapsuleShape(radius, height - 2 * radius, ZUp)
        self.player_node = BulletCharacterControllerNode(character_shape, 0.4, 'Player')
        self.player_node_path = self.master.world_node.attachNewNode(self.player_node)
        self.player_node_path.setPos(90, 31, 395)
        self.player_node_path.setCollideMask(BitMask32.allOn())

        self.master.camera.reparentTo(self.player_node_path)
        self.master.camera.setY(self.master.camera, -5)

        self.camera_model = self.master.loader.loadModel("mesh/models/person/person")
        self.camera_model.reparentTo(self.player_node_path)

        self.bind()

        self.master.taskMgr.add(self.camera_control, "Camera Control")

        self.master.world.attachCharacter(self.player_node_path.node())

    def set_key(self, key, value):
        self.keyMap[key] = value

    def jump(self):
        self.player_node.setMaxJumpHeight(5.0)
        self.player_node.setJumpSpeed(8.0)
        self.player_node.doJump()

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

            self.player_node_path.setH(self.player_node_path.getH() + mouse_position.getX() * -1)

        self.master.win.movePointer(0, int(self.master.win.getXSize() / 2), int(self.master.win.getYSize() / 2))

        if self.keyMap["w"]:
            self.player_node_path.setY(self.player_node_path, SPEED * dt)
        if self.keyMap["s"]:
            self.player_node_path.setY(self.player_node_path, -SPEED * dt)
        if self.keyMap["a"]:
            self.player_node_path.setX(self.player_node_path, -SPEED * dt)
        if self.keyMap["d"]:
            self.player_node_path.setX(self.player_node_path, SPEED * dt)
        if self.keyMap["shift"]:
            self.player_node_path.setZ(self.player_node_path, SPEED * dt)
        if self.keyMap["control"]:
            self.player_node_path.setZ(self.player_node_path, -SPEED * dt)
        if self.keyMap["space"]:
            self.jump()

        return task.cont

    def bind(self):
        self.accept("w", self.set_key, ["w", True])
        self.accept("s", self.set_key, ["s", True])
        self.accept("a", self.set_key, ["a", True])
        self.accept("d", self.set_key, ["d", True])
        self.accept("shift", self.set_key, ["shift", True])
        self.accept("control", self.set_key, ["control", True])
        self.accept("space", self.set_key, ["space", True])
        self.accept("e", self.show_hide_equipment)
        self.accept("f1", self.master.toggle_debug)

        self.accept("w-up", self.set_key, ["w", False])
        self.accept("s-up", self.set_key, ["s", False])
        self.accept("a-up", self.set_key, ["a", False])
        self.accept("d-up", self.set_key, ["d", False])
        self.accept("shift-up", self.set_key, ["shift", False])
        self.accept("control-up", self.set_key, ["control", False])
        self.accept("space-up", self.set_key, ["space", False])

    def show_hide_equipment(self):
        self.equipment.equipment_change_visibility(self)
