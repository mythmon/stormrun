from types import MethodType

import pygame

from stormrun.util import Effect
from stormrun.physics import Vector

class Controller(Effect):

    def __init__(self, keys):
        super(Effect, self).__init__()
        self.keys = keys

    @staticmethod
    def tick(self, target, t):
        f = Vector()

        if self.keys.get(pygame.K_UP, False):
            f.y -= 1
        if self.keys.get(pygame.K_DOWN, False):
            f.y += 1
        if self.keys.get(pygame.K_LEFT, False):
            f.x -= 1
        if self.keys.get(pygame.K_RIGHT, False):
            f.x += 1

        if f.m > 1:
            f.m = 1

        target.apply_force(f)

        self.orig_tick(t)
