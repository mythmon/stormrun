import math


class Vector(object):
    """
    X/Y and Polar representations of a vector. Each representation is only
    update when it is accessed.
    """
    def __init__(self, x=None, y=None, a=None, m=None):
        # Initialize variables
        self._a = None
        self._m = None
        self._x = None
        self._y = None

        if m is not None or a is not None:
            self._a = a if a else 0
            self._m = m if m else 0

        elif x is not None or y is not None:
            self._x = x if x else 0
            self._y = y if y else 0

        if self._x is None:
            self._x = 0
        if self._y is None:
            self._y = 0
        if self._a is None:
            self._a = 0
        if self._m is None:
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

    def update_polar(self):
        self._a = math.atan2(self._y, self._x)
        self._m = math.sqrt(self._x ** 2 + self._y ** 2)

    def update_xy(self):
        self._x = self._m * math.cos(self._a)
        self._y = self._m * math.sin(self._a)

    @property
    def x(self):
        if self._x is None:
            self.update_xy()
        return self._x

    @x.setter
    def x(self, value):
        self._x = value
        self._a = None
        self._m = None

    @property
    def y(self):
        if self._y is None:
            self.update_xy()
        return self._y

    @y.setter
    def y(self, value):
        self._y = value
        self._a = None
        self._m = None

    @property
    def a(self):
        if self._a is None:
            self.update_polar()
        return self._a

    @a.setter
    def a(self, value):
        self._a = value % (math.pi * 2)
        self._x = None
        self._y = None

    @property
    def m(self):
        if self._m is None:
            self.update_polar()
        return self._m

    @m.setter
    def m(self, value):
        if value < 0:
            value = -value
            self._a = (self.a + math.pi) % (math.pi * 2)
        self._m = value
        self._x = None
        self._y = None
