# -*- coding: utf-8 -*-
import unittest
from gl_lib.sim.robot import RobotMotorise, RobotTarget
from gl_lib.sim.robot.strategy.deplacement import DeplacementCarre, DeplacementCercle, Tourner
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
        self.strat2 = Tourner(robot=self.target, angle_max= 360, diametre= 1,vitesse= 120)
        self.strat.arene.add(self.target)
        
        def test_vis(self):
            p0=Point(0.5, 2.5, 0.5)
            obs = RobotMotorise(pave=Pave(1,1,1,p0.clone()), direction=(self.target.centre-p0).to_vect())
            strat_obs = StrategieVision(robot=obs, arene=self.strat.arene)

            td = Thread(target=self.strat.start_3D)
            td_obs = Thread(target=strat_obs.start_3D)
            sim = Simulation(strategies=[self.strat2, self.strat], tmax=35, final_actions=[self.strat.stop_3D])


        td.start()
        #td_obs.start()
        while not self.strat.robot.tete.sensors["cam"].is_set and not strat_obs.robot.tete.sensors["cam"].is_set:
            pass
        sim.start()

if __name__ == '__main__':
    unittest.main()
    print(1+2)
