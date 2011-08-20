import math

from stormrun.util import Effect
from stormrun.geometry import Vector


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

    cutoff = 0.05

    def __init__(self, cons):
        super(Drag, self).__init__()
        self.cons = cons

    @staticmethod
    def tick(self, target, t):
        if target.vel.m > 0:
            drag = Vector(
                a=target.vel.a + math.pi,
                m = (0.5) * (target.vel.m ** 2) * self.cons)

            if drag.m > target.vel.m:
                drag.m = target.vel.m
            if drag.m < self.cutoff:
                drag.m = self.cutoff

            target.apply_force(drag)

        self.orig_tick(t)
