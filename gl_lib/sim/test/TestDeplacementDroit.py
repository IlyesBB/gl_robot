import unittest
from gl_lib.sim.robot.strategy.deplacement import DeplacementDroit
from gl_lib.sim.robot import RobotMotorise, Tete
from gl_lib.sim import Simulation
from gl_lib.sim.display.d2.gui import AppAreneThread
from time import sleep
from gl_lib.sim.geometry import Arene, Point, Pave
from gl_lib.config import PAS_TEMPS
from math import pi

class TestDeplacementDroit(unittest.TestCase):
    def setUp(self):
        self.distance = 1
        self.strat=DeplacementDroit(RobotMotorise(Pave(1,1,1,Point(3,3,0))), self.distance)
        self.arene = Arene()
        self.arene.add(self.strat.robot)

    def test_sim_2D(self):
        p=self.strat.robot.centre.clone()
        sim=Simulation(self.strat)
        app=AppAreneThread(self.arene)
        sim.start()
        app.start()
        dps_wheels = self.strat.robot.get_wheels_rotations(3)
        while not sim.stop:
            pass
        app.stop()

        dist = (self.strat.robot.centre-p).to_vect().get_mag()
        self.assertLess(abs(dist-self.distance), abs(dps_wheels[0])*(pi/180)*PAS_TEMPS*self.strat.robot.rd.diametre/2)




