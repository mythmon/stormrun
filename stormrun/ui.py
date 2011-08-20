import pyglet
from pyglet.gl import *

from stormrun.physics import PhysicsObject
from stormrun.geometry import Vector

class Box(PhysicsObject):

    def __init__(self, *args, **kwargs):
        super(Box, self).__init__(*args, **kwargs)
        self.vertex_list = pyglet.graphics.vertex_list(4,
            ('v2i/static', (-5, -5, -5, +5, +5, +5, +5, -5)),
            ('c4f/static', (0, 1, 0, 0.5,
                            0, 1, 0, 0.5,
                            0, 1, 0, 0.5,
                            0, 1, 0, 0.5)))

    def draw(self):
        glPushMatrix()
        glTranslatef(self.pos.x, self.pos.y, 0)
        self.vertex_list.draw(GL_POLYGON)
        glPopMatrix()


class Starfield(object):

    def __init__(self, camera, density=1.0):
        self.camera = camera

        verts = []
        colors = []
        self.step = int(100/density)

        left = int(-camera.halfsize.x)
        right = int(camera.halfsize.x)
        top = int(camera.halfsize.y)
        bottom = int(-camera.halfsize.y)

        for y in xrange(bottom, top + self.step, self.step):
            for x in xrange(left, right + self.step, self.step):
                verts += [x, y]
                colors += [0.5, 0.5, 0.5]

        self.vertex_list = pyglet.graphics.vertex_list(len(verts) / 2,
            ('v2i/static', verts),
            ('c3f/static', colors))

    def draw(self):
        glPushMatrix()
        trans_p = self.camera.pos

        x = int((trans_p.x // self.step) * self.step)
        y = int((trans_p.y // self.step) * self.step)

        glTranslatef(x, y, 0)
        self.vertex_list.draw(GL_POINTS)
        glPopMatrix()
