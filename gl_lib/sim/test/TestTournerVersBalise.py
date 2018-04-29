# -*- coding: utf-8 -*-
import unittest

from gl_lib.config import PAS_TEMPS
from gl_lib.sim.robot.strategy.deplacement.balise import TournerVersBalise
from gl_lib.sim.robot.strategy.vision import StrategieVision
from gl_lib.sim.robot import RobotMotorise, RobotTarget, Tete
from gl_lib.sim import Simulation
from gl_lib.sim.geometry import *
from math import pi
from threading import Thread
import unittest


class TestTournerVersBalise(unittest.TestCase):

    def setUp(self):
        v=Vecteur(1,1,0).norm()
        p0 = Point(1,1,1)
        self.strat = TournerVersBalise(robot=RobotMotorise(forme=Pave(1,1,1,p0.clone()), direction=v.clone()), arene=AreneFermee(3,3,3))
        self.target = RobotTarget(forme=Pave(1,1,1, (p0.clone()+v*3)), direction=v.clone())
        self.strat.robot.rotate_all_around(self.strat.robot.centre, 30*pi/180)
        self.strat.robot.update()
        self.strat.arene.add(self.target)

    def test_vis(self):
        sim = Simulation(strategies=[self.strat], tmax=10, final_actions=[self.strat.stop_3D])

        thd = Thread(target=self.strat.start_3D)
        thd.start()
        while not self.strat.robot.tete.sensors["cam"].is_set:
            pass
        
        sim.start()





if __name__ == '__main__':
    unittest.main()

