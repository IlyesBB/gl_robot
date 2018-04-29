# -*- coding: utf-8 -*-
import json
from collections import OrderedDict

from gl_lib.sim.geometry import Objet3D, Point


class Roue(Objet3D):
    """
        Définie les informations de base pour une roue
    """
    KEYS = ["diametre", "centre", "vitesseRot", "angle"]

    def __init__(self, diametre=0.3, vitesseRot=0, angle=0, centre=None):
        """
            Initialise les attributs de la roue
        :param diametre: Diamètre en mètres
        :type diametre: float
        :param centre: Centre de la roue
        :type centre: Point
        :param vitesseRot: Vitesse de rotation en degrés par seconde
        :type vitesseRot: float
        :param angle: Angle total tourné en degrés
        :type angle: float
        """
        Objet3D.__init__(self, centre)
        self.diametre = diametre
        self.vitesseRot = vitesseRot
        self.angle = angle

    def __dict__(self):
        dct = OrderedDict()
        dct["__class__"] = Roue.__name__
        dct["diametre"] = self.diametre
        dct["centre"] = self.centre.__dict__()
        dct["vitesseRot"] = self.vitesseRot
        dct["angle"] = self.angle

        return dct

    def __eq__(self, other):
        if Objet3D.__eq__(self, other) is False:
            return False
        if self.diametre != other.diametre:
            return False
        return True

    def turn(self, sens: int or float):
        """
            Permet d'exécuter une rotation en avant ou en arrière
        """
        if sens < 0:
            self.angle += self.vitesseRot
        elif sens > 0:
            self.angle -= self.vitesseRot



    @staticmethod
    def hook(dct):
        """ On ne récupère pas la liste d'objest à ignorer"""
        if dct["__class__"] == Point.__name__:
            return Point.hook(dct)
        elif dct["__class__"] == Roue.__name__:
            return Roue(**{key:dct[key] for key in Roue.KEYS})

    @staticmethod
    def load(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f, object_hook=Roue.hook)


if __name__ == '__main__':
    r = Roue(10)
    r.save("roue.json")
    print(r)
    r2 = Roue.load("roue.json")
    print(r2)
