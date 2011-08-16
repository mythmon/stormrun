import pyglet

from stormrun.physics import PhysicsObject

class Box(PhysicsObject):

    def draw(self):
        pyglet.graphics.draw(4, pyglet.gl.GL_POLYGON,
            ('v2f', (self.pos.x - 5, self.pos.y - 5,
                     self.pos.x - 5, self.pos.y + 5,
                     self.pos.x + 5, self.pos.y + 5,
                     self.pos.x + 5, self.pos.y - 5)))
