#!/usr/bin/python2

import sys

import pygame
from pygame import Rect, Color

from stormrun.physics import Vector
from stormrun.ui import Box
from stormrun.control import Controller

def main():
    pygame.init()
    surface = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()
    keys = {}

    box = Box(Vector(100, 240), Vector(1, -1))
    Controller(keys).apply(box)

    while True:
        # tick

        box.tick(clock.get_time())

        # Blank the screen
        surface.fill((32,32,32))

        # draw
        box.draw(surface)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                keys[event.key] = True
            elif event.type == pygame.KEYUP:
                keys[event.key] = False

        clock.tick(30)


if __name__ == '__main__':
    main()
