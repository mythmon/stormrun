#!/usr/bin/python2
import sys

import pyglet
from pyglet.gl import *

from stormrun.physics import Drag
from stormrun.geometry import Vector
from stormrun.ui import Box, Starfield
from stormrun.control import Controller
from stormrun.camera import Camera

tickers = []
drawers = []

def tick(t):
    for obj in tickers:
        obj.tick(t)

window = pyglet.window.Window(style='dialog', vsync=True)

glEnable(GL_BLEND)

# Clear the screen, to prevent junk on frame 1
window.clear()
window.flip()

keys = {}

box = Box(Vector())
Controller(keys, 0.3).apply(box)
Drag(0.02).apply(box)
drawers.append(box)
tickers.append(box)

camera = Camera(box)
tickers.append(camera)
drawers.append(Starfield(camera, density=2))

fps_display = pyglet.clock.ClockDisplay()
pyglet.clock.schedule_interval(tick, 1/60.0)

@window.event
def on_draw():
    window.clear()

    glPushMatrix()
    camera.focus()

    for obj in drawers:
        obj.draw()

    glPopMatrix()

    fps_display.draw()

@window.event
def on_key_press(symbol, modifers):
    keys[symbol] = True

@window.event
def on_key_release(symbol, modifers):
    keys[symbol] = False

pyglet.app.run()

