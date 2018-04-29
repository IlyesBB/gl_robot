import unittest
from asyncio import sleep
from unittest import TestCase

from gl_lib.config import PAS_TEMPS
from gl_lib.sim import Simulation
from gl_lib.sim.display.d2.gui import AppAreneThread
from gl_lib.sim.robot import *
from gl_lib.sim.geometry import *
from gl_lib.sim.robot.strategy.deplacement import DeplacementCercle


class TestDroitAmeliore(TestCase):
    def setUp(self):
        r = RobotMotorise(forme=Pave(centre=Point(0, 0, 0), width=1, height=1, length=1))
        r.move(Vecteur(5,5,0))
        self.arene = AreneFermee(3,3,3)
        self.diametre_cercle = 2
        self.strat = DeplacementCercle(robot=r, angle_max=360, diametre=self.diametre_cercle)
        self.arene.add(r)

    def test_simulation(self):
        sim = Simulation(strategies=[self.strat], acceleration_factor=5)


    def test_diametre(self):
        """
            Initialise une trajectoire circulaire, et calcule le diamètre de celle-ci
        """
        print("Testing diametre trajectory...")

        app = AppAreneThread(self.arene)
        sim = Simulation(strategies=[self.strat], acceleration_factor=5)

        min_x, min_y = sim.strategie.robot.centre.x, sim.strategie.robot.centre.y
        max_x, max_y = sim.strategie.robot.centre.x, sim.strategie.robot.centre.y

        sim.start()
        while not sim.stop:
            sleep(PAS_TEMPS/5)
            if sim.strategie.robot.centre.x < min_x:
                min_x = sim.strategie.robot.centre.x
            if sim.strategie.robot.centre.x > max_x:
                max_x = sim.strategie.robot.centre.x
            if sim.strategie.robot.centre.y < min_y:
                min_y = sim.strategie.robot.centre.y
            if sim.strategie.robot.centre.y > max_y:
                max_y = sim.strategie.robot.centre.y
            pass

        self.assertLess((max_y-min_y)-self.diametre_cercle, 0.0001)
        print("Done")


    def test_visualisation_2D(self):
        """
            Visualise le déplacement circulaire en 2D
        """
        print("Testing 2D...")

        app = AppAreneThread(self.arene)
        sim = Simulation(strategies=[self.strat], tic=2, tic_display=[self.strat.robot.tete.sensors["acc"]], final_actions=[app.stop])

        sim.start()
        app.start()


if __name__ == '__main__':
    unittest.main()