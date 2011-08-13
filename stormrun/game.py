#!/usr/bin/python2

import sys

import pygame
from pygame import Rect, Color

def main():
    pygame.init()
    surface = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()
    keys = {}

    x, y = 320, 240
    vx, vy = 0, 0
    ax, ay = 0, 0

    while True:
        # tick
        ax, ay = 0, 0

        drag

        if keys.get(pygame.K_UP, False):
            ay -= 1
        if keys.get(pygame.K_DOWN, False):
            ay += 1
        if keys.get(pygame.K_LEFT, False):
            ax -= 1
        if keys.get(pygame.K_RIGHT, False):
            ax += 1

        vx, vy = vx + ax, vy + ay
        x, y = x + vx, y + vy

        # Blank the screen
        surface.fill((0,0,0))

        # draw
        pygame.draw.rect(surface, Color(255,0,0), Rect(x, y, 10, 10))

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
