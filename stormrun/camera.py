from stormrun.geometry import Vector


class Camera(object):

    def __init__(self, target=None, pos=None, size=None):
        self.target = target
        self.pos = target.pos if target else Vector()
        self.halfsize = size/2 if size else Vector(320,240)

    def follow(self, target):
        self.target = target

    def tick(self, t):
        if self.target:
            self.pos = self.target.pos

    def transform(self, p):
        new_p = p + self.halfsize - self.pos
        return new_p

    def hittest(self, p):
        diff = self.pos - p
        return abs(diff.x) < self.halfsize.x and abs(diff.y) < self.halfsize.y

    @property
    def left(self):
        return self.pos.x - self.halfsize.x

    @property
    def right(self):
        return self.pos.x + self.halfsize.x

    @property
    def top(self):
        return self.pos.y - self.halfsize.y

    @property
    def bottom(self):
        return self.pos.y + self.halfsize.y
