from gl_lib.sim.geometry import Vecteur, Point, fonctions
import unittest
import random as rm
from math import *

class TestVecteur(unittest.TestCase):

    def setUp(self):
        self.vector = Vecteur(1,0,0)

    def test_initialisation(self):
        self.assertIsInstance(self.vector, Vecteur, msg=None)
        coords_types_bools = [type(self.vector.x) is int or type(self.vector.x) is float,
                              type(self.vector.y) is int or type(self.vector.y) is float,
                              type(self.vector.z) is int or type(self.vector.z) is float]
        for b in coords_types_bools:
            self.assertEqual(b, True)

    def test_get_mag(self):
        v = self.vector.get_mag()
        self.assertEqual(v, sqrt(pow(self.vector.x, 2) + pow(self.vector.y, 2) + pow(self.vector.z, 2)))

    def test_to_point(self):
        v = self.vector.to_point()
        self.assertIsInstance(v, Point, msg=None)
        coords_equal = [v.x == self.vector.x, v.y == self.vector.y, v.z == self.vector.z]
        for b in coords_equal:
            self.assertEqual(b, True)

    def test_get_diff_angle(self):
        s = [1, -1]
        teta = rm.random()*rm.choice(s)*2*pi
        v=self.vector.clone()
        self.vector.rotate(teta)

        diff = abs(-self.vector.diff_angle(v)-teta)
        if abs(diff-(2*pi)) < 0.001:
            diff = 0

        self.assertLess(diff, 0.001)

    def test_rotate(self):
        s = [-1,1]
        teta = rm.random()*rm.choice(s)*2*pi
        sgn=fonctions.signe(teta)
        n=self.vector.get_mag()
        self.vector.rotate(teta)
        self.assertLess(abs(n-self.vector.get_mag()), 0.001)
        self.assertLess(abs(fonctions.positive_angle(teta)-self.vector.get_angle()), 0.001)

    def test_get_angle(self):
        s = [1, -1]
        teta = rm.random()*2*pi
        v=self.vector.clone()
        self.vector.rotate(teta)
        self.assertEqual(v.diff_angle(self.vector, 1), teta)








