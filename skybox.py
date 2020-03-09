from direct.showbase.DirectObject import DirectObject

import window


class Skybox(DirectObject):
    def __init__(self):
        super().__init__()
        self.master = window.Window.get_instance()
        self.model = self.master.loader.loadModel("models/skybox/skybox")
        self.model.reparentTo(self.master.render)
        self.model.setScale(100)
        self.model.setBin('background', 0)
        self.model.setDepthWrite(0)
        self.model.setTwoSided(True)
