# -*- coding: utf-8 -*-
import json
from collections import OrderedDict
from time import sleep

from gl_lib.sim.geometry import Point, Vecteur, Polygone3D, ApproximableAPave
from math import *


class Pave(Polygone3D, ApproximableAPave):
    """
        Classe définissant un pavé dans un repère en 3D
    """

    def __init__(self, width: float or int, length: float or int, height: float or int, centre=Point(0, 0, 0),
                 vertices: [Point] = None):
        """
            Constructeur ajoutant les 8 sommets autour du centre par défaut: (0,0,0)
        """
        Polygone3D.__init__(self, centre, vertices)
        self.width = float(width)
        self.length = float(length)
        self.height = float(height)

        if vertices is None:
            self.vertices = list()
            self.add_vertex(Point(self.centre.x - width / 2, self.centre.y - length / 2, self.centre.z + height / 2))
            self.add_vertex(Point(self.centre.x + width / 2, self.centre.y - length / 2, self.centre.z + height / 2))
            self.add_vertex(Point(self.centre.x + width / 2, self.centre.y + length / 2, self.centre.z + height / 2))
            self.add_vertex(Point(self.centre.x - width / 2, self.centre.y + length / 2, self.centre.z + height / 2))
            self.add_vertex(Point(self.centre.x - width / 2, self.centre.y - length / 2, self.centre.z - height / 2))
            self.add_vertex(Point(self.centre.x + width / 2, self.centre.y - length / 2, self.centre.z - height / 2))
            self.add_vertex(Point(self.centre.x + width / 2, self.centre.y + length / 2, self.centre.z - height / 2))
            self.add_vertex(Point(self.centre.x - width / 2, self.centre.y + length / 2, self.centre.z - height / 2))

    def __ne__(self, pave):
        return not self.__eq__(pave)

    def __dict__(self):
        dct2 = Polygone3D.dict(self)
        dct = OrderedDict()
        l=[self.vertices[i].__dict__() for i in range(len(self.vertices))]
        dct["__class__"] = Pave.__name__
        dct["centre"] = dct2["centre"]
        dct["width"] = self.width
        dct["length"] = self.length
        dct["height"] = self.height
        dct["vertices"] = dct2["vertices"]
        return dct

    def rotate_around(self, point, teta, axis=None):
        """
            Tourne le centre du pavé autour de point selon z d'un angle teta

        :param point: Point autour duquel tourner
        :type point: Point
        :param teta: Angle en radians
        :type teta: float
        :param axis: 'z', 'x' ou 'y'

        """
        n_centre = point + (self.centre - point).to_vect().rotate(teta=teta, axis=axis)
        v = n_centre - self.centre
        self.move(v)

    def rotate_all_around(self, point: Point, teta: float, axis=None):
        """
            Tourne le pavé autour de point selon z d'un angle teta, et tourne ses sommets autour de son centre

        :param point: Point autour duquel tourner
        :type point: Point
        :param teta: Angle en radians
        :type teta: float
        :param axis: 'z', 'x' ou 'y'

        """
        if point != self.centre:
            n_centre = point + (self.centre - point).to_vect().rotate(teta=teta, axis=axis)
            self.centre = n_centre.clone()

        for i in range(0, len(self.vertices)):
            self.vertices[i] = point + (self.vertices[i] - point).to_vect().rotate(teta=teta, axis=axis)

        return self.clone()

    def rotate(self, teta: float, axis=None):
        """
            Tourne le pavé selon autour de son centre

        :param teta: Angle en radians
        :type teta: float
        :param axis: 'z', 'x' ou 'y'

        """
        return self.rotate_all_around(self.centre, teta, axis=axis)


    def clone(self):
        return Pave(self.width, self.length, self.height, self.centre.clone(),
                    [self.vertices[i].clone() for i in range(len(self.vertices))])

    def get_length(self):
        """
            Retourne la longueur caractéristique du pavé, selon l'axe z
        """
        return max(self.width, self.length)

    def __eq__(self, pave):
        if not isinstance(pave, type(self)):
            return False
        if self.centre != pave.centre:
            return False
        if self.length != pave.length or self.width != pave.width or self.height != self.height:
            return False
        for i in range(len(self.vertices)):
            if self.vertices[i] != pave.vertices[i]:
                return False
        return True


    def __str__(self):
        s = "("+self.__class__.__name__
        s += "({:6.6},{:6.6},{:6.6});  vertices: ".format(self.width, self.length, self.height)
        for i in range(int(len(self.vertices)/2)):
            s += "n{}({:6.6},{:6.6}) ".format(i, self.vertices[i].x, self.vertices[i].y)
        return s+")"

    def get_inclinaisont(self):
        """
            Retourne la différence d'angle entre un des côtés du pavé sur le plan Oxy, et le vecteur (1,0,0)
        """
        return (self.vertices[1]-self.vertices[0]).to_vect().diff_angle(Vecteur(1,0,0))

    @staticmethod
    def load(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f, object_hook=Pave.hook)


    @staticmethod
    def hook(dct):
        if dct["__class__"]==Point.__name__:
            return Point.hook(dct)
        elif dct["__class__"]==Pave.__name__:
            return Pave(dct["width"], dct["length"], dct["height"],
                dct["centre"], [dct["vertices"][i] for i in range(len(dct["vertices"]))])

    def get_pave(self):
        return self


if __name__ == '__main__':
    p = Pave(150, 200, 0, Point(50,50,0))
    print(p)
