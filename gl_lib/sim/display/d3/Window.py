from pyglet.gl import *
from pyglet.window import key
import math
from gl_lib.sim.display.d3.Model import *
from gl_lib.sim.geometry.point import Vecteur
from math import pi
from gl_lib.sim.robot.sensor import Camera

def projection():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()


def model():
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def push(pos, rot):
    glPushMatrix()
    glRotatef(-rot[0], 1, 0, 0)
    glRotatef(-rot[1], 0, 1, 0)
    glTranslatef(-pos[0], -pos[1], -pos[2], )


class Window(pyglet.window.Window):

    def set2d(self):
        projection()
        gluOrtho2D(0, self.width, 0, self.height)
        model()

    def set3d(self):
        projection()
        gluPerspective(70, self.width / self.height, 0.05, 1000)
        model()

    def setLock(self, state):
        self.lock = state
        self.set_exclusive_mouse(state)

    lock = False
    mouse_lock = property(lambda self: self.lock, setLock)

    def __init__(self, arene=None, camera=None):
        super().__init__(width=1000, height=800, caption='Robot', resizable=True)
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
        push(self.camera.centre.to_tuple(),
             ( (self.camera.direction.diff_angle(Vecteur(1, 0, 0)) * 360 / (2 * pi)),
               (self.camera.direction.diff_angle(Vecteur(0, 1, 0)) * 360 / (2 * pi))))
        self.model.draw()
        glPopMatrix()
