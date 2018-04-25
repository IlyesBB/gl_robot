# -*- coding: utf-8 -*-
import unittest
from gl_lib.sim.robot.strategy.deplacement import Tourner
from gl_lib.sim.robot import RobotMotorise
from gl_lib.sim import Simulation
from gl_lib.sim.geometry.fonctions import positive_angle
from time import sleep
import random as rm
from gl_lib.config import PAS_TEMPS
from math import pi
from gl_lib.sim.display.d2.gui import AppAreneThread
from gl_lib.sim.geometry import Arene, Pave, Point


class TestTourner(unittest.TestCase):
    def setUp(self):
        self.angle = rm.random() * rm.choice([-1, 1]) * pi
        self.strat = Tourner(robot=RobotMotorise(Pave(1,1,1,Point(2,2,0))), angle_max=(self.angle * 180 / pi))
        self.arene = Arene()
        self.arene.add(self.strat.robot)

    def test_sim(self):
        print("Initialising rotation of ", self.angle*180/pi, "degres")
        app = AppAreneThread(self.arene)
        s = Simulation([self.strat])
        v = self.strat.robot.direction.clone()
        s.start()
        app.start()
        self.strat.robot.set_wheels_rotation(1, 40)
        self.strat.robot.set_wheels_rotation(2, 60)

        sens = self.strat.sens
        precision = max(self.strat.robot.get_wheels_rotations(1), self.strat.robot.get_wheels_rotations(2)) * (
                    pi / 180) * PAS_TEMPS * (max(self.strat.robot.rd.diametre,
                                                self.strat.robot.rg.diametre) / self.strat.robot.dist_wheels)
        while not s.stop:
            pass
        app.stop()
        if sens > 0:
            angle = abs((2 * pi) - v.diff_angle(self.strat.robot.direction, 1))
        else:
            angle = abs(v.diff_angle(self.strat.robot.direction, 1))

        print("Error: ", abs(abs(self.angle) - angle)*(180/pi), " degres")
        print("Maximal error expected: ", precision*180/pi, "degres")
        self.assertLess(abs(abs(self.angle) - angle), precision)

