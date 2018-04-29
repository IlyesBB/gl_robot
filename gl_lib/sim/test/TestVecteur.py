# -*- coding: utf-8 -*-
from gl_lib.sim.geometry import Vecteur, Point, fonctions
import unittest
import random as rm
from math import *

class TestVecteur(unittest.TestCase):

    def setUp(self):
        self.vector = Vecteur(1,0,0)

    def test_initialisation(self):
        print("Testing initialisation...")
        self.assertIsInstance(self.vector, Vecteur, msg="Error initialisation")
        coords_types_bools = [type(self.vector.x) is int or type(self.vector.x) is float or int,
                              type(self.vector.y) is int or type(self.vector.y) is float or int,
                              type(self.vector.z) is int or type(self.vector.z) is float or int]
        for b in coords_types_bools:
            self.assertEqual(b, True, msg="Error initialisation")
        print("Done")

    def test_to_point(self):
        """
            Teste la conversion en point
        """
        print("Testing to_point...")
        v = self.vector.to_point()
        self.assertIsInstance(v, Point, msg="Error conversion")
        coords_equal = [v.x == self.vector.x, v.y == self.vector.y, v.z == self.vector.z]
        for b in coords_equal:
            self.assertEqual(b, True)
        print("Done")


    def test_rotate(self):
        """
            Tourne un vecteur et vérifie qu'il a tourné du bon angle
        """
        print("Testing rotate...")
        s = [1,-1]
        teta = rm.random()*rm.choice(s)*2*pi
        n=self.vector.get_mag()
        self.vector.rotate(teta)
        err_angle=abs(fonctions.positive_angle(teta)-self.vector.get_angle(signe=1))*180/pi
        err_distance=abs(n-self.vector.get_mag())
        self.assertAlmostEqual(err_distance, 0, msg="Error distance")
        self.assertAlmostEqual(err_angle, 0, msg="Error angle")
        print("Done")


if __name__ == '__main__':
    unittest.main()

