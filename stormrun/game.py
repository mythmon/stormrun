#!/usr/bin/python2

import sys

import pyglet

from stormrun.physics import Vector, Drag
from stormrun.ui import Box
from stormrun.control import Controller

tickers = []
drawers = []

def tick(t):
    for obj in tickers:
        obj.tick(t)

window = pyglet.window.Window(style='dialog')

# Clear the screen, to prevent junk on frame 1
window.clear()
window.flip()

keys = {}

box = Box(Vector(100, 240))
Controller(keys).apply(box)
Drag(0.2).apply(box)

fps_display = pyglet.clock.ClockDisplay()

pyglet.clock.schedule_interval(tick, 1/60.0)

drawers.extend([box, fps_display])
tickers.append(box)

@window.event
def on_draw():
    window.clear()

    for obj in drawers:
        obj.draw()

@window.event
def on_key_press(symbol, modifers):
    keys[symbol] = True

@window.event
def on_key_release(symbol, modifers):
    keys[symbol] = False

pyglet.app.run()

