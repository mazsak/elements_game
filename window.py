import ctypes
import sys

from direct.showbase.ShowBase import ShowBase, WindowProperties, CollisionTraverser
from direct.task.TaskManagerGlobal import taskMgr

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
                self.skybox = Skybox()
                self.landscape = Landscape()
                self.player = Player()

                self.accept('escape', sys.exit)

                taskMgr.doMethodLater(.05, self.traverse_task, "tsk_traverse")

        def properties(self):
            props = WindowProperties()
            user32 = ctypes.windll.user32
            screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
            props.setSize(screensize)
            props.setCursorHidden(True)
            props.setFullscreen(1)
            self.win.requestProperties(props)

        def traverse_task(self, task=None):
            self.player.collision_handler.sortEntries()
            for i in range(self.player.collision_handler.getNumEntries()):
                entry = self.player.collision_handler.getEntry(i)
                print(entry)

            if task:
                return task.again
