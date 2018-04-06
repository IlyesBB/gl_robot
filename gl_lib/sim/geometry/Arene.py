from gl_lib.sim.geometry.Objet3D import Objet3D
from gl_lib.sim.geometry.Pave import *

from math import *
import json


class Arene(object):
    """
    Definit une structure de base pour une arene contenant des Objet3D
    """

    def __init__(self, objets3D=list()):
        """
        objets3D: [Objet3D]
        """
        self.objets3D = objets3D

    def add(self, objet3D):
        """
        Ajoute un objet3D a la liste si c'est une sous classe de Objet3D
        """
        if issubclass(type(objet3D), Objet3D):
            self.objets3D.append(objet3D)

    def empty(self):
        """
        Reinitialise la liste d'objets 3D
        """
        self.objets3D = list()


    def __repr__(self):
        """
        Quand on entre une arene dans l interpreteur
        """
        return "Arene: objets3D({})".format(self.objets3D)

    def __getattr__(self, nom):
        """
        Permet d'acceder a un attribut

        si ce n'est pas possible:
        """
        print("L'attribut {} n'est pas accessible dans Arene !".format(nom))


    def save(self, fichier):

        """sauvegardeArene(Arene) prend une aréne en paramétre la convertie au format Json et l'enregiste dans un fichier texte"""

        def my_enc(obj):
            dic = dict(obj.__dict__)
            dic.update({"__class":obj.__class__.__name__})
            return dic

        if(issubclass(Arene,type(self))==False):
           print("sauvegarde Arene prend une Aréne en paramétre");
           return None
        f = open(fichier,'w')
        areneJson=json.dump(self,f,indent=4,sort_keys=True,default=my_enc)
        f.close()

    def load(self, fichier):

        def my_hook(dic):
            if "__class" in dic:
                cls = dic.pop("__class" )
                return eval(cls)(**dic)
            return dic

        f = open(fichier,"r")
        obj = json.load(f,object_hook=my_hook)
        return obj


