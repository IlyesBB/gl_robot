# -*- coding: utf-8 -*-

from pyglet.gl import *
from math import pi
from gl_lib.sim.robot.sensor.camera.d3 import Model
from gl_lib.config import PIX_PAR_M_3D, PAS_TEMPS
from gl_lib.sim.geometry import *
import pyglet

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
    glTranslatef(-pos[0], -pos[1], -pos[2], )


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
        super().__init__(width=1000, height=800, caption='Robot', resizable=True, visible=True)
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
        self.camera.picture()

    def update(self,dt):
        pass
