# -*- coding: utf-8 -*-
import random
from gl_lib.sim.geometry import *
from gl_lib.sim.robot.sensor import CapteurIR
from .TestCapteur import TestCapteur
from gl_lib.sim.geometry import Arene
from gl_lib.sim.robot import Tete
from gl_lib.sim.robot.sensor import VueMatriceArene
from gl_lib.config import PAS_IR, RES_M
from math import pi

class TestCapteurIR(TestCapteur):

    def setUp(self):
        self.obj = CapteurIR(Point(0,0,0), Vecteur(1,1,0).norm())
        self.tete = Tete()
        self.obj2 = CapteurIR(self.tete.centre, self.tete.direction)
        self.arene = Arene()

    def test_init(self):
        TestCapteur.test_init(self)
        bool_type = type(self.obj.portee) is float or type(self.obj.portee) is int
        bool_type2 = type(self.obj2.portee) is float or type(self.obj2.portee) is int
        self.assertEqual(bool_type, True)
        self.assertEqual(bool_type2, True)

    def test_get_mesure(self):
        """
        On met un pavé dans la direction du capteur
        On prends une mesure, on vérifie qu'elle a été réalisée
        :return:
        """
        res = self.obj.get_mesure(self.arene)
        bool_type = type(res) is float or type(res) is int
        self.assertEqual(bool_type, True)

        # Vérifie qu'on détecte bien un pavé droit devant
        v=Vecteur(1,0,0).norm()
        self.obj.direction, self.obj.centre = v.clone(), Point(0,0,0)
        v2=v*2
        p=Pave(1,1,1, self.obj.centre+v2)
        p.rotate(pi)
        self.arene.add(p)
        res = self.obj.get_mesure(self.arene)
        # Résultat du bon type
        bool_type = type(res) is float or type(res) is int
        self.assertEqual(bool_type, True)
        # Distance caluclée avec bonne précision
        self.assertLess(abs((v2.get_mag()-p.length/2)-res), max(PAS_IR, 1/RES_M))
        diff=abs(v2.get_mag()-p.length/2-res)
        self.obj.print_last_view()
        print("Evaluated distance: ", res, " meters")
        print("Error: ", diff, " meters")
        print("Maximum error expected: ", max(PAS_IR, 1/RES_M), " meters")

    def test_clone(self):
        obj = self.obj.clone()
        self.assertEqual(obj.centre, self.obj.centre)
        self.assertEqual(obj.direction, self.obj.direction)
        self.assertEqual(obj.portee, self.obj.portee)

    def test_eq(self):
        obj = self.obj.clone()
        self.assertEqual(obj, self.obj)

        obj.direction = None
        self.assertNotEqual(obj, self.obj)

        obj = self.obj.clone()
        obj.centre = None
        self.assertNotEqual(obj, self.obj)

        obj = self.obj.clone()
        obj.portee = None
        self.assertNotEqual(obj, self.obj)







