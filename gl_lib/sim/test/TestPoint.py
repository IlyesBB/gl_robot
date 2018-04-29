# -*- coding: utf-8 -*-
from gl_lib.sim.geometry import Point, Vecteur, fonctions
import unittest
import random as rm
from math import pi

class TestPoint(unittest.TestCase):
    def setUp(self):
        self.dot = Point(1,1,0)

    def test_initialisation(self):
        self.assertIsInstance(self.dot, Point, msg="Error initialisation")
        coords_types_bools = [type(self.dot.x) is int or type(self.dot.x) is float,
                              type(self.dot.y) is int or type(self.dot.y) is float,
                              type(self.dot.z) is int or type(self.dot.z) is float]
        for b in coords_types_bools:
            self.assertEqual(b, True, msg="Error initialisation")

    def test_to_vect(self):
        """
            Teste la conversion en vecteur
        """
        print("Testing to_vect...")
        v=self.dot.to_vect()
        coords_equal = [v.x == self.dot.x, v.y == self.dot.y, v.z == self.dot.z]
        for b in coords_equal:
            self.assertEqual(b, True, msg="Error conversion")
        self.assertIsInstance(v, Vecteur, msg="Error conversion")
        print("Done")

    def test_rotate_around(self):
        """
            Teste la rotation
            TODO: Il y à un problème quand la coordonnée z est non nulle
            TODO: Peut être très imprécis dans certains cas, à corriger, ou trouver les cas pathologiques
        """
        print("Testing rotate_around...")
        s=[-1, 1]
        p=Point(rm.choice(s)*rm.randint(2,5), rm.choice(s)*rm.randint(2,5), 0)
        teta=rm.random()*rm.choice(s)*pi
        v=(self.dot-p).to_vect()

        n=v.get_mag()
        aux = (v*100).rotate(teta)
        aux = aux*n/aux.get_mag()+p


        self.dot.rotate_around(p, teta)
        v2 = (aux.to_point()-p).to_vect()

        d_dist = abs(v.get_mag()-v2.get_mag())
        d_angle = v.diff_angle(v2, signe=1)

        self.assertAlmostEqual(d_angle, fonctions.positive_angle(teta), msg="Error angle")
        self.assertAlmostEqual(d_dist, 0, msg="Error distance")
        print("Done")

    def test_json(self):
        print("Testing json format...")
        try:
            self.dot.save("dot.json")
            d2 = Point.load("dot.json")
            self.assertEqual(self.dot, d2)
        except PermissionError:
            print("Permission Error")
        print("Done")

if __name__ == '__main__':
    unittest.main()

