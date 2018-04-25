# -*- coding: utf-8 -*-
from gl_lib.sim.robot.sensor.camera.d3 import Window
from gl_lib.sim.robot.sensor.camera import Camera
import unittest
from pyglet.gl import *
from time import sleep

class TestWindow(unittest.TestCase):
    def setUp(self):
        self.window=Window(camera=Camera())

    def test_run(self):
        glClearColor(0, 0, 0, 0)
        glEnable(GL_DEPTH_TEST)

        pyglet.app.run()


