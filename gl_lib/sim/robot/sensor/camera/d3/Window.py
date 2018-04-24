from PIL import Image

from pyglet.gl import *
from pyglet.window import key
from math import pi
from gl_lib.sim.robot.sensor.camera.d3 import Model
from gl_lib.config import PIX_PAR_M, PAS_TEMPS
from gl_lib.sim.geometry import *

def projection():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()


def model():
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def push(pos, rot):
    angle=rot.diff_angle(Vecteur(-1,0,0))*180/pi
    glPushMatrix()
    glRotatef(-90, 0, 1, 0)
    glRotatef(-90, 1, 0, 0)
    glRotatef(angle, 0, 0, 1)
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


    def __init__(self, arene=None, camera=None):
        config = Config(double_buffer=True)
        super().__init__(width=1000, height=800, caption='Robot', resizable=True, visible=True,config=config)
        self.set_minimum_size(300,200)
        self.model = Model(arene)
        self.camera = camera
        if arene is None:
            self.model = Model(self.camera.arene)
        pyglet.clock.schedule_interval(self.update, PAS_TEMPS/2)

    def on_draw(self):
        self.clear()
        self.set3d()

        push(self.camera.centre, self.camera.direction)
        self.model.draw()
        glPopMatrix()

    def update(self,dt):
        self.camera.picture()

