from gl_lib.sim.robot.sensor.Capteur import Capteur
from pyglet.gl import *
from threading import Thread
from gl_lib.sim.robot.sensor.camera.d3 import *
from gl_lib.sim.geometry import *
from gl_lib.sim.geometry.point import *


class Camera(Capteur, Thread):
    """
    La caméra a besoin de pouvoir lancer une application pyglet indépedante
    On la fait donc aussi hériter de Thread
    """
    # Angle de vue de la caméra en y, en degrés
    ANGLE_VY = 70

    def __init__(self, centre=Point(0, 0, 0), direction=Vecteur(1, 0, 0), arene=None, tete=None):
        """

        :param centre: Centre de la caméra, peut être attaché à une tête
        :param direction: Direction de la caméra, même remarque
        :param arene: Arène à représenter dans l'application
        """
        Thread.__init__(self)
        Capteur.__init__(self, centre=centre, direction=direction, tete=None)
        self.arene = arene
        self.get_pic=False
        self.new_pic=True

    def run(self):
        """
        Lance l'application pyglet
        :return:
        """
        window = Window(camera=self, arene=self.arene)
        glClearColor(0, 0, 0, 0)
        glEnable(GL_DEPTH_TEST)

        pyglet.app.run()

    def picture(self):
        """
        Enregistre une image dans le répertoire sim, sous le nom screenshot.png
        A CORRIGER : Paramétrage du nom du fichier
        """
        if self.get_pic:
            self.get_pic=False
            self.new_pic=True
            return pyglet.image.get_buffer_manager().get_color_buffer().save('../../screenshot.png')
        else:
            return None

    def get_picture(self):
        self.get_pic=True

if __name__ == '__main__':
    from math import pi

    Pave1 = Pave(10, 8, 30)

    Pave2 = Pave(15, 6, 25)

    Pave3 = Pave(7, 7, 7)
    arene = AreneFermee()
    arene.add(Pave1)
    arene.add(Pave2)
    arene.add(Pave3)
    c = Camera(centre=Point(26, 6, 3), direction=Vecteur(1, 0, 0).norm(), arene=arene)
    c.start()
