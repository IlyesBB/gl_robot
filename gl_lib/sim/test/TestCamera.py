
from gl_lib.config import PAS_TEMPS
from gl_lib.sim.robot.sensor.camera import Camera
from gl_lib.sim.robot import Tete
from gl_lib.sim.robot.sensor import Capteur
from .TestCapteur import TestCapteur
from threading import Thread
from time import sleep
from math import pi
from gl_lib.sim.geometry import Vecteur, Point


class TestCamera(TestCapteur):
    def setUp(self):
        self.obj = Camera(Point(1,1,1),Vecteur(1,0,0))
        self.tete=Tete()
        self.obj2 = Camera(self.tete.centre, self.tete.direction)

    def test_init(self):
        self.assertIsInstance(self.obj, Capteur)

    def test_picture(self):
        """
        Prend une photo
        :return:
        """
        self.obj.take_picture()
        while not self.obj.is_set:
            pass
        self.obj.stop()
        self.assertNotEqual(self.obj.get_image(), None)
        self.obj.print_image("sc_perso.png")

    def test_video(self):
        """
        Affiche une arène vide en 3D, effectue quelques rotations
        :return:
        """
        td = Thread(target = self.obj.run)

        n=10
        teta = (pi/2)/10
        td.start()
        while not self.obj.is_set:
            pass
        for i in range(n):
            self.obj.rotate(teta)
            sleep(PAS_TEMPS)

        self.obj.stop()

