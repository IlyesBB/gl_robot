from gl_lib.sim.robot import Roue
import unittest
import random

class TestRoue(unittest.TestCase):
    def setUp(self):
        self.r= Roue()

    def test_init(self):
        r=Roue()
        self.assertEqual(r.angle, 0)

    def test_clone(self):
        r=self.r.clone()
        self.assertEqual(self.r.diametre, r.diametre)
        self.assertEqual(self.r.centre, r.centre)

    def test_turn(self):
        s=random.choice([1,-1, 0])
        a=self.r.angle
        self.r.turn(1)
        self.assertEqual(self.r.angle, a+self.r.vitesseRot*s)

