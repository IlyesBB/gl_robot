# -*- coding: utf-8 -*-
import json
from collections import OrderedDict

from gl_lib.sim.robot.sensor import Capteur
from pyglet.gl import *
from threading import Thread, RLock, Event
from gl_lib.sim.robot.sensor.camera.d3 import *
from gl_lib.sim.geometry import *
from gl_lib.sim.geometry import fonctions
from gl_lib.config import REPNAME_SCREENSHOTS, FILENAME_SCREENSHOT, FORMAT_SCREENSHOT
import multiprocessing as mp
import os
from PIL import Image
import shutil


class Camera(Capteur):
    """
        Permet de visualiser une arène en 3D dans une application pyglet, de récupérer des images sous forme de bytes
        ou de capture d'écran
    """
    # Angle de vue de la caméra en y, en degrés
    ANGLE_VY = 180

    def __init__(self, centre=Point(0, 0, 0), direction=Vecteur(1, 0, 0), get_pic: bool = False,
                 is_running: bool = False, is_set: bool = False, cpt: int = 1):
        """
            Initialise les attributs de la caméra, et le répetoire de sauvegarde des captures d'écran
        :param centre: Centre de la caméra, peut être attaché à une tête
        :param direction: Direction de la caméra, même remarque
        """
        Capteur.__init__(self, centre=centre, direction=direction)
        # arene doit être réinitialisé en dehors de la classe
        self.arene = AreneFermee()
        self.window = None  # Window (gl_lib.sim.robot.sensor.camera.d3.Window)
        self.raw_im = None  # Image

        self.is_set, self.is_running = is_set, is_running
        self.get_pic = get_pic
        self.cpt = cpt
        self.rep_name = fonctions.get_project_repository() + REPNAME_SCREENSHOTS

    def __dict__(self):
        dct = OrderedDict()
        dct["__class__"] = Camera.__name__
        dct["centre"] = self.centre.__dict__()
        dct["direction"] = self.direction.__dict__()

        dct["is_set"] = self.is_set
        dct["is_running"] = self.is_running
        dct["get_pic"] = self.get_pic
        dct["cpt"] = self.cpt

        return dct

    def __str__(self):
        s = "{}; is_running: {}; cpt: {}".format(self.__class__.__name__, self.is_running, self.cpt)
        return s

    def run(self):
        """
            Lance l'application pyglet

            La couleur de fond par défaut est le gris
        """
        self.is_running = True
        self.window = Window(self.arene, self)
        glClearColor(190, 190, 190, 0)
        glEnable(GL_DEPTH_TEST)
        try:
            pyglet.app.run()
        except RuntimeError:
            pass
        except pyglet.gl.lib.GLException:
            pass

    def picture(self):
        """
            Récupère l'image actuelle de l'application, si l'appareil a été "enclenché" avec take_picture()

            Cette méthode est appelée à la fin de la mathode on_draw de la fenêtre
        """
        if self.get_pic:
            # print("Acquiring image...")
            image = pyglet.image.get_buffer_manager().get_color_buffer().get_image_data()
            self.raw_im = Image.frombytes(image.format, (image.width, image.height), image.data)
            # L'image récupérée est alternée...
            self.raw_im = self.raw_im.rotate(180)
            self.raw_im = self.raw_im.transpose(Image.FLIP_LEFT_RIGHT)
            # self.print_image("screenshot"+str(self.cpt)+".png")
            self.get_pic = False
            # print("Picture ", self.cpt, " taken")
            self.cpt += 1
        self.is_set = True

    def print_image(self, fname):
        """
            Sauvegarde la dernière image enregistrée dans le fichier de nom fname

        :param fname: Nom du fichier

        """
        os.chdir("/")
        # print("Printing image...")
        s = self.rep_name + fname
        try:
            self.raw_im.save(s)
        except AttributeError:
            pass

    def get_image(self):
        """
            Récuprère la dernière image enregistrée

        :return: PIL.Image

        """
        try:
            return self.raw_im.getdata()
        except AttributeError:
            # Au cas où aucune image n'a été enregistrée
            pass

    def take_picture(self):
        """
            Si aucune application n'a été lancée avant l'appel de cette fontion, une application est lancée
        """
        self.get_pic = True
        if not self.is_running and not self.is_set:
            td = Thread(target=self.run)
            td.start()

    def stop(self):
        """
            Ferme la fenêtre
        """
        pyglet.app.exit()
        try:
            self.window.close()
        except TypeError:
            # Au cas où self.window = None
            pass
        self.is_set = False

    @staticmethod
    def hook(dct):
        if dct["__class__"] == Vecteur.__name__:
            return Vecteur.hook(dct)
        if dct["__class__"] == Point.__name__:
            return Point.hook(dct)
        if dct["__class__"] == Camera.__name__:
            return Camera(dct["centre"], dct["direction"], dct["get_pic"],
                          dct["is_running"], dct["is_set"], dct["cpt"])

    @staticmethod
    def load(filename):
        """
            Permet de charger un objet Camera depuis un fichier au format json adapté

        :param filename:

        """
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f, object_hook=Camera.hook)


if __name__ == '__main__':
    c = Camera(Point(0, 0, 0), Vecteur(1, 0, 0))
