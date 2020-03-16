import json
import sys

from direct.actor.Actor import Vec3
from direct.showbase.ShowBase import ShowBase
from direct.showbase.ShowBaseGlobal import globalClock
from direct.task.TaskManagerGlobal import taskMgr
from panda3d.bullet import BulletWorld, BulletRigidBodyNode, BulletDebugNode, BulletTriangleMesh, \
    BulletTriangleMeshShape
from panda3d.core import loadPrcFileData, WindowProperties, BitMask32

from bind import Bind
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

                self.properties()
                self.setFrameRateMeter(True)
                self.skybox = Skybox()

                self.accept(self.bind[Bind.EXIT.value], sys.exit)

                self.world = BulletWorld()
                self.world_node = None
                self.debug_node_path = None
                self.setup_world()

        def setup_world(self):
            self.world_node = self.render.attachNewNode('World')
            self.world.setGravity(Vec3(0, 0, -9.81))

            # Landscape
            model = self.loader.loadModel("mesh/models/landscape/landscape")
            model.reparentTo(self.render)
            model.setScale(100)
            model.flatten_light()
            geom_nodes = model.findAllMatches('**/+GeomNode')
            geom_node = geom_nodes.getPath(0).node()
            geom_mesh = geom_node.getGeom(0)
            mesh = BulletTriangleMesh()
            mesh.add_geom(geom_mesh)
            ground_shape = BulletTriangleMeshShape(mesh, dynamic=False)

            ground_node = self.world_node.attachNewNode(BulletRigidBodyNode('Ground'))
            ground_node.node().addShape(ground_shape)

            '''
            if self.debug_mode:
                debug_node_path = self.world_node.attachNewNode(BulletDebugNode('Debug'))
                debug_node_path.show()
                debug_node_path.node().showNormals(True)
                self.world.setDebugNode(debug_node_path.node())
            '''
            self.debug_node_path = self.world_node.attachNewNode(BulletDebugNode('Debug'))
            self.debug_node_path.hide()
            self.world.setDebugNode(self.debug_node_path.node())

            ground_node.setPos(0, 0, 0)
            ground_node.setCollideMask(BitMask32.allOn())

            self.world.attachRigidBody(ground_node.node())

            # Character
            player = Player()

            # Other models
            path = 'mesh/models/bullet/pyramid'
            self.add_model(path, pos_x=50, pos_y=15, pos_z=370, scale=5)
            self.add_model(path, pos_x=30, pos_y=15, pos_z=370, scale=5)
            self.add_model(path, pos_x=70, pos_y=15, pos_z=390, scale=5)
            self.add_model(path, pos_x=50, pos_y=40, pos_z=360, scale=5)

            path = 'mesh/models/bullet/ball'
            self.add_model(path, pos_x=0, pos_y=15, pos_z=400, scale=8)
            self.add_model(path, pos_x=30, pos_y=40, pos_z=450, scale=8)

            taskMgr.add(self.update, 'updateWorld')

        def update(self, task):
            dt = globalClock.getDt()
            self.world.doPhysics(dt, 10, 0.008)
            return task.cont

        def toggle_debug(self):
            if self.debug_node_path.isHidden():
                self.debug_node_path.show()
            else:
                self.debug_node_path.hide()

        def add_model(self, path, pos_x, pos_y, pos_z, scale):
            model = self.loader.loadModel(path)
            model.setScale(scale)
            model.flatten_light()

            geom = model.findAllMatches('**/+GeomNode').getPath(0).node().getGeom(0)
            mesh = BulletTriangleMesh()
            mesh.addGeom(geom)
            shape = BulletTriangleMeshShape(mesh, dynamic=True)

            body = BulletRigidBodyNode('Bowl')
            body_node_path = self.world_node.attachNewNode(body)
            body_node_path.node().addShape(shape)
            body_node_path.node().setMass(10.0)
            body_node_path.setPos(pos_x, pos_y, pos_z)
            body_node_path.setCollideMask(BitMask32.allOn())
            self.world.attachRigidBody(body_node_path.node())

            model.reparentTo(body_node_path)

        def properties(self):
            if not self.pipe:
                self.makeDefaultPipe()

            props = WindowProperties()

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
            props.setDefault(props)

            self.openMainWindow(props)

        def change_mouse_visibility(self):
            props = WindowProperties().getDefault()
            if props.getCursorHidden():
                props.setCursorHidden(False)
            else:
                props.setCursorHidden(True)
            props.setDefault(props)
            self.win.requestProperties(props)

        def load_bind(self):
            with open('config/bind.json') as f:
                self.bind = json.load(f)

        def load_option(self):
            with open('config/options.json') as f:
                self.option = json.load(f)
