from unittest import TestCase
from gl_lib.sim.robot import Tete
from gl_lib.sim.geometry import Vecteur, fonctions
from gl_lib.sim.robot.sensor import Accelerometre, CapteurIR
from gl_lib.sim.robot.sensor.camera import Camera
import random

from math import pi


class TestTest(TestCase):
    def setUp(self):
        self.tete = Tete()
        self.tete.add_sensors(acc=Accelerometre(self.tete.centre, self.tete.direction), ir=CapteurIR(self.tete.centre, self.tete.direction),
                              cam=Camera(self.tete.centre, self.tete.direction))

    def test_init(self):
        self.assertIsInstance(self.tete, Tete)
        self.assertIsInstance(self.tete.dir_robot, Vecteur)
        self.assertIsInstance(self.tete.direction, Vecteur)
        self.assertIsInstance(self.tete.sensors, list)

    def test_rotate(self):
        angle = random.choice([1, -1]) * random.random() * 2 * pi
        angle=fonctions.positive_angle(angle)
        self.tete.rotate(angle)
        self.tete.update()
        print(self.tete.dir_rel.get_angle(), angle)
        print(self.tete.direction, self.tete.sensors[0].direction)

        for i in range(len(self.tete.sensors)):
            self.assertEqual(self.tete.direction, self.tete.sensors[i].direction)

        self.assertEqual(angle, self.tete.dir_robot.diff_angle(self.tete.direction, 1))

