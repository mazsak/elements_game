from direct.showbase.DirectObject import DirectObject
from direct.task import Task
from panda3d.core import GeoMipTerrain, Quat, CollisionHandlerEvent, CollisionNode, CollisionSphere
from panda3d.ode import OdeWorld, OdeBody, OdeMass

import window



class Landscape(DirectObject):

    def __init__(self):
        super().__init__()
        self.master = window.Window.get_instance()

        self.collision = CollisionHandlerEvent()
        self.collision.addInPattern('into-%in')
        self.collision.addOutPattern('outof-%in')

        self.model = self.master.loader.loadModel("models/landscape/landscape")
        self.model.reparentTo(self.master.render)
        self.model.setScale(100)

        self.collCount = 0

        self.world = OdeWorld()
        self.world.setGravity(0, 0, -9.81)
        self.body = OdeBody(self.world)
        M = OdeMass()
        M.setSphere(7874, 1.0)
        self.body.setMass(M)
        self.body.setPosition(self.model.getPos(self.master.render))
        self.body.setQuaternion(self.model.getQuat(self.master.render))

        self.initCollisionSphere(self.model, True)

        self.deltaTimeAccumulator = 0.0
        self.stepSize = 1.0 / 90.0

        # self.master.taskMgr.doMethodLater(1.0, self.simulation, "Physics Simulation")

    def simulation(self, task):
        self.body.setForce(0, min(task.time ** 4 * 500000 - 500000, 0), 0)

        self.deltaTimeAccumulator += globalClock.getDt()
        while self.deltaTimeAccumulator > self.stepSize:
            self.deltaTimeAccumulator -= self.stepSize
            self.world.quickStep(self.stepSize)
        self.model.setPosQuat(self.master.render, self.body.getPosition(), Quat(self.body.getQuaternion()))
        return Task.cont

    def initCollisionSphere(self, obj, show=False):
        # Get the size of the object for the collision sphere.
        bounds = obj.getChild(0).getBounds()
        center = bounds.getCenter()
        radius = bounds.getRadius() * 1.1

        # Create a collision sphere and name it something understandable.
        collSphereStr = 'CollisionHull{0}_{1}'.format(self.collCount, obj.name)
        self.collCount += 1
        cNode = CollisionNode(collSphereStr)
        cNode.addSolid(CollisionSphere(center, radius))

        cNodepath = obj.attachNewNode(cNode)
        if show:
            cNodepath.show()

        # Return a tuple with the collision node and its corrsponding string so
        # that the bitmask can be set.
        return (cNodepath, collSphereStr)