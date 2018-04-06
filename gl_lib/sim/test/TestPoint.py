from gl_lib.sim.geometry.point import Point
from gl_lib.sim.geometry.point import Vecteur
import unittest

class TestPoint(unittest.TestCase):

    def setUp(self):
        self.a = Point(0, 0, 0)
        self.b = Point(1, 2, 3)

    def test_initialisation(self):
        self.assertIsInstance(self.a, Point, msg=None)
        self.assertEqual(self.a.x, 0)
        self.assertEqual(self.a.y, 0)
        self.assertEqual(self.a.z, 0)

    def test_setPosition(self):
        self.a.set_position(Point(0, 0, 1))
        self.assertEqual(self.a.x, 0)
        self.assertEqual(self.a.y, 0)
        self.assertEqual(self.a.z, 1)

    def test_deplacer(self):
        self.a.move(self.b)
        self.assertEqual(self.a.x, self.b.x)
        self.assertEqual(self.a.y, self.b.y)
        self.assertEqual(self.a.z, self.b.z)

    def test_toVect(self):
        v = self.a.to_vect()
        self.assertIsInstance(v, Vecteur, msg=None)
        self.assertEqual(v.x, self.a.x)
        self.assertEqual(v.y, self.a.y)
        self.assertEqual(v.z, self.a.z)

