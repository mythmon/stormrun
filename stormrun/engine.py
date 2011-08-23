#import sys
#
import pyglet
from pyglet.gl import *
#from pyglet.window import key
#
import SDL
#
#from stormrun.physics import Drag
#from stormrun.geometry import Vector
#from stormrun.ui import Ship, Starfield
#from stormrun.control import KeyboardControls, VarTweaker, JoystickControls
from stormrun.camera import Camera


class Engine(object):
    """
    Handles video, and input. Input is from keyboard, mouse, or joystick, and
    can be both event driver or polled.
    """

    def __init__(self, load_joystick=False):
        self.init = False
        self.load_joystick = load_joystick

        self.tickers = []
        self.drawers = {
            'background': [],
            'foreground': [],
            'hud': [],
            'preload': [],
        }

        self.key_status = {}
        self.mouse_status = {}
        if load_joystick:
            self.joystick_status = {}

        self.window = pyglet.window.Window(1024, 768, vsync=True)
        self.setup_gl()

        # Clear the screen, to prevent junk on the first frame
        self.window.clear()
        self.window.flip()

        for event in [self.on_draw, self.on_key_press, self.on_key_release,
                      self.on_mouse_press, self.on_mouse_release,
                      self.on_mouse_motion, self.on_mouse_drag]:
            self.window.event(event)

        self.drawers['preload'].append(pyglet.text.Label(
            'Loading...', font_name='Mono', font_size=36, color=(255, 255, 255, 127),
            x=self.window.width / 2, y=self.window.height / 2,
            anchor_x='center', anchor_y='center'))

    def setup_gl(self):
        # Enable opacity
        glEnable(GL_BLEND)

    def setup(self):
        """
        Setup that takes more time.  Shows a loading screen, and initializes
        SDL to poll joysticks.  Should be called after pyglet's run_app
        function has been started.
        """
        if self.load_joystick:
            print("Loading SDL")
            SDL.start()
            SDL.SDL_Init(SDL.SDL_INIT_JOYSTICK)
            print("Done loading SDL")

        self.camera = Camera(self)
        self.tickers.append(self.camera)

        self.drawers['hud'].append(pyglet.clock.ClockDisplay())
        pyglet.clock.schedule_interval(self.tick, 1.0/60)

        self.world.setup()
        self.init = True

    def tick(self, t):
        """
        To be called as often as possible, for things like physics calculations
        and control updating. No drawing or other visual interaction.

        :param t: The amount of time in seconds since the last call to tick.
        """
        for obj in self.tickers:
            obj.tick(t)

    def on_draw(self):
        self.window.clear()

        if self.init:
            glPushMatrix()
            self.camera.focus()

            for obj in self.drawers['background']:
                obj.draw()

            for obj in self.drawers['foreground']:
                obj.draw()

            glPopMatrix()

            for obj in self.drawers['hud']:
                obj.draw()

            #ship_stats.text = 'Pos: {0:+.1f}, Vel: {1:+.1f}'.format(ship.pos, ship.vel)
        else:
            for obj in self.drawers['preload']:
                obj.draw()
            self.window.flip()
            self.setup()

    def on_key_press(self, symbol, modifers):
        self.key_status[symbol] = True

    def on_key_release(self, symbol, modifiers):
        self.key_status[symbol] = False

    def on_mouse_press(self, x, y, button, modifers):
        self.mouse_status[button] = True

    def on_mouse_release(self, x, y, button, modifers):
        self.mouse_status[button] = False

    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse_status['x'] = x
        self.mouse_status['y'] = y
        self.mouse_status['dx'] = dx
        self.mouse_status['dy'] = dy

    def on_mouse_drag(self, x, y, dx, dy, button, modifiers):
        self.on_mouse_motion(x, y, dx, dy)

