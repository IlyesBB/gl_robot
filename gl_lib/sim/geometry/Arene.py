# -*- coding: utf-8 -*-
from collections import OrderedDict

from gl_lib.sim.geometry import *

from math import *
import json


class Arene(Objet3D):
    """
        Définit une structure de base pour une arène contenant des Objet3D

        TODO: Faire hériter Arene de list, pour pouvoir implémenter __len__ ...
    """
    def __init__(self, objets3D=list(), centre=None):
        """
            Initialise la liste d'objets 3D
        :param objets3D: Liste d'objets de l'arène
        :type objets3D: [Objet3D]
        :param centre: Centre de l'arène
        :type centre: Point

        TODO: Prendre en compte l'initialisation du centre
        """
        Objet3D.__init__(self, centre)
        self.objets3D = objets3D

    def add(self, objet3D):
        """
            Ajoute un objet 3D à la liste si c'est son type est une sous classe de Objet3D
        """
        if issubclass(type(objet3D), Objet3D):
            self.objets3D.append(objet3D)

    def add_list(self, l_objets):
        """
            Ajoute une liste d'objets 3D dans l'arène

        :param l_objets: Liste d'objets à ajouter
        :type l_objets: [Objet3D]

        """
        for o in l_objets:
            self.add(o)

    def empty(self):
        """
            Réinitialise la liste d'objets 3D
        """
        self.objets3D = list()

    def remove(self,obj):
        """
            Supprime l'objet de l'arène

        :param obj:
        :return:

        """
        self.objets3D.remove(obj)

    def __getattr__(self, nom):
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