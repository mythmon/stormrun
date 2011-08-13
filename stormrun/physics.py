import math

from stormrun.util import dirty_property, Effect

class Vector(object):

    x = dirty_property('_x', lambda self: self._m * math.cos(self._a),
        ['_a', '_m'])
    y = dirty_property('_y', lambda self: self._m * math.sin(self._a),
        ['_a', '_m'])
    a = dirty_property('_a', lambda self: math.atan2(self._y, self._x),
        ['_x', '_y'], ['m'])
    m = dirty_property('_m',
            lambda self: math.sqrt(self._x ** 2 + self._y ** 2),
            ['_x', '_y'], ['a'])

    @m.setter
    def m(self, value):
        if value < 0:
            value = -value
            self._a += math.pi
        self._m = value
        # update a
        self._a = self.a
        # invalidate x and y
        self._x = None
        self._y = None

    def __init__(self, x=None, y=None, a=None, m=None):
        self._x = None
        self._y = None
        self._m = None
        self._a = None

        if m is not None or a is not None:
            if m is None:
                m = 1
            if a is None:
                a = 0

            if m < 0:
                a += math.pi
                m = -m

            self._a = a
            self._m = m
            # update x and y
            self.x
            self.y

        if x is not None or y is not None:
            if x is None:
                x = 0
            if y is None:
                y = 0
            self._x = x
            self._y = y
            # update a and m
            self.a
            self.m

        if a is None and m is None and x is None and y is None:
            self._x = 0
            self._y = 0
            self._a = 0
            self._m = 0

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        if isinstance(other, Vector):
            return self.x * other.x + self.y * other.y
        else:
            return Vector(a=self.a, m=self.m * other)

    def __repr__(self):
        return '<{x}, {y}>'.format(x=self.x, y=self.y)


class PhysicsObject(object):

    def __init__(self, pos, vel=None):
        self.pos = pos
        self.vel = vel if vel else Vector()
        self.accel = Vector()
        self.effects = []

    def tick(self, t):
        self.vel += self.accel
        self.pos += self.vel

        self.accel = Vector()

    def apply_force(self, force=None, x=None, y=None):
        if force:
            self.accel += force
        if x:
            self.accel.x += x
        if y:
            self.accel.y += y


class Drag(Effect):

    def __init__(self, cons):
        super(Effect, self).__init__()
        self.cons = cons

    @staticmethod
    def tick(self, target, t):
        if target.vel.m > 0:
            drag = Vector(a=target.vel.a)
            drag.m = (-1/2) * (drag.m ** 2) * self.cons

            if drag.m > target.vel.m:
                drag.m = target.vel.m

            target.apply_force(drag)

        self.orig_tick(t)
