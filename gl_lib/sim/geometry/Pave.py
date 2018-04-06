from gl_lib.sim.geometry.Objet3D import *
from gl_lib.sim.geometry.point import Point, Vecteur
from gl_lib.sim.geometry.Polygone3D import Polygone3D
from math import *


class Pave(Polygone3D):
    """
    Classe definissant un pave dans un repere en 3D
    """

    def __init__(self, width: float or int, length: float or int, height: float or int, centre=Point(0, 0, 0)):
        """
        Constructeur ajoutant les 8 sommets autour du centre par defaut: (0,0,0)
        """
        Polygone3D.__init__(self, centre=centre)
        self.width = float(width)
        self.length = float(length)
        self.height = float(height)

        self.add_vertex(self.centre + Point(-self.width / 2, -self.length / 2, self.height / 2))
        self.add_vertex(self.centre + Point(self.width / 2, -self.length / 2, self.height / 2))
        self.add_vertex(self.centre + Point(self.width / 2, self.length / 2, self.height / 2))
        self.add_vertex(self.centre + Point(-self.width / 2, self.length / 2, self.height / 2))
        self.add_vertex(self.centre + Point(-self.width / 2, self.length / 2, -self.height / 2))
        self.add_vertex(self.centre + Point(self.width / 2, -self.length / 2, -self.height / 2))
        self.add_vertex(self.centre + Point(self.width / 2, self.length / 2, -self.height / 2))
        self.add_vertex(self.centre + Point(-self.width / 2, self.length / 2, -self.height / 2))

    def rotate_around(self, point: Point, teta: float, axis=None):
        """
        Tourne le pave autour de point selon z d'un angle teta
        """
        n_centre = point + (self.centre - point).to_vect().rotate(teta=teta, axis=axis)
        v = n_centre - self.centre
        self.centre = n_centre.clone()

        for i in range(0, len(self.vertices)):
            self.vertices[i] = self.vertices[i] + v

    def rotate_all_around(self, point: Point, teta: float, axis=None):
        """
        Tourne le pave autour de point selon z d'un angle teta
        """
        if point != self.centre:
            n_centre = point + (self.centre - point).to_vect().rotate(teta=teta, axis=axis)
            self.centre = n_centre.clone()

        for i in range(0,len(self.vertices)):
            self.vertices[i] = point + (self.vertices[i] - point).to_vect().rotate(teta=teta, axis=axis)

    def rotate(self, teta: float, axis=None):
        """
        Tourne le pavé selon z autour du centre
        """
        self.rotate_all_around(self.centre, teta, axis=axis)


if __name__ == '__main__':
    p = Pave(1, 1, 0)
    print(p)
    p2 = p.clone()
    print(p2)

