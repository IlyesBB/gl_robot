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
        v2 = Vecteur(1,0,0)
        p0 = Point(0.5,0.5,0.6)
        self.strat = DroitVersBaliseVision(RobotMotorise(pave=Pave(1,1,1,p0.clone()), direction=v2.clone()), AreneFermee(3,3,3))
        self.target = RobotTarget(pave=Pave(1,1,1, p0.clone()+v2*3), direction=v2.clone())
        self.strat2 = DeplacementCercle(self.target, 360, 1)
        self.strat.arene.add(self.target)

    def test_vis(self):
        td = Thread(target=self.strat.start_3D)
        sim = Simulation([self.strat, self.strat2], tmax=10, final_actions=[self.strat.stop_3D])

        td.start()
        while not self.strat.robot.tete.sensors["cam"].is_set:
            pass
        sim.start()

