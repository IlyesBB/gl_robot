from gl_lib.sim.robot.strategy import Strategie
from gl_lib.sim.robot import RobotMotorise, Tete
from gl_lib.sim.robot.sensor import *

import random
import unittest

class StrategyTest(unittest.TestCase):
    def setUp(self):
        self.robot = RobotMotorise()

    def init_test(self):
        s=Strategie(self.robot)
        self.assertIsInstance(s.robot.tete.lcapteurs[Tete.ACC], Accelerometre, None)
        self.assertIsInstance(s.robot.tete.lcapteurs[Tete.CAM], camera.Camera, None)
        self.assertIsInstance(s.robot.tete.lcapteurs[Tete.IR], CapteurIR, None)

