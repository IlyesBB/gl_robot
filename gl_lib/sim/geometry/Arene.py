from collections import OrderedDict

from gl_lib.sim.geometry import *

from math import *
import json


class Arene(Objet3D):
    """
    Definit une structure de base pour une arene contenant des Objet3D
    """
    def __init__(self, objets3D:[Objet3D]=list(), centre:Point=None):
        """
        objets3D: [Objet3D]
        """
        Objet3D.__init__(self, centre)
        self.objets3D = objets3D

    def add(self, objet3D):
        """
        Ajoute un objet3D a la liste si c'est une sous classe de Objet3D
        """
        if issubclass(type(objet3D), Objet3D):
            self.objets3D.append(objet3D)

    def add_list(self, l_objets: [Objet3D]):
        """

        :param l_objets:
        :return:
        """
        for o in l_objets:
            self.add(o)

    def empty(self):
        """
        Reinitialise la liste d'objets 3D
        """
        self.objets3D = list()

    def remove(self,obj:Objet3D):
        self.objets3D.remove(obj)

    def __getattr__(self, nom):
        """
        Permet d'acceder a un attribut

        si ce n'est pas possible:
        """
        print("L'attribut {} n'est pas accessible dans Arene !".format(nom))

    def __dict__(self):
        dct = OrderedDict()

        if len(self.objets3D)>0:
            l=[self.objets3D[i].__dict__() for i in range(len(self.objets3D))]
        else:
            l=list()
        dct["__class__"] = self.__class__.__name__
        dct["objets3D"] = l
        if self.centre is not None:
            dct["centre"] = self.centre.__dict__()
        else:
            dct["centre"] = None
        return dct

    def clone(self):
        l=list()
        if len(self.objets3D)>0:
            l=[self.objets3D[i].clone() for i in range(len(self.objets3D))]
        return Arene(l,self.centre.clone())

    def dict(self):
        a = Arene.clone(self)
        return a.__dict__()

    @staticmethod
    def hook(dct):
        if dct["__class__"]==Point.__name__:
            return Point.hook(dct)
        elif dct["__class__"]==Pave.__name__:
            return Pave.hook(dct)
        elif dct["__class__"]==Arene.__name__:
            return Arene(dct["objets3D"], dct["centre"])

    @staticmethod
    def load(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f, object_hook=Arene.hook)


if __name__ == '__main__':
    from gl_lib.sim.geometry import Pave
    a = Arene([Pave(1,1,1)])

    a.save("arene.json")
    d=a.__dict__()

    a2 = Arene.load("arene.json")
    print(a2)