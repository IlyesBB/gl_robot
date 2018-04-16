from unittest import TestCase
from gl_lib.sim.robot.strategy.deplacement import DeplacementDroitAmeliore, DDroitAmelioreVision
from gl_lib.sim.robot import RobotMotorise, Tete
from gl_lib.sim.robot.display.d2.gui import AppAreneThread
from gl_lib.sim.simulation import Simulation
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
        self.strat = DDroitAmelioreVision(RobotMotorise(pave=Pave(1,1,1, c.clone()), direction=v.clone()),dist, self.arene)
        self.p=Pave(0.5,0.5,0.5,c+self.v)
        self.p.rotate(pi)
        self.arene.add(self.p)
        self.arene.add(self.strat.robot)


    def test_detection_3D(self):
        print("Evaluating direct detection with infrared ray simulation...")
        sim = Simulation(self.strat)

        sim.start()
        #self.strat.start()

        while not sim.stop:
            pass
        #self.strat.stop()

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








