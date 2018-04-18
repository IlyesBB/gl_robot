from gl_lib.sim.geometry import *

from math import *
import json


class Arene(object):
    """
    Definit une structure de base pour une arene contenant des Objet3D
    """

    def __init__(self, objets3D:[Objet3D]=list()):
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
            dic.update({"__class": obj.__class__.__name__})
            return dic

        f = open(fichier, 'w')
        areneJson = json.dump(self, f, indent=4, sort_keys=True, default=my_enc)
        f.close()

    def load(self, fichier):

        def my_hook(dic):
            if "__class" in dic:
                cls = dic.pop("__class")
                return eval(cls)(**dic)
            return dic

        f = open(fichier, "r")
        obj = json.load(f, object_hook=my_hook)
        return obj


if __name__ == '__main__':
    from gl_lib.sim.robot import RobotMotorise, RobotTarget, Tete
    from gl_lib.sim.robot.sensor import *
    from gl_lib.sim.geometry import *
    from gl_lib.sim import Simulation
    from gl_lib.sim.robot.strategy.vision import StrategieDeplacementVision, StrategieVision

    a = AreneFermee(15, 15, 15)
    p1 = Pave(1, 1, 1)
    l = [Vecteur(a.width - p1.width / 2, p1.length / 2, p1.height / 2),
         Vecteur(a.width - p1.width / 2, p1.length / 2, -p1.height / 2 + a.height),
         Vecteur(p1.width / 2, a.length - p1.length / 2, p1.height / 2),
         Vecteur(p1.width / 2, a.length - p1.length / 2, -p1.height / 2 + a.height),
         Vecteur(a.width - p1.width / 2, a.length - p1.length / 2, p1.height / 2),
         Vecteur(a.width - p1.width / 2, a.length - p1.length / 2, -p1.height / 2 + a.height)]

    for v in l:
        a.add(p1.move(v).clone())
    r = RobotTarget(pave=Pave(1, 1, 1, centre=Point(0.5, 0.5, 1)), direction=Vecteur(1, 0, 0).norm())
    r.set_wheels_rotation(3, 0)

    s = Simulation(StrategieVision(r, a))

    s.start()
