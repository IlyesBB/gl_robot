# -*- coding: utf-8 -*-
import unittest
import random
from gl_lib.sim.robot import Robot
from gl_lib.sim.geometry import Pave, Objet3D, Vecteur, Point
from math import pi


class TestRobot(unittest.TestCase):

    def setUp(self):
        self.r = Robot()
        random.seed()

    def test_init(self):
        self.assertIsInstance(self.r, Robot, msg=None)
        self.assertIsInstance(self.r.rd, Objet3D, msg=None)
        self.assertIsInstance(self.r.rg, Objet3D, msg=None)
        self.assertIsInstance(self.r.forme, Pave, msg=None)
        self.assertIsInstance(self.r.direction, Vecteur, msg=None)

        self.assertEqual(self.r.rd.centre, self.r.centre + (self.r.direction.rotate(-pi / 4) * self.r.forme.width / 2))
        self.assertEqual(self.r.rg.centre, self.r.centre + (self.r.direction.rotate(pi / 4) * self.r.forme.width / 2))
        self.assertEqual(self.r.dist_wheels, self.r.forme.width)

    def test_clone(self):
        r=self.r.clone()

        self.assertEqual(r.forme, self.r.forme)
        self.assertEqual(r.centre, self.r.centre)
        self.assertEqual(r.direction, self.r.direction)
        self.assertEqual(r.rd, self.r.rd)
        self.assertEqual(r.rg, self.r.rg)
        self.assertEqual(r.dist_wheels - self.r.dist_wheels, 0.0)

    def test_eq(self):
        r=self.r.clone()
        self.assertEqual(r, self.r)

        r=self.r.clone()
        r.centre = None
        self.assertNotEqual(r, self.r)

        r=self.r.clone()
        r.direction = None
        self.assertNotEqual(r, self.r)

        r=self.r.clone()
        r.rg = None
        self.assertNotEqual(r, self.r)

        r=self.r.clone()
        r.rd = None
        self.assertNotEqual(r, self.r)

        r=self.r.clone()
        r.dist_wheels = None
        self.assertNotEqual(r, self.r)




    def test_move(self):
        v = Vecteur(random.choice([1, -1]) * random.randint(0, 5), random.choice([1, -1]) * random.randint(0, 5),
                    random.choice([1, -1]) * random.randint(0, 5))

        f = self.r.forme.clone()
        c = self.r.centre.clone()
        rg = self.r.rg.clone()
        rd = self.r.rd.clone()

        self.r.move(v)
        rd.move(v)
        rg.move(v)
        f.move(v)
        c.move(v)

        self.assertEqual(self.r.forme, f)
        self.assertEqual(self.r.centre, c)
        self.assertEqual(self.r.rd, rd)
        self.assertEqual(self.r.rg, rg)

    def test_rotate_around(self):
        p = Point(random.choice([1, -1]) * random.randint(0, 5), random.choice([1, -1]) * random.randint(0, 5),
                  random.choice([1, -1]) * random.randint(0, 5)) + self.r.centre
        teta = random.random() * 2 * pi * random.choice([1, -1])

        f = self.r.forme.clone()
        c = self.r.centre.clone()
        rg = self.r.rg.clone()
        rd = self.r.rd.clone()

        self.r.rotate_around(p, teta)
        rd.centre.rotate_around(p, teta)
        rg.centre.rotate_around(p, teta)
        f.centre.rotate_around(p, teta)
        c.rotate_around(p, teta)


        self.assertEqual(self.r.forme.centre, f.centre)
        self.assertEqual(self.r.centre, c)
        self.assertEqual(self.r.rd.centre, rd.centre)
        self.assertEqual(self.r.rg.centre, rg.centre)

    def test_rotate_all_around(self):
        p = Point(random.choice([1, -1]) * random.randint(0, 5), random.choice([1, -1]) * random.randint(0, 5),
                  random.choice([1, -1]) * random.randint(0, 5)) + self.r.centre
        teta = random.random() * 2 * pi * random.choice([1, -1])

        f = self.r.forme.clone()
        c = self.r.centre.clone()
        rg = self.r.rg.clone()
        rd = self.r.rd.clone()
        v = self.r.direction.clone()

        print(v)

        self.r.rotate_all_around(p, teta)
        rd.rotate_around(p, teta)
        rg.rotate_around(p, teta)
        f.rotate_all_around(p, teta)
        c.rotate_around(p, teta)
        v.rotate(teta)

        self.assertEqual(self.r.direction, v)
        self.assertEqual(self.r.forme, f)
        self.assertEqual(self.r.centre, c)
        self.assertEqual(self.r.direction, v)
        self.assertEqual(self.r.rd, rd)
        self.assertEqual(self.r.rg, rg)

if __name__ == '__main__':
    unittest.main()
