# -*- coding: utf-8 -*-
import unittest
from unittest import TestCase
from gl_lib.sim.robot import Tete
from gl_lib.sim.geometry import Vecteur, fonctions
from gl_lib.sim.robot.sensor import Accelerometre, CapteurIR
from gl_lib.sim.robot.sensor.camera import Camera
import random

from math import pi


class TestTest(TestCase):
    def setUp(self):
        """
            Crée une tête et lui ajoute 3 capteurs
        """
        self.tete = Tete()
        self.tete.add_sensors({"acc":Accelerometre(self.tete.centre, self.tete.direction),
                                "ir":CapteurIR(self.tete.centre, self.tete.direction),
                                "cam":Camera(self.tete.centre, self.tete.direction)})

    def test_init(self):
        """
            Vérification de la validité de __init__
        """
        self.assertIsInstance(self.tete, Tete)
        self.assertIsInstance(self.tete.dir_robot, Vecteur)
        self.assertIsInstance(self.tete.direction, Vecteur)
        self.assertIsInstance(self.tete.sensors, list)

    def test_rotate(self):
        """
            Teste si les capteurs suivent bien la tête (en position et direction)
        """
        # Rotation d'un angle aléatoire
        angle = random.random() * 2 * pi
        self.tete.rotate(angle)
        self.tete.update()

        # On teste l'égalité des directions pour chaque capteur
        for i in range(len(self.tete.sensors)):
            self.assertEqual(self.tete.direction, self.tete.sensors[i].direction)

        # On vérifie que la tête a le bon angle relatif par rapport à sa direction référence dir_robot
        self.assertEqual(angle, self.tete.dir_robot.diff_angle(self.tete.direction, 1))



    def test_move(self):
        """
            Teste si les capteurs suivent bien la tête (en position et direction)
        """
        # Déplacement d'une distance aléatoire
        d = (random.random()*0.5+0.5)*random.randint(5, 10)
        self.tete.move(Vecteur(1,0,0)*d)
        self.tete.update()

        # On teste l'égalité des centre pour chaque capteur
        for i in range(len(self.tete.sensors)):
            self.assertEqual(self.tete.centre, self.tete.sensors[i].centre)

    def test_attach(self):
        """
            Vérifie que la tête suit bien le centre et la direction à laquelle elle est attachée
        """
        # On part de sa position et sa direction
        direction=self.tete.dir_robot.clone()
        centre = self.tete.centre.clone()

        self.tete.attach(centre, direction)

        # Déplacement et rotation des références
        d = (random.random()*0.5+0.5)*random.randint(5, 10)
        angle = random.random() * 2 * pi
        centre.move(Vecteur(1,0,0)*d)
        direction.rotate(angle)

        self.tete.update()

        # On vérifie que la tête a bien suivi le mouvement
        self.assertEqual(direction, self.tete.direction)
        self.assertEqual(centre, self.tete.centre)

if __name__ == '__main__':
    unittest.main()

