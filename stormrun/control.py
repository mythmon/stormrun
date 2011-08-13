from types import MethodType

import pygame

from stormrun.util import Effect

class Controller(Effect):

    def __init__(self, keys):
        super(Effect, self).__init__()
        self.keys = keys

    @staticmethod
    def tick(self, target, t):
        ax, ay = 0, 0

        if self.keys.get(pygame.K_UP, False):
            ay -= 1
        if self.keys.get(pygame.K_DOWN, False):
            ay += 1
        if self.keys.get(pygame.K_LEFT, False):
            ax -= 1
        if self.keys.get(pygame.K_RIGHT, False):
            ax += 1

        target.apply_force(x=ax, y=ay)

        self.orig_tick(t)
