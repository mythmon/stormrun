from datetime import datetime, timedelta
import random

import pyglet
from pyglet.gl import *

from stormrun.physics import PhysicsObject
from stormrun.geometry import Vector

class Ship(PhysicsObject):

    def __init__(self, world, thrust=0.3, *args, **kwargs):
        super(Ship, self).__init__(world, *args, **kwargs)
        self.body = pyglet.graphics.vertex_list(4,
            ('v2f/static', (12, 0, -6, 7.5, -3, 0, -6, -7.5)),
            ('c4f/static', (1, 1, 1, 0.5,
                            1, 1, 1, 0.5,
                            1, 1, 1, 0.5,
                            1, 1, 1, 0.5)))

        self.recticle = pyglet.graphics.vertex_list(8,
            ('v2f/static', (0,  6,  2,  2,  6, 0,  2, -2,
                            0, -6, -2, -2, -6, 0, -2,  2)),
            ('c4f/static', (1, 0.5, 0.5, 0.5, 1, 0.5, 0.5, 0.5,
                            1, 0.5, 0.5, 0.5, 1, 0.5, 0.5, 0.5,
                            1, 0.5, 0.5, 0.5, 1, 0.5, 0.5, 0.5,
                            1, 0.5, 0.5, 0.5, 1, 0.5, 0.5, 0.5)))

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
        self.body.draw(GL_LINE_LOOP)
        glPopMatrix()

        glTranslatef(self.aim.x, self.aim.y, 0)
        self.recticle.draw(GL_LINE_LOOP)
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
