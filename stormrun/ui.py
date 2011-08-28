from datetime import datetime, timedelta
import random
from itertools import izip_longest, repeat

import pyglet
from pyglet.gl import *

from stormrun.physics import PhysicsObject
from stormrun.geometry import Vector
from stormrun import util


class DrawObject(object):
    """An object to be drawn."""

    def __init__(self):
        self.pieces = []

    def draw(self):
        for piece in self.pieces:
            piece.draw()


class DrawPiece(object):
    """A single piece of a DrawObject."""

    def __init__(self, verts=None, vert_type='v2f/static', draw_type=GL_LINE_LOOP,
            color=None, colors=None, color_type='c3f/static'):

        self.draw_type = draw_type

        if not verts:
            verts = []
        verts = util.flatten(verts)
        num_verts = len(verts) // int(vert_type[1])

        if not colors:
            colors = []
        if not color:
            if color_type[:3] == 'c3f':
                color = (1.0, 1.0, 1.0)
            elif color_type[:3] == 'c4f':
                color = (1.0, 1.0, 1.0, 1.0)
            else:
                raise Exception("I don't understand that color format.")

        # any given colors will be used, otherwise use the default
        real_colors = []
        for given, default in izip_longest(colors, repeat(color, num_verts)):
            if given:
                real_colors.append(given)
            else:
                real_colors.append(default)

        real_colors = util.flatten(real_colors)

        self.verts = pyglet.graphics.vertex_list(num_verts,
                (vert_type, verts), (color_type, real_colors))


    def draw(self):
        self.verts.draw(self.draw_type)

class Ship(PhysicsObject):

    def __init__(self, world, thrust=0.3, *args, **kwargs):
        super(Ship, self).__init__(world, *args, **kwargs)

        self.body = DrawPiece([(12, 0), (-6, 7.5), (-3, 0), (-6, -7.5)],
                color=(1, 1, 1, 0.5), color_type='c4f/static')

        self.recticle = DrawPiece([(0, 6), (2, 2), (6, 0), (2, -2),
               (0, -6), (-2, -2), (-6, 0), (-2, 2)],
               color=(1, 0.5, 0.5, 0.5), color_type='c4f/static')

        self.draw_ang = self.vel.a_degrees
        self.thrust = 0.3
        self.aim = Vector(a=0, m=100)
        self.shot_clock = 0
        self.time_per_shot = 0.2

    def draw(self):
        if self.vel.m > 0.1:
            self.draw_ang = self.vel.a_degrees

        glPushMatrix()
        glTranslatef(self.pos.x, self.pos.y, 0)

        # Isolate the ship's rotation from the aim
        glPushMatrix()
        glRotatef(self.draw_ang, 0, 0, 1)
        self.body.draw()
        glPopMatrix()

        glTranslatef(self.aim.x, self.aim.y, 0)
        self.recticle.draw()
        glPopMatrix()

    def tick(self, t, *args, **kwargs):
        super(Ship, self).tick(t, *args, **kwargs)

        if self.shot_clock < t:
            self.shot_clock = 0
        elif self.shot_clock > 0:
            self.shot_clock -= t

    def move_in_dir(self, f):
        f.a
        f.m = self.thrust
        self.apply_force(f)

    def move(self, f):
        f.a
        f.m = f.m * self.thrust
        self.apply_force(f)

    def fire(self):
        if self.shot_clock <= 0:
            v = Vector(a=self.aim.a, m=10)
            l = Laser(self.world, v, pos=self.pos, vel=v+self.vel)
            self.world.drawers['foreground'].append(l)
            self.world.tickers.append(l)
            self.shot_clock = self.time_per_shot

    def aim_in_dir(self, vec):
        self.aim.m = 100
        self.aim.a = vec.a

    def aim_relative(self, vec):
        self.aim = vec


class Laser(PhysicsObject):

    def __init__(self, world, direction, *args, **kwargs):
        super(Laser, self).__init__(world, *args, **kwargs)
        self.vertex_list = pyglet.graphics.vertex_list(2,
            ('v2f/static', (0, 0, 5, 0)),
            ('c4f/static', (0, 1, 0, 0.9, 0, 1, 0, 0.9)))

        self.draw_ang = direction.a_degrees

        self.lifetime = random.random() * 2 + 2

    def tick(self, t, *args, **kwargs):
        super(Laser, self).tick(t, *args, **kwargs)

        self.lifetime -= t
        if self.lifetime <= 0:
            self.world.tickers.remove(self)
            self.world.drawers['foreground'].remove(self)


    def draw(self):
        glPushMatrix()
        glTranslatef(self.pos.x, self.pos.y, 0)
        glRotatef(self.draw_ang, 0, 0, 1)
        self.vertex_list.draw(GL_LINE_LOOP)
        glPopMatrix()


class Starfield(object):

    def __init__(self, camera, density=1.0):
        self.camera = camera

        verts = []
        colors = []
        self.step = int(100/density)

        left = int(-camera.halfsize.x)
        right = int(camera.halfsize.x)
        top = int(camera.halfsize.y)
        bottom = int(-camera.halfsize.y)

        for y in xrange(bottom, top + self.step, self.step):
            for x in xrange(left, right + self.step, self.step):
                verts += [x, y]
                colors += [0.5, 0.5, 0.5]

        self.vertex_list = pyglet.graphics.vertex_list(len(verts) / 2,
            ('v2i/static', verts),
            ('c3f/static', colors))

    def draw(self):
        glPushMatrix()
        trans_p = self.camera.pos

        x = int((trans_p.x // self.step) * self.step)
        y = int((trans_p.y // self.step) * self.step)

        glTranslatef(x, y, 0)
        self.vertex_list.draw(GL_POINTS)
        glPopMatrix()
