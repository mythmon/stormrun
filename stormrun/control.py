from pyglet.window import key, mouse

import SDL

from stormrun.util import Effect
from stormrun.geometry import Vector

class KeyboardControls(Effect):

    def __init__(self, engine, *args, **kwargs):
        super(KeyboardControls, self).__init__(engine, *args, **kwargs)
        self.key_status = engine.key_status
        self.mouse_status = engine.mouse_status

    @staticmethod
    def tick(self, target, *args, **kwargs):
        f = Vector()

        if self.key_status.get(key.W, False):
            f.y += 1
        if self.key_status.get(key.S, False):
            f.y -= 1
        if self.key_status.get(key.A, False):
            f.x -= 1
        if self.key_status.get(key.D, False):
            f.x += 1

        if f.m > 0:
            target.move_in_dir(f)

        if self.mouse_status.get(mouse.LEFT, False):
            target.fire()

        if 'x' in self.mouse_status and 'y' in self.mouse_status:
            vec = Vector(self.mouse_status['x'], self.mouse_status['y'])
            vec -= self.engine.camera.halfsize
            target.aim_relative(vec)

        self.orig_tick(*args, **kwargs)


class VarTweaker(Effect):

    def __init__(self, key_status, var_str, incr, up_key, down_key):
        self.key_status = key_status
        self.var_str = var_str
        self.incr = incr
        self.up_key = up_key
        self.down_key = down_key

    @staticmethod
    def tick(self, target, *args, **kwargs):
        delta = 0
        if self.key_status.get(self.up_key, False):
            delta += 1
        if self.key_status.get(self.down_key, False):
            delta -= 1

        if delta != 0:
            val = target.__getattribute__(self.var_str)
            val += delta * self.incr
            target.__setattr__(self.var_str, val)
            print "{0}: {1}".format(self.var_str, val)

        self.orig_tick(*args, **kwargs)


class JoystickControls(Effect):

    def __init__(self, engine):
        self.engine = engine
        self.js = SDL.SDL_JoystickOpen(0)

    @staticmethod
    def tick(self, target, *args, **kwargs):
        SDL.SDL_JoystickUpdate()

        # Movement
        x = SDL.SDL_JoystickGetAxis(self.js, 0) / 32768.0
        y = SDL.SDL_JoystickGetAxis(self.js, 1) / 32768.0
        y = -y

        f = Vector(x, y)
        if f.m > 0.1:
            target.move(f)

        # Gun
        x = SDL.SDL_JoystickGetAxis(self.js, 3) / 32768.0
        y = SDL.SDL_JoystickGetAxis(self.js, 4) / 32768.0
        y = -y

        f = Vector(x, y)
        if f.m > 0.5:
            target.aim_in_dir(f)

        trigger = SDL.SDL_JoystickGetAxis(self.js, 5) / 32768.0
        if trigger > 0.5:
            target.fire()

        self.orig_tick(*args, **kwargs)
