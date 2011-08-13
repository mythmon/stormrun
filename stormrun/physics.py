import math

from stormrun.util import dirty_property

class Vector(object):

    x = dirty_property('_x', lambda self: self._m * math.cos(self._a),
        ['_a', '_m'])
    y = dirty_property('_y', lambda self: self._m * math.sin(self._a),
        ['_a', '_m'])
    a = dirty_property('_a', lambda self: math.atan2(self._y, self._x),
        ['_x', '_y'])
    m = dirty_property('_m',
        lambda self: math.sqrt(self._x ** 2 + self._y ** 2), ['_x', '_y'])

    def __init__(self, x, y):
        self._x = x
        self._y = y
        self._a = None
        self._m = None

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __repr__(self):
        return '<{x}, {y}>'.format(x=self.x, y=self.y)


class PhysicsObject(object):

    def __init__(self, pos, vel=None):
        self.pos = pos
        self.vel = vel if vel else Vector(0, 0)
        self.accel = Vector(0, 0)
        self.effects = []

    def tick(self, t):
        self.vel += self.accel
        self.pos += self.vel

        self.accel = Vector(0, 0)

    def apply_force(self, force=None, x=None, y=None):
        if force:
            self.accel += force
        if x:
            self.accel.x += x
        if y:
            self.accel.y += y
