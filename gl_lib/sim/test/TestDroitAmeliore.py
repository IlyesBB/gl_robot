# -*- coding: utf-8 -*-
import unittest
from threading import Thread
from unittest import TestCase
from gl_lib.sim.robot.strategy.deplacement import DeplacementDroitAmeliore, DDroitAmelioreVision
from gl_lib.sim.robot import RobotMotorise, Tete
from gl_lib.sim.display.d2.gui import AppAreneThread
from gl_lib.sim import Simulation
from gl_lib.sim.geometry import Arene, Point, Pave, Vecteur
from gl_lib.config import PAS_IR, PAS_TEMPS
from math import pi

class TestDroitAmeliore(TestCase):
    def setUp(self):
        c=Point(2,2,1)
        v=Vecteur(1,0,0)
        dist = 3.0
        self.arene = Arene()
        self.v = v*dist
        self.strat = DeplacementDroitAmeliore(robot=RobotMotorise(pave=Pave(1,1,1, c.clone()), direction=v.clone()),arene=self.arene)
        self.p=Pave(0.5,0.5,0.5,c+self.v)
        #self.p.rotate(-pi/4)
        self.arene.add(self.p)
        self.arene.add(self.strat.robot)


    def test_detection_2D(self):
        print("Evaluating direct detection with infrared ray simulation...")
        td = Thread(target=self.strat.robot.tete.sensors["cam"].run)

        app = AppAreneThread(self.arene)
        sim = Simulation(strategies=[self.strat], final_actions=[app.stop])

        self.strat.init_movement(3,60)

        sim.start()
        #self.strat.start()
        app.start()

        while not sim.stop:
            pass
        #self.strat.robot.tete.sensors["cam"].stop()


        # On s'assure que le pavé est bien entré dans le champ d'alerte
        dist = (self.p.centre-self.strat.robot.centre).to_vect().get_mag()-self.p.length/2
        self.assertLess(dist, self.strat.proximite_max)

        # On s'assure qu'on a détecté la limite avec une assez bonne précision
        print("Object detected at: ", self.strat.last_detected, " meters")
        diff = abs(self.strat.last_detected-dist)
        err_max = max(self.strat.robot.get_wheels_rotations(1)*(pi/180)*self.strat.robot.rd.diametre*PAS_TEMPS,PAS_IR)

        self.assertLess(diff, err_max)

        print("Error: ", diff, " meters")
        print("Maximum error expected: ", err_max, " meters")

if __name__ == '__main__':
    unittest.main()
