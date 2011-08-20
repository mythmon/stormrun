from pyglet.window import key

from stormrun.util import Effect
from stormrun.geometry import Vector

class KeyboardControls(Effect):

    def __init__(self, keys, thrust=0.3):
        super(Effect, self).__init__()
        self.keys = keys
        self.thrust = thrust

    @staticmethod
    def tick(self, target, *args, **kwargs):
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

        if f.m > 0:
            target.thrust(f)

        if self.keys.get(key.SPACE, False):
            target.fire()

        self.orig_tick(*args, **kwargs)


class VarTweaker(Effect):

    def __init__(self, keys, var_str, incr, up_key, down_key):
        self.keys = keys
        self.var_str = var_str
        self.incr = incr
        self.up_key = up_key
        self.down_key = down_key

    @staticmethod
    def tick(self, target, *args, **kwargs):
        delta = 0
        if self.keys.get(self.up_key, False):
            delta += 1
        if self.keys.get(self.down_key, False):
            delta -= 1

        if delta != 0:
            val = target.__getattribute__(self.var_str)
            val += delta * self.incr
            target.__setattr__(self.var_str, val)
            print "{0}: {1}".format(self.var_str, val)

        self.orig_tick(*args, **kwargs)
