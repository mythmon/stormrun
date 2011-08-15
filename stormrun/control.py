from pyglet.window import key

from stormrun.util import Effect
from stormrun.geometry import Vector

class Controller(Effect):

    def __init__(self, keys):
        super(Effect, self).__init__()
        self.keys = keys

    @staticmethod
    def tick(self, target, t):
        f = Vector()

        thrust = 0.5

        if self.keys.get(key.UP, False):
            f.y += thrust
        if self.keys.get(key.DOWN, False):
            f.y -= thrust
        if self.keys.get(key.LEFT, False):
            f.x -= thrust
        if self.keys.get(key.RIGHT, False):
            f.x += thrust

        if f.m > thrust:
            f.m = thrust

        target.apply_force(f)

        self.orig_tick(t)
