from pyglet.window import key

from stormrun.util import Effect
from stormrun.geometry import Vector

class Controller(Effect):

    def __init__(self, keys, thrust=0.3):
        super(Effect, self).__init__()
        self.keys = keys
        self.thrust = thrust

    @staticmethod
    def tick(self, target, t):
        f = Vector()

        if self.keys.get(key.UP, False):
            f.y += self.thrust
        if self.keys.get(key.DOWN, False):
            f.y -= self.thrust
        if self.keys.get(key.LEFT, False):
            f.x -= self.thrust
        if self.keys.get(key.RIGHT, False):
            f.x += self.thrust

        if f.m > self.thrust:
            f.m = self.thrust

        target.apply_force(f)

        self.orig_tick(t)
