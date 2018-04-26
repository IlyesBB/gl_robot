# -*- coding: utf-8 -*-
from gl_lib.sim.robot.sensor import VueMatriceArene
import unittest
import random
from gl_lib.sim.geometry import Point, Arene, Vecteur, Pave, fonctions
from math import pi
import random

class TestVueMatriceArene(unittest.TestCase):
    """
    Cette classe sert à tester la vue matricielle d'un pavé

    On crée une vue matricielle d'une arène dans une direction aléatoire, à une position aléatoire

    On prend pour les tests des distancees entre 1 et 5 mètres
    """

    def setUp(self):
        self.arene = Arene()
        # Création aléatoire des variables
        l = [random.randint(1,5)*random.choice([1,-1]) for i in range(2)]
        origine = Point(l[0], l[1], 0)
        teta = random.random()*random.choice([1,-1])*2*pi # Angle du vecteur entre l'origine et le pavé
        v=Vecteur(1,0,0).rotate(teta).norm()

        # True est obligatoire pour que test_vue_dessus affiche le pavé au centre
        self.view_mat=VueMatriceArene(self.arene, origine.clone(), v.clone(), True)

    def test_init(self):
        self.assertIsInstance(self.view_mat.origine, Point)
        self.assertIsInstance(self.view_mat.arene, Arene)
        self.assertIsInstance(self.view_mat.ox, Vecteur)
        self.assertIsInstance(self.view_mat.ajuste, bool)

    def test_vue_dessus(self):
        """
        On ajoute à l'arène un pavé de dimensions (1,1,1) dans l'axe Ox de la vue,
        à une distance comprise entre 1 et 5 mètres

        S'assure qu'on a bien une matrice carrée, de la bonne taille
        contenant des entiers, et qu'elle a bien détecté un pavé dans la zone
        """
        teta2 = random.random()*random.choice([1,-1])*2*pi # Angle de rotation du pavé
        self.dist = random.randint(1, 5) # Distance qu'on va mettre entre l'origine et le centre du pavé
        self.p=Pave(1,1,1, self.view_mat.origine+self.view_mat.ox*self.dist)
        self.p.rotate(teta2)
        self.arene.add(self.p)
        print("Evaluatin view of:\n", self.p, "\n")
        dx = self.dist+max(self.p.width, self.p.length) # On s'assure d'englober tout le pavé
        m=self.view_mat.vueDessus(dx)

        self.assertEqual(len(m), int(dx*VueMatriceArene.res))
        if self.view_mat is not None:
            print(self.view_mat)
        for i in range(len(m)):
            for j in range(len(m[0])):
                self.assertIsInstance(m[i][j], int)

        self.assertEqual(len(m), len(m[0]))

if __name__ == '__main__':
    unittest.main()

