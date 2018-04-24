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


class TestStrategieVision(unittest.TestCase):

    def setUp(self):
        v=Vecteur(1,1,0).norm()
        p0 = Point(1,1,1)
        self.strat = TournerVersBalise(RobotMotorise(pave=Pave(1,1,1,p0.clone()), direction=v.clone()), AreneFermee(3,3,3))
        self.target = RobotTarget(pave=Pave(1,1,1, (p0.clone()+v*3+Vecteur(1,0,0)*4)), direction=v.clone())
        self.target.rotate_all_around(self.target.centre, -pi/4)
        self.strat.arene.add(self.target)

    def test_vis(self):
        import threading
        sim = Simulation([self.strat], tic=3, tmax=8, final_actions=[self.strat.stop_3D])

        t_max = 10/PAS_TEMPS
        sens = None
        thd = Thread(target=self.strat.start_3D)
        thd.start()
        while not self.strat.robot.tete.sensors["cam"].is_set:
            pass
        sim.start()



