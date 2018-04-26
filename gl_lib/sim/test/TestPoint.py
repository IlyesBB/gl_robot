# -*- coding: utf-8 -*-
from gl_lib.sim.geometry import Point, Vecteur
import unittest
import random as rm
from math import pi

class TestPoint(unittest.TestCase):
    def setUp(self):
        self.dot = Point(0,0,0)

    def test_initialisation(self):
        self.assertIsInstance(self.dot, Point, msg=None)
        coords_types_bools = [type(self.dot.x) is int or type(self.dot.x) is float,
                              type(self.dot.y) is int or type(self.dot.y) is float,
                              type(self.dot.z) is int or type(self.dot.z) is float]
        for b in coords_types_bools:
            self.assertEqual(b, True)

    def test_to_vect(self):
        v=self.dot.to_vect()
        coords_equal = [v.x == self.dot.x, v.y == self.dot.y, v.z == self.dot.z]
        for b in coords_equal:
            self.assertEqual(b, True)
        self.assertIsInstance(v, Vecteur)

    def test_eq(self):
        p=self.dot.clone()
        self.assertEqual(p, self.dot)

        p.x=None
        self.assertNotEqual(p, self.dot)

        p=self.dot.clone()
        p.y=None
        self.assertNotEqual(p, self.dot)

        p=self.dot.clone()
        p.z=None
        self.assertNotEqual(p, self.dot)

    def test_rotate_around(self):
        s=[1,-1]
        p=Point(rm.choice(s)*rm.randint(0,5), rm.choice(s)*rm.randint(1,5), rm.choice(s)*rm.randint(0,5))
        teta=rm.random()*rm.choice(s)*2*pi
        v=(self.dot-p).to_vect()
        n=v.get_mag()
        copy=v.clone()
        self.dot.rotate_around(p, teta)
        v.rotate(teta)
        n2=(self.dot-p).to_vect().get_mag()
        print(v, copy, v.diff_angle(copy), teta)
        print(n,n2)

if __name__ == '__main__':
    unittest.main()

