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


class Camera(Thread, Capteur):
    """
    La caméra a besoin de pouvoir lancer une application pyglet indépedante
    On la fait donc aussi hériter de Thread

    Attention: Il ne faut pas redéfinir la méthode __eq__ dans cette classe ou ses classes mères
    au risque de générer des bugs
    """
    # Angle de vue de la caméra en y, en degrés
    ANGLE_VY = 180

    def __init__(self, centre=Point(0, 0, 0), direction=Vecteur(1, 0, 0), arene:Arene=None, get_pic=False, new_pic=False):
        """
        :param centre: Centre de la caméra, peut être attaché à une tête
        :param direction: Direction de la caméra, même remarque
        :param arene: Arène à représenter dans l'application
        """
        Thread.__init__(self)
        Capteur.__init__(self, centre=centre, direction=direction)
        self.arene = arene
        self.window = None
        self.get_pic=get_pic
        self.new_pic=new_pic
        self.pix_data = None
        self._stop_event = Event()
        self.fname = fonctions.get_project_repository()+REPNAME_SCREENSHOTS+FILENAME_SCREENSHOT
        self.cpt = 0
        self.lock = None
        if arene is None:
            self.arene = AreneFermee(10,10,10)

    def run(self):
        """
        Lance l'application pyglet
        :return:
        """
        self.window = Window(self.arene, self)
        glClearColor(0, 0, 0, 0)
        glEnable(GL_DEPTH_TEST)

        pyglet.app.run()

    def picture(self):
        """
        Enregistre une image dans le répertoire sim, sous le nom screenshot.png
        A CORRIGER : Paramétrage du nom du fichier
        """
        if self.get_pic:
            image = pyglet.image.get_buffer_manager().get_color_buffer().get_image_data()
            self.pix_data = image
            self.print_picture()
            self.new_pic = True
            self.get_pic = False
            #print("Picture ", self.cpt, " taken")
            self.cpt += 1

    def print_picture(self):
        s = self.fname+str(self.cpt)+FORMAT_SCREENSHOT
        self.pix_data.save(s)


    def get_picture(self):
        self.get_pic=True
        self.new_pic=False
    def clone(self):
        return Camera(self.centre, self.direction, self.arene, self.get_pic, self.new_pic)

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()



if __name__ == '__main__':

    Pave1 = Pave(10, 8, 30)

    Pave2 = Pave(15, 6, 25)

    Pave3 = Pave(7, 7, 7)
    arene = AreneFermee()
    arene.add(Pave1)
    arene.add(Pave2)
    arene.add(Pave3)
    c = Camera(centre=Point(26, 6, 3), direction=Vecteur(1, 0, 0).norm(), arene=arene)
    c.start()
