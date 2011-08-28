#!/usr/bin/python2
import pyglet
from pyglet.gl import *

from stormrun.engine import Engine
from stormrun.geometry import Vector


class Editor(object):

    def __init__(self, engine):
        self.engine = engine
        engine.setup_hook.append(self)

    def setup(self):
        self.engine.camera.pos = Vector(self.engine.window.width / 2,
                                        self.engine.window.height / 2)

        Toolbar(self.engine)


class Point(object):
    """A single point on the screen."""

    def __init__(self, engine, pos):
        self.pos = pos
        self.engine = engine

        engine.addDrawer(self, 'hud')
        engine.subscribeMouse(self)

        # the weird .375 stuff makes this pixel perfect (mostly)
        self.outline = pyglet.graphics.vertex_list(4,
            ('v2f/static', (4.375, 4.375, 4.375, -4.375, -4.375, -4.375, -4.375, 4.375)))
        self.center = pyglet.graphics.vertex_list(4,
            ('v2f/static', (2.375, 2.375, 2.375, -2.375, -2.375, -2.375, -2.375, 2.375)))

    def draw(self):
        glPushMatrix()
        glTranslatef(self.pos.x, self.pos.y, 0)
        self.center.draw(GL_POLYGON)
        self.outline.draw(GL_LINE_LOOP)
        glPopMatrix()


class Toolbar(object):

    def __init__(self, engine):
        self.engine = engine
        engine.addDrawer(self, 'hud')
        engine.subscribeMouse(self, ['release'])

        self.size = Vector(engine.window.width, 32)
        self.pos = Vector(0, 0)

        #self.tools = [ToolObjectCursor(engine), ToolHand(engine),
        #              ToolAddPoint(engine), ToolRemovePoint(engine)]
        self.tools = [ToolObjectCursor(), ToolVertexCursor()]

        self.outline = pyglet.graphics.vertex_list(4,
            ('v2f/static', self.size.to('r2f')))

    def on_mouse_release(self, x, y, button, modifiers):
        if 0 <= y <= 32:
            idx = x // 32
            if 0 <= idx < len(self.tools):
                self.activate(idx)

    def draw(self):
        self.outline.draw(GL_LINE_LOOP)

        glPushMatrix()
        for tool in self.tools:
            tool.draw()
            glTranslatef(32, 0, 0)
        glPopMatrix()

    def activate(self, idx):
        """Activate the tool at `idx`, and deactivate others."""
        for i, tool in enumerate(self.tools):
            tool.active = (i == idx)
        self.active_tool = self.tools[idx]


class Tool(object):
    """Base class for a tool in the toolbar."""

    def __init__(self):
        self.size = Vector(32, 32)
        self.outline = pyglet.graphics.vertex_list(4,
            ('v2f/static', self.size.to('r2f')))
        self.highlight = pyglet.graphics.vertex_list_indexed(4,
            [0, 1, 2, 0, 2, 3],
            ('v2f/static', self.size.to('r2f')),
            ('c3f/static', (0.5, 0.5, 0.5, 0.5, 0.5, 0.5,
                            0.5, 0.5, 0.5, 0.5, 0.5, 0.5)))
        self.active = False

    def draw(self):
        if self.active:
            self.highlight.draw(GL_TRIANGLE_STRIP)
        self.outline.draw(GL_LINE_LOOP)

    def drawCursor(self):
        self

class ToolObjectCursor(Tool):
    def __init__(self):
        super(ToolObjectCursor, self).__init__()
        self.icon = pyglet.graphics.vertex_list(4,
            ('v2f/static', (12, 10, 12, 25, 22, 15, 17, 15)))

    def draw(self):
        super(ToolObjectCursor, self).draw()
        self.icon.draw(GL_LINE_LOOP)


class ToolVertexCursor(Tool):
    def __init__(self):
        super(ToolVertexCursor, self).__init__()
        self.icon = pyglet.graphics.vertex_list_indexed(4, [0, 1, 3, 3, 2, 1],
            ('v2f/static', (12, 10, 12, 25, 22, 15, 17, 15)))

    def draw(self):
        super(ToolVertexCursor, self).draw()
        self.icon.draw(GL_TRIANGLE_STRIP)


class ToolHand(object):
    pass


class ToolAddPoint(object):
    pass


class ToolRemovePoint(object):
    pass


if __name__ == '__main__':
    engine = Engine()
    editor = Editor(engine)
    pyglet.app.run()
