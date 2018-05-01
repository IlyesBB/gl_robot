# -*- coding: utf-8 -*-
import os

import numpy
from PIL import Image
from gl_lib.config import PAS_TEMPS
from gl_lib.sim.robot.sensor.camera import Camera
from gl_lib.sim.robot import Tete, RobotMotorise, RobotTarget
from gl_lib.sim.robot.sensor import Capteur
import unittest
from threading import Thread
from time import sleep
from math import pi
from gl_lib.sim.geometry import Vecteur, Point, Pave, Arene


class TestCamera(unittest.TestCase):
    """
        Crée une caméra, teste ses fonctionnalités
    """

    def setUp(self):
        """
            Crée une caméra
        """
        self.obj = Camera(Point(0.2, 0.2, 0.5), Vecteur(1, 0, 0))

    def test_init(self):
        self.assertIsInstance(self.obj, Camera)
        self.assertIsInstance(self.obj.centre, Point)
        self.assertIsInstance(self.obj.direction, Vecteur)

    def test_picture(self):
        """
            Vérifie l'effectivité du système de capture d'écran
        """
        # L'image n'est prise que lorsque la fenêtre est dessinée, quand self.obj.is_set est à True
        print("Testing picture...")
        self.obj.take_picture()
        while not self.obj.is_set:
            pass
        self.obj.stop()

        self.obj.print_image("sc_perso.png")
        os.chdir(self.obj.rep_name)
        im = Image.open("sc_perso.png")
        im.show()
        self.obj.raw_im.show()

        # Vérifie le contenu des pixels un à un
        self.assertEqual(list(im.getdata()), list(self.obj.get_image()))
        os.system('rm sc_perso.png')
        print("Done")

    def test_rotation(self):
        """
            Affiche une arène vide en 3D, effectue quelques rotations
        """
        print("Testing video...")
        td = Thread(target=self.obj.run)

        n = 10
        teta = (pi / 2) / n
        td.start()
        while not self.obj.is_set:
            pass
        for i in range(n):
            self.obj.rotate(teta)
            sleep(PAS_TEMPS)

        self.obj.stop()
        print("Done")

    def test_view(self):
        """
            Affiche une arène vide en 3D, effectue quelques rotations
        """
        print("Testing video...")
        td = Thread(target=self.obj.run)

        p = RobotTarget(forme=Pave(1,1,1, Point(3,3,0.5)))
        a=Arene()
        a.add(p)
        n_rot = 100
        teta = 2*pi/n_rot

        self.obj.direction = (p.centre-self.obj.centre).to_vect().norm()
        td.start()
        while not self.obj.is_set:
            pass
        for i in range(n_rot):
            p.rotate_all_around(p.centre, teta)
            sleep(PAS_TEMPS)

        self.obj.stop()
        print("Done")


    def test_json(self):
        """
            Test de sauvegarder/charger une caméra
        """
        try:
            self.obj.save("camera.json")
            obj2 = Camera.load("camera.json")
            self.assertEqual(self.obj, obj2)
            os.system('rm camera.json')
        except PermissionError:
            pass

if __name__ == '__main__':
    unittest.main()
