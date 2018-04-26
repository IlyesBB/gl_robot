# -*- coding: utf-8 -*-
from gl_lib.sim.geometry import Pave, Point, Vecteur
from math import pi
import unittest
import random


class TestPave(unittest.TestCase):

    def setUp(self):
        self.p = Pave(random.randint(1, 5), random.randint(1, 5), random.randint(1, 5))
        print(self.p)

    def test_initialisation(self):
        self.assertIsInstance(self.p, Pave, msg=None)
        self.assertIsInstance(self.p.length, float, msg=None)
        self.assertIsInstance(self.p.width, float, msg=None)
        self.assertIsInstance(self.p.height, float, msg=None)
        for v in self.p.vertices:
            self.assertIsInstance(v, Point, None)
        self.assertEqual(len(self.p.vertices), 8, None)

    def test_clone(self):
        p = self.p.clone()
        self.assertEqual(p, self.p, None)

    def test_eq(self):
        p = self.p.clone()
        self.assertEqual(p, self.p, None)
        v = Vecteur(random.randint(1, 5) * random.choice([1, -1]),
                    random.randint(1, 5) * random.choice([1, -1]),
                    random.randint(1, 5) * random.choice([1, -1]))
        p = self.p.clone().move(v)
        self.assertNotEqual(p, self.p, None)

    def test_rotate_around(self):
        v = Vecteur(random.randint(0, 5) * random.choice([1, -1]),
                    random.randint(0, 5) * random.choice([1, -1]),
                    random.randint(0, 5) * random.choice([1, -1]))
        teta = random.choice([1, -1]) * random.random() * 2 * pi

        v2 = (self.p.vertices[1] - self.p.vertices[0]).to_vect()
        self.p.rotate_around(self.p.centre + v, teta)
        angle=v2.get_angle() - (self.p.vertices[1] - self.p.vertices[0]).to_vect().get_angle()
        self.assertLess(abs(angle)%pi, 0.001, None)

        p = self.p.clone()
        n_centre = (self.p.centre + v) + (self.p.centre - (self.p.centre + v)).to_vect().rotate(teta)
        v = n_centre - self.p.centre
        self.assertEqual(p.move(v), self.p, None)

    def test_rotate_all_around(self):
        v = Vecteur(random.randint(0, 5) * random.choice([1, -1]),
                    random.randint(0, 5) * random.choice([1, -1]),
                    random.randint(0, 5) * random.choice([1, -1]))
        teta = random.choice([1, -1]) * random.random() * 2 * pi

        v2 = (self.p.vertices[1] - self.p.vertices[0]).to_vect()
        self.p.rotate_all_around(self.p.centre + v, teta)
        angle = v2.get_angle() - (self.p.vertices[1] - self.p.vertices[0]).to_vect().get_angle()
        # On veut une précision au millième
        self.assertLess(abs(abs(angle) % pi - abs(teta) % pi), 0.001, None)
if __name__ == '__main__':
    unittest.main()
