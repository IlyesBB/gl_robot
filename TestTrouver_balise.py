from unittest import TestCase

from gl_lib.config import PAS_TEMPS
from gl_lib.sim.robot.strategy.analyse.image import trouver_balise
from gl_lib.sim.robot.sensor.camera import Balise
import os
from PIL import Image
from gl_lib.sim.robot.strategy.vision import StrategieVision
from gl_lib.sim import Simulation
from gl_lib.sim.robot import RobotMotorise, RobotTarget
from gl_lib.sim.geometry import *
from math import pi
from time import sleep
from threading import Thread

class TestTrouver_balise(TestCase):
    def setUp(self):
        """
        :return:
        """

        self.l = Balise().colors  # RGYB

        v=Vecteur(1,1,0).norm()
        p0 = Point(1,1,1)
        self.strat = StrategieVision(RobotMotorise(pave=Pave(1,1,1,p0.clone()), direction=v.clone()), AreneFermee(3,3,3))
        self.target = RobotTarget(pave=Pave(1,1,1, p0.clone()+v*2), direction=v.clone())
        self.target.rotate_all_around(self.target.centre, -pi/4)
        self.strat.arene.add(self.target)

    def test_trouver_balise(self):
        os.chdir("/home/ilyes/2I013/Projet/gl_lib/sim/robot/sensor/camera/pictures")
        im = Image.open("screenshot0.png")
        p=trouver_balise(self.l, image=im)
        print(p)



