import unittest
import random
from gl_lib.sim.robot import RobotPhysique, Tete
from .TestRobot import TestRobot
from gl_lib.sim.geometry import Pave, Objet3D, Vecteur, Point
from math import pi
from gl_lib.sim.robot.sensor import CapteurIR, Accelerometre
from gl_lib.sim.robot.sensor.camera import Camera


class TestRobotPhysique(TestRobot):

    def setUp(self):
        self.r = RobotPhysique()

    def test_init(self):
        TestRobot.test_init(self)
        self.assertIsInstance(self.r.tete, Tete)

        self.assertEqual(self.r.tete.dir_robot, self.r.direction)
        self.assertEqual(self.r.tete.centre, self.r.centre)

    def test_move(self):
        v = Vecteur(random.choice([1, -1]) * random.randint(1, 5), random.choice([1, -1]) * random.randint(0, 5),
                    random.choice([1, -1]) * random.randint(1, 5))
        self.r.move(v)
        t=Tete(centre=self.r.tete.clone())
        vect_diff=(t.centre.move(v)-self.r.tete.centre).to_vect()
        self.assertLess(vect_diff.get_mag(), 0.001)

    def test_rotate_tete(self):
        """
        La tête tourne avec le robot, mais le robot ne tourne pas avec la tête
        :return:
        """
        teta=random.random()*2*pi

        self.r.rotate_all_around(self.r.centre, teta)
        self.r.update()
        self.assertLess(abs(self.r.tete.direction.diff_angle(self.r.direction)), 0.001)

        self.r.tete.rotate(teta)
        self.r.update()
        self.assertLess(abs(abs(self.r.tete.direction.diff_angle(self.r.direction))-teta), 0.001)



