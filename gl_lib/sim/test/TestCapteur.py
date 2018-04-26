# -*- coding: utf-8 -*-
import unittest
import random
from gl_lib.sim.geometry import *
from gl_lib.sim.robot.sensor import Capteur
from .TestObjet3D import TestObjet3D
from gl_lib.sim.robot import Tete
from math import pi

class TestCapteur(TestObjet3D):

    def setUp(self):
        self.obj=Capteur()
        self.tete=Tete()
        self.obj2=Capteur(self.tete.centre, self.tete.direction)

    def test_init(self):
        self.assertIsInstance(self.obj.centre, Point)
        self.assertIsInstance(self.obj.direction, Vecteur)
        self.assertIsInstance(self.obj2.centre, Point)
        self.assertIsInstance(self.obj2.direction, Vecteur)

        self.assertEqual(self.obj2.centre, self.tete.centre)
        self.assertEqual(self.obj2.direction, self.tete.direction)

    def test_clone(self):
        obj=self.obj.clone()
        self.assertEqual(obj.centre, self.obj.centre)
        self.assertEqual(obj.direction, self.obj.direction)

    def test_move(self):
        v = Vecteur(random.randint(1, 5) * random.choice([1, -1]),
                    random.randint(1, 5) * random.choice([1, -1]),
                    random.randint(1, 5) * random.choice([1, -1]))

        obj=self.obj.clone()
        self.obj.move(v)
        self.assertEqual((self.obj.centre-obj.centre).to_vect().get_mag(), v.get_mag())

        obj=self.tete.clone()
        self.tete.move(v)
        self.assertEqual(self.obj2.centre, self.tete.centre)
        self.assertEqual(self.obj2.direction, self.tete.direction)
        self.assertEqual((self.tete.centre-obj.centre).to_vect().get_mag(), v.get_mag())

    def test_rot_tete(self):
        teta=random.random()*2*pi*random.choice([1,-1])
        v=self.obj2.direction.clone()
        self.tete.rotate(teta)
        self.assertEqual(self.tete.direction, self.obj2.direction)

if __name__ == '__main__':
    unittest.main()
