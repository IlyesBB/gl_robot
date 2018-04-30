# -*- coding: utf-8 -*-
import random
import unittest

from gl_lib.sim.geometry import *
from gl_lib.sim.robot.sensor import CapteurIR, Capteur
from gl_lib.sim.geometry import Arene
from gl_lib.sim.robot import Tete
from gl_lib.sim.robot.sensor import VueMatriceArene
from gl_lib.config import PAS_IR, RES_M
from math import pi

class TestCapteurIR(unittest.TestCase):

    def setUp(self):
        self.obj = CapteurIR(Point(0,0,0), Vecteur(1,1,0).norm())
        self.tete = Tete()
        self.arene = Arene()

    def test_init(self):
        bool_type = type(self.obj.portee) is float or type(self.obj.portee) is int
        self.assertEqual(bool_type, True, msg="Error initialisation")
        self.assertIsInstance(self.obj, CapteurIR, msg="Error initialisation")
        self.assertIsInstance(self.obj, Capteur, msg="Error initialisation")

    def test_get_mesure(self):
        """
            On met un pavé dans la direction du capteur
            On prends une mesure, on vérifie qu'elle a été réalisée
        """
        print("Testing detection...")

        # Mesure dans arène vide
        res = self.obj.get_mesure(self.arene)
        self.assertEqual(res, -1)


        # Mesure arène avec pavé
        v=Vecteur(1,0,0).norm()
        self.obj.direction, self.obj.centre = v.clone(), Point(0,0,0)
        v2=v*2
        p=Pave(1,1,1, self.obj.centre+v2)
        self.arene.add(p)
        res = self.obj.get_mesure(self.arene)

        # Résultat du bon type
        bool_type = type(res) is float or type(res) is int
        self.assertEqual(bool_type, True)

        # Distance caluclée avec bonne précision
        diff=abs(v2.get_mag()-p.length/2-res)
        self.assertLess(diff, max(PAS_IR, 1/RES_M), msg="Precision error")
        print("Done")

    def test_json(self):
        print("Testing json")
        try:
            self.obj.save("capteur_ir.json")
            obj2 = CapteurIR.load("capteur_ir.json")
            self.assertEqual(self.obj, obj2)
        except PermissionError:
            print("PerimissionError")
        print("Done")

if __name__ == '__main__':
    unittest.main()
