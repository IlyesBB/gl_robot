from gl_lib.sim.geometry import *
from gl_lib.sim.robot import Tete

class Capteur(object):
    """
    Classe abstraite

    La positione et la direction du capteur sont liées a celles de la tête s'il y en a une
    """

    def __init__(self, centre:Point=Point(0, 0, 0), direction:Vecteur=Vecteur(1, 0, 0)):
        self.centre=centre
        self.direction = direction

    def __repr__(self):
        return "Sensor de type : {} , position : {}".format(type(self), self.centre)

    def update(self):
        pass

    def clone(self):
        return Capteur(self.centre, self.direction)

    def rotate(self, teta:float or int, axis=None):
        self.direction.rotate(teta, axis)

    def rotate_around(self, point:Point, teta:float or int, axis=None):
        self.centre.rotate_around(point, teta, axis)

    def rotate_all_around(self, point:Point, teta:float or int, axis=None):
        self.rotate_around(point, teta, axis)
        self.rotate(teta, axis)

    def move(self, vector:Vecteur):
        self.centre.move(vector)