from direct.showbase.DirectObject import DirectObject

import window

SPEED = 40


class Player(DirectObject):

    def __init__(self):
        super().__init__()
        self.master = window.Window.get_instance()

        self.keyMap = {"w": False, "s": False, "a": False, "d": False}
        self.rotation = [0, 0]

        self.camera_model = self.master.loader.loadModel("models/person/person")
        self.camera_model.reparentTo(self.master.render)
        self.camera_model.setPos(0, 15, 100)

        self.master.camera.reparentTo(self.camera_model)
        self.master.camera.setY(self.master.camera, -5)

        self.bind()

        self.master.taskMgr.add(self.cameraControl, "Camera Control")

    def setKey(self, key, value):
        self.keyMap[key] = value

    def cameraControl(self, task):
        dt = globalClock.getDt()
        if (dt > .20):
            return task.cont

        if self.master.mouseWatcherNode.hasMouse() == True:
            mouse_position = self.master.mouseWatcherNode.getMouse()
            self.rotation[0] += mouse_position.getY() * 30
            self.rotation[1] += mouse_position.getX() * -50
            self.master.camera.setP(self.rotation[0])
            self.master.camera.setH(self.rotation[1])

            self.camera_model.setH(self.camera_model.getH() + mouse_position.getX() * -1)

        self.master.win.movePointer(0, int(self.master.win.getXSize() / 2), int(self.master.win.getYSize() / 2))

        if self.keyMap["w"] == True:
            self.camera_model.setY(self.camera_model, SPEED * dt)
        if self.keyMap["s"] == True:
            self.camera_model.setY(self.camera_model, -SPEED * dt)
        if self.keyMap["a"] == True:
            self.camera_model.setX(self.camera_model, -SPEED * dt)
        if self.keyMap["d"] == True:
            self.camera_model.setX(self.camera_model, SPEED * dt)

        return task.cont

    def bind(self):
        self.accept("w", self.setKey, ["w", True])
        self.accept("s", self.setKey, ["s", True])
        self.accept("a", self.setKey, ["a", True])
        self.accept("d", self.setKey, ["d", True])

        self.accept("w-up", self.setKey, ["w", False])
        self.accept("s-up", self.setKey, ["s", False])
        self.accept("a-up", self.setKey, ["a", False])
        self.accept("d-up", self.setKey, ["d", False])
