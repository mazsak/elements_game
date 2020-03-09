import sys

from direct.showbase.ShowBase import ShowBase, WindowProperties, CollisionTraverser

from landscape import Landscape
from player import Player
from skybox import Skybox


class Window:
    __instance = None

    @staticmethod
    def get_instance():
        if Window.__instance is None:
            Window.__Window()
        return Window.__instance

    class __Window(ShowBase):

        def __init__(self):
            if Window.__instance is None:
                Window.__instance = self
                super().__init__()
                self.cTrav = CollisionTraverser()
                self.properties()
                self.sykbox = Skybox()
                self.landscape = Landscape()
                self.player = Player()

                self.accept('escape', sys.exit)

        def properties(self):
            props = WindowProperties()
            props.setCursorHidden(True)
            props.setFullscreen(1)
            self.win.requestProperties(props)
