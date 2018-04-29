# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, "/Users/Macbook pro/PycharmProjects/GurrenLagann-dev")

from pyglet.gl import *
from pyglet.window import key
import math
from gl_lib.sim.display.d3.Camera import *
from gl_lib.sim.display.d3.Model import *
from gl_lib.sim.display.d3.Window import *
from gl_lib.sim.geometry.Pave import *
from gl_lib.sim.geometry.Arene import *


#if __name__ == '__main__':
window = Window(width=1000,height=800,caption='Robot',resizable=True, capteur=None)
glClearColor(0,0,0,0)
glEnable(GL_DEPTH_TEST)
#glEnable(GL_CULL_FACE)
pyglet.app.run()


