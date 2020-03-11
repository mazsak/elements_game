import json
import sys

from panda3d.core import loadPrcFileData, CollisionHandlerQueue, WindowProperties, CollisionTraverser, \
    CollisionHandlerFloor
from direct.showbase.ShowBase import ShowBase

from bind import Bind
from landscape import Landscape
from options import Options
from player import Player
from skybox import Skybox

loadPrcFileData('', 'window-type none')


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
                self.bind = {}
                self.load_bind()
                self.option = {}
                self.load_option()

                self.cTrav = CollisionTraverser()
                self.collision_handler = CollisionHandlerQueue()
                self.floor_handler = CollisionHandlerFloor()
                self.properties()
                self.setFrameRateMeter(True)
                self.skybox = Skybox()
                self.landscape = Landscape()
                self.player = Player()
                self.cTrav.addCollider(self.landscape.cnode_path, self.collision_handler)
                self.cTrav.addCollider(self.player.cnode_path, self.collision_handler)

                self.floor_handler.setMaxVelocity(14)
                self.floor_handler.addCollider(self.player.cnode_path, self.player.camera_model)
                self.floor_handler.setOffset(10.0)
                self.cTrav.addCollider(self.player.cnode_path, self.floor_handler)

                self.accept(self.bind[Bind.EXIT.value], sys.exit)

                # taskMgr.doMethodLater(.1, self.traverse_task, "tsk_traverse")

        def properties(self):
            self.makeDefaultPipe()
            props = WindowProperties().getDefault()

            props.setTitle("Title placeholder")

            if self.option[Options.FULL.value]:
                props.setSize(self.option[Options.RES.value][Options.X.value],
                              self.option[Options.RES.value][Options.Y.value])
                props.setFullscreen(True)
                loadPrcFileData('', 'fullscreen t')
            else:
                props.setSize(self.option[Options.RES.value][Options.X.value],
                              self.option[Options.RES.value][Options.Y.value])
            props.setCursorHidden(True)

            self.openMainWindow(props)

        def properties_with_mouse(self):
            props = WindowProperties()
            if self.option[Options.FULL.value]:
                props.setSize(self.option[Options.RES.value][Options.X.value],
                              self.option[Options.RES.value][Options.Y.value])
            else:
                props.setSize(self.option[Options.RES.value][Options.X.value] - 100,
                              self.option[Options.RES.value][Options.Y.value] - 100)
            props.setCursorHidden(False)
            self.win.requestProperties(props)

        def traverse_task(self, task=None):
            self.collision_handler.sortEntries()
            for i in range(self.collision_handler.getNumEntries()):
                entry = self.collision_handler.getEntry(i)
                print(entry)

            if task:
                return task.again

        def load_bind(self):
            with open('config/bind.json') as f:
                self.bind = json.load(f)

        def load_option(self):
            with open('config/options.json') as f:
                self.option = json.load(f)
