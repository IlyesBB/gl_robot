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
    """
    # Angle de vue de la caméra en y, en degrés
    ANGLE_VY = 180

    def __init__(self, centre=Point(0, 0, 0), direction=Vecteur(1, 0, 0),get_pic:bool=False,
                 is_running:bool=False, is_set:bool=False,cpt:int=0):
        """
        :param centre: Centre de la caméra, peut être attaché à une tête
        :param direction: Direction de la caméra, même remarque
        """
        Capteur.__init__(self, centre=centre, direction=direction)
        # arene doit être initialisé en dehors de la classe
        self.arene = None
        self.window = None # Window (gl_lib.sim.robot.sensor.camera.d3.Window)
        self.raw_im = None # Image

        self.is_set, self.is_running = is_set, is_running
        self.get_pic = get_pic
        self.cpt = cpt
        self.rep_name = fonctions.get_project_repository()+REPNAME_SCREENSHOTS

    def run(self):
        """
        Lance l'application pyglet
        :return:
        """
        self.is_running = True
        self.window = Window(self.arene, self)
        glClearColor(0, 0, 0, 0)
        glEnable(GL_DEPTH_TEST)
        pyglet.app.run()

    def set_environnement(self, arene:Arene):
        self.arene = arene

    def picture(self):
        """
        Cette méthode est appelée à la fin de on_draw de la window
        """
        if self.get_pic:
            #print("Acquiring image...")
            image = pyglet.image.get_buffer_manager().get_color_buffer().get_image_data()
            self.raw_im = Image.frombytes(image.format, (image.width, image.height), image.data)
            # L'image récupérée est alternée...
            self.raw_im = self.raw_im.rotate(180)
            self.raw_im = self.raw_im.transpose(Image.FLIP_LEFT_RIGHT)
            self.get_pic = False
            #print("Picture ", self.cpt, " taken")
            self.cpt += 1
        self.is_set = True



    def print_image(self, fname):
        """
        Enregistre la dernière image enregistrée dans le fichier de nom fname
        :param fname:
        :return:
        """
        #print("Printing image...")
        if self.raw_im is not None:
            s=self.rep_name+fname
            self.raw_im.save(s)

    def get_image(self):
        if self.raw_im is not None:
            return self.raw_im.getdata()

    def take_picture(self):
        """
        Si aucune application n'a été lancée avant l'appel de cette fontion, une application est lancée
        :return:
        """
        self.get_pic = True
        if not self.is_running and not self.is_set:
            td = Thread(target=self.run)
            td.start()

    def clone(self):
        return Camera(self.centre.clone(), self.direction.clone(), self.get_pic, self.is_running, self.is_set, self.cpt)

    def stop(self):
        pyglet.app.exit()
        self.is_set = False

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

    @staticmethod
    def hook(dct):
        """ On ne récupère pas la liste d'objest à ignorer"""
        if dct["__class__"] == Vecteur.__name__:
            return Vecteur.hook(dct)
        if dct["__class__"] == Point.__name__:
            return Point.hook(dct)
        if dct["__class__"] == Camera.__name__:
            return Camera(dct["centre"], dct["direction"], dct["get_pic"],
                          dct["is_running"], dct["is_set"], dct["cpt"])

    @staticmethod
    def load(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f, object_hook=Camera.hook)


if __name__ == '__main__':

    c= Camera(Point(0,0,0), Vecteur(1,0,0))

