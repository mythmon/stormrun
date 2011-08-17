import pyglet
from pyglet.gl import *

from stormrun.physics import PhysicsObject

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
