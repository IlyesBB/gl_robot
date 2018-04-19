import json
from collections import OrderedDict
from gl_lib.utils import Serializable
from gl_lib.sim.geometry import Point

class Objet3D(Serializable):
    """
    Classe definissant un objet 3D de facon abstraite
    """

    def __init__(self, centre=None):
        """
        centre : Point definissant le centre de l'objet. initialise a (0, 0, 0)
        """
        self.centre = centre

    def move(self, vecteur):
        """
        deplace les Point dans sommets et centre de l'objet
        """
        self.centre.move(vecteur)

    def rotate_around(self, point, teta, axis=None):
        """
        tourne l'objet d'un angle teta auout d'un point
        :param point: Point
        :param teta: float en rad
        """
        self.centre.rotate_around(point, teta, axis)

    def clone(self):
        return Objet3D(self.centre.clone())

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False
        if other.centre != self.centre:
            return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        """
        Quand on entre un objet3D dans l'interpreteur
        """
        s = ""
        d = self.__dict__()
        for k in d.keys():
            if isinstance(d[k], list) and len(d[k])>0:
                s += k + " :\n"
                for i in range(len(d[k])):
                    s += "\t" + str(d[k][i]) + "\n"
            else:
                s += k+" : "+str(d[k])+"\n"
        return s

    def __getattr__(self, nom):
        """
        Permet d'acceder a un attribut

        si ce n'est pas possible:
        """
        print("L'attribut {} n'est pas accessible dans {} !".format(nom, type(self)))

    def __dict__(self):
        dct = OrderedDict()
        dct["__class__"]=Objet3D.__name__
        dct["centre"]=self.centre.__dict__()
        return dct

    def dict(self):
        o = Objet3D.clone(self)
        return o.__dict__()
    cpt = 0

    @staticmethod
    def deserialize(dct):
        if dct["__class__"]==Objet3D.__name__:
            return Objet3D(dct["centre"])
        elif dct["__class__"]==Point.__name__:
            return Point.deserialize(dct)


    @staticmethod
    def load(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f, object_hook=Objet3D.deserialize)




if __name__ == '__main__':
    o = Objet3D(Point(0,0,0))

    o.save("objet3D.json")

    o2 = Objet3D.load("objet3D.json")
    print(o2)