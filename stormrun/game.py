#!/usr/bin/python2
import sys

import pyglet
from pyglet.gl import *
from pyglet.window import key

from stormrun.physics import Drag
from stormrun.geometry import Vector
from stormrun.ui import Ship, Starfield
from stormrun.control import KeyboardControls, VarTweaker, JoystickControls
from stormrun.camera import Camera

class World(object):
    pass

world = World()

world.tickers = []
world.drawers = []

def tick(t):
    for obj in world.tickers:
        obj.tick(t)

window = pyglet.window.Window(1024, 768, style='dialog', vsync=True)

glEnable(GL_BLEND)

# Clear the screen, to prevent junk on frame 1
window.clear()
window.flip()

keys = {}

ship = Ship(world, Vector())
world.drawers.append(ship)
world.tickers.append(ship)

kb = JoystickControls()
kb.apply(ship)
VarTweaker(keys, 'thrust', 0.01, up_key=key.Q, down_key=key.A).apply(kb)

drag = Drag(0.03)
drag.apply(ship)
VarTweaker(keys, 'cons', 0.001, up_key=key.W, down_key=key.S).apply(drag)

camera = Camera(ship, size=Vector(window.width, window.height))
world.tickers.append(camera)
world.drawers.append(Starfield(camera, density=2))

fps_display = pyglet.clock.ClockDisplay()
pyglet.clock.schedule_interval(tick, 1/60.0)

ship_stats = pyglet.text.Label('', font_name='Mono', font_size=10,
        color=(255, 255, 255, 127), x=window.width-10, y=10,
        anchor_x='right', anchor_y='bottom')

@window.event
def on_draw():
    window.clear()

    glPushMatrix()
    camera.focus()

    for obj in world.drawers:
        obj.draw()

    glPopMatrix()

    ship_stats.text = 'Pos: {0:+.1f}, Vel: {1:+.1f}'.format(ship.pos, ship.vel)
    ship_stats.draw()
    fps_display.draw()

@window.event
def on_key_press(symbol, modifers):
    keys[symbol] = True

@window.event
def on_key_release(symbol, modifers):
    keys[symbol] = False

pyglet.app.run()
