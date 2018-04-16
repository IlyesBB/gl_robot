from gl_lib.config import PIX_PAR_M
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
        self.obj = Camera()
        self.tete=Tete()
        self.obj2 = Camera(self.tete.centre, self.tete.direction)

    def test_init(self):
        TestCapteur.test_init(self)
        self.assertIsInstance(self.obj, Thread)
        self.assertIsInstance(self.obj, Capteur)

    def test_start(self):
        print(self.obj.direction, self.obj.centre)
        self.obj.start()
        sleep(3)
        self.obj.stop()

    def test_rot_window(self):
        TestCamera.test_start(self)

        self.obj = Camera(Point(1,1,1)*PIX_PAR_M*0.1,Vecteur(1,0,0))
        TestCamera.test_start(self)

        self.obj = Camera(Point(1,1,1), Vecteur(1,0,0).rotate(pi/4))
        TestCamera.test_start(self)

        v=Vecteur(1,1,0).norm()
        for i in range(3):
            self.obj = Camera(((v*i*0.01*PIX_PAR_M).to_point()), v)
            TestCamera.test_start(self)
