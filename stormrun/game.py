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

key_status = {}
mouse_status = {}

ship = Ship(0.3, world, pos=Vector())
world.drawers.append(ship)
world.tickers.append(ship)

joy = JoystickControls()
joy.apply(ship)
kb = KeyboardControls(key_status, mouse_status)
kb.apply(ship)
VarTweaker(key_status, 'thrust', 0.01, up_key=key.I, down_key=key.K).apply(ship)
VarTweaker(key_status, 'time_per_shot', 0.01, up_key=key.U, down_key=key.J).apply(ship)

drag = Drag(0.03)
drag.apply(ship)
VarTweaker(key_status, 'cons', 0.001, up_key=key.O, down_key=key.L).apply(drag)

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
    key_status[symbol] = True

@window.event
def on_key_release(symbol, modifers):
    key_status[symbol] = False

@window.event
def on_mouse_motion(x, y, dx, dy):
    mouse_status['x'] = x
    mouse_status['y'] = y
    p =  Vector(x, y) - camera.halfsize
    ship.aim_relative(p)

@window.event
def on_mouse_press(x, y, button, modifiers):
    mouse_status[button] = True

    print(repr(mouse_status))

@window.event
def on_mouse_release(x, y, button, modifiers):
    mouse_status[button] = False

    print(repr(mouse_status))

@window.event
def on_mouse_drag(x, y, dx, dy, button, modifiers):
    on_mouse_motion(x, y, dx, dy)

pyglet.app.run()
