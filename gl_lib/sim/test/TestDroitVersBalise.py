import unittest
from gl_lib.sim.robot import RobotMotorise, RobotTarget
from gl_lib.sim.robot.strategy.deplacement import DeplacementCarre, DeplacementCercle
from gl_lib.sim.robot.strategy.deplacement.balise import DroitVersBaliseVision
from gl_lib.sim.robot.strategy.vision import StrategieVision
from gl_lib.sim.robot.sensor.camera import Balise
from gl_lib.sim.geometry import AreneFermee,Pave, Vecteur, Point
from gl_lib.sim import Simulation
from time import sleep
from math import pi
from threading import Thread

class TestDroitVersBalise(unittest.TestCase):
    def setUp(self):
        v=Vecteur(1,1,0).norm()
        p0 = Point(1,1,1)
        self.strat = DroitVersBaliseVision(RobotMotorise(pave=Pave(1,1,1,p0.clone()), direction=v.clone()), AreneFermee(3,3,3))
        self.target = RobotTarget(pave=Pave(1,1,1, p0.clone()+v*3), direction=Vecteur(1,0,0))
        self.strat2 = DeplacementCercle(self.target, 360, 1)
        self.strat.arene.add(self.target)

    def test_vis(self):
        td = Thread(target=self.strat.start_3D)
        sim = Simulation([self.strat, self.strat2])

        sim.start()
        td.start()
        sim.join()
        td.join()
        while not sim.stop:
            pass
        self.strat.stop_3D()
