# -*- coding: utf-8 -*-
from gl_lib.sim.robot.strategy.vision import StrategieVision
from gl_lib.sim.robot import RobotMotorise, RobotTarget
from gl_lib.sim.geometry import *
from math import pi
import unittest
from threading import Thread
from gl_lib.sim import Simulation
from time import sleep

class TestStrategieVision(unittest.TestCase):

    def setUp(self):
        v=Vecteur(1,1,0).norm()
        p0 = Point(1,1,1)
        self.strat = StrategieVision(RobotMotorise(pave=Pave(1,1,1,p0.clone()), direction=v.clone()), AreneFermee(3,3,3))
        self.target = RobotTarget(pave=Pave(1,1,1, p0.clone()+v*2), direction=v.clone())
        self.target.rotate_all_around(self.target.centre, -pi/4)
        self.strat.arene.add(self.target)

    def test_vis(self):
        td = Thread(target=self.strat.start_3D)
        sim = Simulation(strategies=[self.strat])

        td.start()
        sim.start()

        sleep(15)

        self.strat.stop_3D()

    if __name__ == '__main__':
        unittest.main()

