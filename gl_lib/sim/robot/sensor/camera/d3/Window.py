from pyglet.gl import *
from pyglet.window import key
import pdb
import math
from gl_lib.sim.robot.sensor.camera.d3 import *
from gl_lib.sim.geometry.point import Vecteur
from math import pi, acos
from math import pi
from gl_lib.config import PIX_PAR_M

def projection():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()


def model():
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def push(pos, rot):
    angle=rot.get_angle()*180/pi
    glPushMatrix()
    glRotatef(-90, 1, 0, 0)
    glRotatef(90+angle, 0, 0, 1)
    pos=pos.to_tuple()

    glTranslatef(int(-pos[0]*PIX_PAR_M), int(-pos[1]*PIX_PAR_M), int(-pos[2]*PIX_PAR_M), )


class Window(pyglet.window.Window):

    def set2d(self):
        projection()
        gluOrtho2D(0, self.width, 0, self.height)
        model()

    def set3d(self):
        projection()
        gluPerspective(70, self.width / self.height, 0.05, 800)
        model()

    def setLock(self, state):
        self.lock = state
        self.set_exclusive_mouse(state)

    lock = False
    mouse_lock = property(lambda self: self.lock, setLock)

    def __init__(self, arene=None, camera=None):
        super().__init__(width=1000, height=1000, caption='Robot', resizable=True)
        self.set_minimum_size(300, 200)
        self.keys = key.KeyStateHandler()
        self.push_handlers(self.keys)

        self.model = Model(arene)

        self.camera = camera

    def on_mouse_motion(self, x, y, dx, dy):
        if self.mouse_lock: self.camera.mouse_motion(dx, dy)

    def on_draw(self):
        self.clear()
        self.set3d()

        push(self.camera.centre,
            self.camera.direction)
        self.model.draw()
        glPopMatrix()

        self.camera.picture()