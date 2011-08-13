import pygame
from pygame import Rect, Color

from stormrun.physics import PhysicsObject

class Box(PhysicsObject):

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), Rect(self.pos.x, self.pos.y, 10, 10))
