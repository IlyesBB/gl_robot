# -*- coding: utf-8 -*-
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
        self.strat=DeplacementDroit(robot=RobotMotorise(forme=Pave(1,1,1,Point(3,3,0))), distance_max=self.distance)
        self.arene = Arene()
        self.arene.add(self.strat.robot)

    def test_sim_2D(self):
        """
            Teste la distance parcourue lors d'un déplacement droit
        """
        p=self.strat.robot.centre.clone()
        sim=Simulation(strategies=[self.strat], tic=2, tic_display=[self.strat.robot.tete.sensors["acc"]])
        app=AppAreneThread(self.arene)
        sim.start()
        app.start()
        dps_wheels = self.strat.robot.get_wheels_rotations(3)

        while not sim.stop:
            pass
        dist = (self.strat.robot.centre-p).to_vect().get_mag()
        # On s'assure qu'on a la précision souhaitée
        self.assertLess(abs(dist-self.distance), abs(dps_wheels[0])*(pi/180)*PAS_TEMPS*self.strat.robot.rd.diametre/2)

    def test_json(self):
        dda = DeplacementDroit(robot=RobotMotorise())
        d = dda.__dict__()
        dda.save("deplacement_droit.json")

        dda2 = DeplacementDroit.load("deplacement_droit.json")


if __name__ == '__main__':
    unittest.main()
