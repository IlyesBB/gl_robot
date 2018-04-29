import os
import unittest
from PIL import Image

from gl_lib.sim.geometry.fonctions import get_project_repository
from gl_lib.sim.robot.strategy.analyse.image import trouver_balise


class TestTrouver_baliser(unittest.TestCase):
    def setUp(self):
        os.chdir(get_project_repository()+"/sim/robot/sensor/camera/d3")
        self.im = Image.open("balise.png")
        self.colors = [(255, 0, 0, 255), (0, 255, 0, 255),  (255,255,0,255), (0,0,255,255)]

    def test_trouver_balise(self):
        p = trouver_balise(self.colors, image=self.im)
        print(p)