# -*- coding: utf-8 -*-
import unittest
from gl_lib.sim.geometry import Objet3D
from gl_lib.sim.geometry import *


class TestObjet3D(unittest.TestCase):
    def setUp(self):
        self.obj=Objet3D()

    def test_init(self):
        pass

    def test_clone(self):
        obj=self.obj.clone()
        self.assertEqual(obj, self.obj)

    def test_eq(self):
        obj=self.obj.clone()
        self.assertEqual(obj.centre, self.obj.centre)

        try:
            obj.centre=self.obj.centre.move(Vecteur(1,0,0))
        except AttributeError:
            obj.centre=Point(0,0,0)
        self.assertNotEqual(obj.centre, self.obj.centre)

if __name__ == '__main__':
    unittest.main()
