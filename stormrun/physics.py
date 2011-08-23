import math

from stormrun.util import Effect
from stormrun.geometry import Vector


class PhysicsObject(object):

    def __init__(self, world, pos=None, vel=None):
        self.world = world
        self.pos = pos if pos else Vector()
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

    min_drag = 0.05
    min_vel = 0.1

    def __init__(self, engine, cons, *args, **kwargs):
        super(Drag, self).__init__(engine, *args, **kwargs)
        self.cons = cons

    @staticmethod
    def tick(self, target, t):
        if target.vel.m > self.min_vel:
            drag = Vector(
                a=target.vel.a + math.pi,
                m = (0.5) * (target.vel.m ** 2) * self.cons)

            if drag.m > target.vel.m:
                drag.m = target.vel.m
            if drag.m < self.min_drag:
                drag.m = self.min_drag

            target.apply_force(drag)
        elif 0 < target.vel.m < self.min_vel:
            target.vel = Vector()

        self.orig_tick(t)

    def __repr__(self):
        return "<Drag on {0}>".format(self.target)
