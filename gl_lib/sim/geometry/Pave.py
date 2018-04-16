from gl_lib.sim.geometry import Point, Vecteur, Polygone3D
from math import *


class Pave(Polygone3D):
    """
    Classe definissant un pave dans un repere en 3D
    """

    def __init__(self, width: float or int, length: float or int, height: float or int, centre=Point(0, 0, 0), vertices:[Point]=None):
        """
        Constructeur ajoutant les 8 sommets autour du centre par defaut: (0,0,0)
        """
        Polygone3D.__init__(self, centre, vertices)
        self.width = float(width)
        self.length = float(length)
        self.height = float(height)

        if vertices is None:
            self.add_vertex(Point(self.centre.x - width / 2, self.centre.y - length / 2, self.centre.z + height / 2))
            self.add_vertex(Point(self.centre.x + width / 2, self.centre.y - length / 2, self.centre.z + height / 2))
            self.add_vertex(Point(self.centre.x + width / 2, self.centre.y + length / 2, self.centre.z + height / 2))
            self.add_vertex(Point(self.centre.x - width / 2, self.centre.y + length / 2, self.centre.z + height / 2))
            self.add_vertex(Point(self.centre.x - width / 2, self.centre.y - length / 2, self.centre.z - height / 2))
            self.add_vertex(Point(self.centre.x + width / 2, self.centre.y - length / 2, self.centre.z - height / 2))
            self.add_vertex(Point(self.centre.x + width / 2, self.centre.y + length / 2, self.centre.z - height / 2))
            self.add_vertex(Point(self.centre.x - width / 2, self.centre.y + length / 2, self.centre.z - height / 2))
        else:
            self.vertices=list()
            for vertex in vertices:
                self.add_vertex(vertex.clone())


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

        for i in range(0,len(self.vertices)):
            self.vertices[i] = point + (self.vertices[i] - point).to_vect().rotate(teta=teta, axis=axis)

    def rotate(self, teta: float, axis=None):
        """
        Tourne le pavé selon z autour du centre
        """
        self.rotate_all_around(self.centre, teta, axis=axis)
        return self.clone()

    def clone(self):
        return Pave(self.width, self.length, self.height, self.centre, self.vertices)

    def move(self, vecteur:Vecteur):
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

    def __ne__(self, pave):
        return not self.__eq__(pave)


if __name__ == '__main__':
    p = Pave(1, 1, 0)
    print(p)
    p2 = p.clone()
    print(p2)

    p2.move(Vecteur(1,0,0))
    print(p2, p)

