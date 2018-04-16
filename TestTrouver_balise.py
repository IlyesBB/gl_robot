from unittest import TestCase
from gl_lib.sim.robot.strategy.analyse.image import trouver_balise
from gl_lib.sim.robot.sensor.camera import Balise
import imageio as io
import os
import multiprocessing as mp

class TestTrouver_balise(TestCase):
    def setUp(self):
        """
        :return:
        """
        os.chdir("/home/ilyes/2I013/Projet/gl_lib/sim/robot/sensor/")
        self.l = [(255,0, 0, 255), (0,255,0,255), (255,255,0,255), (0,0,255,255)]  # RGYB

    def test_trouver_balise(self):
        p=trouver_balise(self.l, fname='screenshot0.png')

