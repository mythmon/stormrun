#!/usr/bin/python2
#import sys
#
import pyglet
#from pyglet.gl import *
#from pyglet.window import key
#
#import SDL
#
from stormrun.engine import Engine
from stormrun.physics import Drag
#from stormrun.geometry import Vector
from stormrun.ui import Ship, Starfield
from stormrun.control import KeyboardControls, VarTweaker, JoystickControls
#from stormrun.camera import Camera


class World(object):
    """Handles game logic and all the objects in the various scenes."""

    def __init__(self, engine):

        engine.world = self

        self.ship = Ship(engine, thrust=0.3)
        engine.drawers['foreground'].append(self.ship)
        engine.tickers.append(self.ship)

        # Physics
        Drag(engine, 0.03).apply(self.ship)

        # Controls
        KeyboardControls(engine).apply(self.ship)

        ship_stats = pyglet.text.Label('', font_name='Mono', font_size=10,
                color=(255, 255, 255, 127), x=engine.window.width-10, y=10,
                anchor_x='right', anchor_y='bottom')
        engine.drawers['hud'].append(ship_stats)

    def setup(self):
        """Setup that needs the engine to be set up already."""
        # Joystick controls
        JoystickControls(engine).apply(self.ship)

        # Camera controls
        engine.camera.target = self.ship
        engine.drawers['background'].append(Starfield(engine.camera, density=2))


if __name__ == '__main__':
    engine = Engine(load_joystick=True)
    world = World(engine)
    pyglet.app.run()
