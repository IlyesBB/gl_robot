# -*- coding: utf-8 -*-
import unittest

import pyglet

from gl_lib.sim.robot import RobotMotorise, RobotTarget
from gl_lib.sim.robot.strategy.deplacement import DeplacementCarre, DeplacementCercle, Tourner, DeplacementDroit
from gl_lib.sim.robot.strategy.deplacement.balise import DroitVersBaliseVision
from gl_lib.sim.robot.strategy.vision import StrategieVision
from gl_lib.sim.robot.sensor.camera import Balise
from gl_lib.sim.geometry import AreneFermee,Pave, Vecteur, Point
from gl_lib.sim import Simulation
from time import sleep
from math import pi
from threading import Thread

class TestDroitVersBalise(unittest.TestCase):
    """
    TODO: S'arranger pour que la direction u capteur ir suive bien celle de la tête
    """
    def setUp(self):
        self.v2 = Vecteur(1,0,0)
        self.p0 = Point(1,1,0.5)
        self.strat = DroitVersBaliseVision(RobotMotorise(forme=Pave(1,1,1,self.p0.clone()), direction=self.v2.clone()), AreneFermee(5,5,5))
        self.target = RobotTarget(forme=Pave(1,1,1, self.p0.clone()+self.v2*3), direction=self.v2.clone())
        self.strat.arene.add(self.target)

    def test_target_straith_trajectory(self):
        self.strat2 = DeplacementDroit(robot=self.target,vitesse= 30, distance_max=2)
        td = Thread(target=self.strat.start_3D)
        sim = Simulation(strategies=[self.strat2, self.strat], tmax=15, tic=3,
                         tic_display=[self.strat],
                         final_actions=[self.strat.stop_3D])

        td.start()
        while not self.strat.robot.tete.sensors["cam"].is_set:
            pass
        sim.start()
        while not sim.stop:
            pass

    def test_target_circle_trajectectory(self):
        self.strat = DroitVersBaliseVision(RobotMotorise(forme=Pave(1,1,1,self.p0.clone()), direction=self.v2.clone()), AreneFermee(10,10,10))
        self.strat2 = DeplacementCercle(robot=self.target,vitesse=30, diametre=3, angle_max=360)
        td = Thread(target=self.strat.start_3D)
        sim = Simulation(strategies=[self.strat2, self.strat], tmax=15, tic=1,tic_display=[self.strat], final_actions=[self.strat.stop_3D])
        td.start()
        while not self.strat.robot.tete.sensors["cam"].is_set:
            pass
        sim.start()
        while not sim.stop:
            pass
        self.assertNotEqual(self.strat.last_detected, None)



if __name__ == '__main__':
    unittest.main()
