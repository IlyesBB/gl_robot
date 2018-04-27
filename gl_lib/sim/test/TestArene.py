# -*- coding: utf-8 -*-
import unittest

from gl_lib.sim.geometry import Arene, Vecteur
from gl_lib.sim.geometry import Polygone3D
from gl_lib.sim.geometry import Objet3D, Point



class testArene(unittest.TestCase):

    def setUp(self):
        self.a = Arene()
        self.n = 3
        self.b = Objet3D()


    def test_creation_arene(self):
        self.assertIsInstance(self.a, Arene, msg=None)
        self.assertIsInstance(self.b, Objet3D, msg=None)
        self.a.empty()
        self.assertEqual(len(self.a.objets3D), 0)


    def test_arene_remplie(self):
        self.assertEqual(len(self.a.objets3D), 0)
        for i in range(0, self.n):
            self.a.add(Objet3D())
        print(self.a)
        self.assertEqual(len(self.a.objets3D), self.n)

    def test_vide_arene(self):
        for i in range(0, self.n):
            self.a.add(Objet3D())
        self.a.empty()
        self.assertEqual(len(self.a.objets3D), 0)

    def test_add_list(self):
        self.a.empty()
        l = [Objet3D(Point(0,0,0)).clone() for i in range(self.n)]
        self.a.add_list(l)

        self.assertEqual(len(l), len(self.a.objets3D))

        for i in range(self.n):
            self.a.objets3D[i].centre.move(Vecteur(1,0,0))

        self.assertNotEqual(l[0], self.a.objets3D[0])

if __name__ == '__main__':
    unittest.main()
