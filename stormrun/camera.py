from pyglet.gl import *

from stormrun.geometry import Vector


class Camera(object):

    def __init__(self, engine, target=None, pos=None):
        self.target = target
        self.pos = target.pos if target else pos if pos else Vector()
        self.halfsize = Vector(engine.window.width / 2, engine.window.height / 2)

    def follow(self, target):
        self.target = target

    def tick(self, t):
        if self.target:
            self.pos = self.target.pos

    def focus(self):
        p = self.halfsize - self.pos
        glTranslatef(p.x, p.y, 0)

    @property
    def size(self):
        return self.halfsize * 2

    @property
    def left(self):
        return self.pos.x - self.halfsize.x

    @property
    def right(self):
        return self.pos.x + self.halfsize.x

    @property
    def top(self):
        return self.pos.y + self.halfsize.y

    @property
    def bottom(self):
        return self.pos.y - self.halfsize.y
