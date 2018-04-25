# -*- coding: utf-8 -*-
import json
from collections import OrderedDict

from gl_lib.sim.geometry import Objet3D, Point


class Roue(Objet3D):
    """
    Definie les informations de base pour une roue
    """

    def __init__(self,diametre:float or int=0.3, centre:Point=Point(0,0,0), vitesseRot:float=0, angle:float=0):
        """

        :param diametre:
        """
        Objet3D.__init__(self, centre)
        self.diametre = diametre
        self.vitesseRot = vitesseRot
        self.angle = angle

    def turn(self, sens):
        """
        :param sens:
        :return:
        """
        if sens < 0:
            self.angle += self.vitesseRot
        elif sens > 0:
            self.angle -= self.vitesseRot

    def get_angle(self):
        return self.angle

    def clone(self):
        return Roue(self.diametre, self.centre.clone(), self.vitesseRot, self.angle)

    def __eq__(self, other):
        if Objet3D.__eq__(self, other) is False:
            return False
        if self.diametre != other.diametre:
            return False
        return True

    def __dict__(self):
        dct = OrderedDict()
        dct["__class__"] = Roue.__name__
        dct["diametre"] = self.diametre
        dct["centre"] = self.centre.__dict__()
        dct["vitesseRot"] = self.vitesseRot
        dct["angle"] = self.angle

        return dct

    @staticmethod
    def hook(dct):
        """ On ne récupère pas la liste d'objest à ignorer"""
        if dct["__class__"] == Point.__name__:
            return Point.hook(dct)
        elif dct["__class__"] == Roue.__name__:
            return Roue(dct["diametre"], dct["centre"], dct["vitesseRot"], dct["angle"])

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
