import json
from collections import OrderedDict

from gl_lib.sim.geometry import Objet3D, Point, Vecteur

class Polygone3D(Objet3D):
    """
    Classe definissant un polygone de facon abstraite
    """

    def __init__(self, centre:Point=Point(0,0,0), vertices:[Point]=list()):
        """
        initialise la liste des sommets
        """
        Objet3D.__init__(self, centre=centre)
        self.vertices = vertices

    def add_vertex(self, sommet):
        """
        ajoute sommet a la liste sommets du polygone
        """
        self.vertices.append(sommet.clone())

    def add_vertices(self, sommets):
        """
        Ajoute les points les uns après les autres
        :param sommets:
        :return:
        """
        for vertex in sommets:
            self.add_vertex(vertex)

    def move(self, vecteur:Vecteur):
        """
        deplace les sommets et le centre
        """
        Objet3D.move(self, vecteur)
        for s in self.vertices:
            s.move(vecteur)
        return self
        #on ne verifie pas que vecteur est bien definit
        #car c'est une classe abstraite

    def __dict__(self):
        dct = OrderedDict()
        dct["__class__"]=Polygone3D.__name__
        if self.centre is not None:
            try:
                dct["centre"] = self.centre.__dict__()
            except:
                pass
        else:
            dct["centre"] = None

        n=len(self.vertices)
        if self.vertices is not None and n>0:
            dct["vertices"] = [0]*n
            for i in range(n):
                dv = self.vertices[i].__dict__()
                dct["vertices"][i] = self.vertices[i].__dict__()

        else:
            dct["vertices"] = []
        return dct

    def dict(self):
        p = Polygone3D(centre=self.centre, vertices=self.vertices)
        return p.__dict__()

    @staticmethod
    def deserialize(dct):
        if dct["__class__"]==Point.__name__:
            return Point.deserialize(dct)
        elif dct["__class__"]==Polygone3D.__name__:
            return Polygone3D(centre=dct["centre"], vertices=[dct["vertices"][i] for i in range(len(dct["vertices"]))])

    @staticmethod
    def load(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f, object_hook=Polygone3D.deserialize)

    def clone(self):
        d=self.__dict__()
        return Polygone3D(centre=d["centre"], vertices=d["vertices"])





if __name__=='__main__':
    from gl_lib.sim.geometry import *
    p=Polygone3D(vertices=[Point(1,1,1)])

    d=p.__dict__()

    p.save("polygone3D.json")

    p2 = Polygone3D.deserialize(d)
    print(p2)

    p3 = Polygone3D.load("polygone3D.json")