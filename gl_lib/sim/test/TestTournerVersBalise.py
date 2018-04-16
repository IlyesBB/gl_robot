import unittest
from gl_lib.sim.robot.strategy.deplacement.balise import TournerVersBalise
from gl_lib.sim.robot.strategy.vision import StrategieVision
from gl_lib.sim.robot import RobotMotorise, RobotTarget
from gl_lib.sim.simulation import Simulation
from gl_lib.sim.geometry import *
from math import pi
from threading import Thread
import unittest


class TestStrategieVision(unittest.TestCase):

    def setUp(self):
        v=Vecteur(1,1,0).norm()
        v2=v.clone()
        p0 = Point(1,1,1)
        self.strat = TournerVersBalise(RobotMotorise(pave=Pave(1,1,1,p0.clone()), direction=v.clone()), AreneFermee(3,3,3))
        self.target = RobotTarget(pave=Pave(1,1,1, p0.clone()+v*2+v2), direction=v.clone())
        self.strat.arene.add(self.target)

    def test_vis(self):

        sim = Simulation(self.strat)
        sim.start()
        self.strat.start_3D()
        sens = None
        while not sim.stop:
            sens = self.strat.sens
            pass
        self.strat.stop_3D()

        self.assertEqual(sens, 0)
