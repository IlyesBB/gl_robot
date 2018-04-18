import json
from collections import OrderedDict
from time import sleep

from gl_lib.sim.geometry import Point, Vecteur, Polygone3D, ApproximableAPave
from math import *


class Pave(Polygone3D, ApproximableAPave):
    """
    Classe definissant un pave dans un repere en 3D
    """

    def __init__(self, width: float or int, length: float or int, height: float or int, centre=Point(0, 0, 0),
                 vertices: [Point] = None):
        """
        Constructeur ajoutant les 8 sommets autour du centre par defaut: (0,0,0)
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

    def rotate_around(self, point: Point, teta: float, axis=None):
        """
        Tourne le pave autour de point selon z d'un angle teta
        """
        n_centre = point + (self.centre - point).to_vect().rotate(teta=teta, axis=axis)
        v = n_centre - self.centre
        self.move(v)

    def rotate_all_around(self, point: Point, teta: float, axis=None):
        """
        Tourne le pave autour de point selon z d'un angle teta
        """
        if point != self.centre:
            n_centre = point + (self.centre - point).to_vect().rotate(teta=teta, axis=axis)
            self.centre = n_centre.clone()

        for i in range(0, len(self.vertices)):
            self.vertices[i] = point + (self.vertices[i] - point).to_vect().rotate(teta=teta, axis=axis)

    def rotate(self, teta: float, axis=None):
        """
        Tourne le pavé selon z autour du centre
        """
        self.rotate_all_around(self.centre, teta, axis=axis)
        return self.clone()

    def clone(self):
        l=list()
        for i in range(len(self.vertices)):
            l.append(self.vertices[i].clone())
        return Pave(self.width, self.length, self.height, self.centre.clone(), l)

    def move(self, vecteur: Vecteur):
        Polygone3D.move(self, vecteur)
        return self

    def get_length(self):
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

    def __repr__(self):
        s = "Pave {} : width {} : length {} : height {}\n".format(self.centre, self.width, self.length, self.height)
        s += "["
        for i in range(len(self.vertices)):
            s += str(self.vertices[i])+", "
        s += "]"
        return s

    def __ne__(self, pave):
        return not self.__eq__(pave)

    def __dict__(self):
        dct = OrderedDict()
        l=[self.vertices[i].__dict__() for i in range(len(self.vertices))]
        dct["__class__"] = "Pave"
        dct["centre"] = self.centre.__dict__()
        dct["width"] = self.width
        dct["length"] = self.length
        dct["height"] = self.height
        dct["vertices"] = l
        return dct

    @staticmethod
    def deserialize(dct):
        if dct["__class__"] == "Pave":
            print(dct["vertices"])
            return Pave(dct["width"],dct["length"],dct["height"],Point.deserialize(dct["centre"]),
                        [Point.deserialize(dct["vertices"][i]) for i in range(1,len(dct["vertices"]))])

        pass

    @staticmethod
    def load(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f, object_hook=Pave.deserialize)

    def get_pave(self):
        return self


if __name__ == '__main__':
    p = Pave(1, 1, 0)
    p.save("pave.json")
    sleep(3)
    dct = p.__dict__()

    p3 = Pave.deserialize(dct)
    print(p3)