import json
from collections import OrderedDict
from gl_lib.sim.robot.sensor import CapteurIR, Accelerometre, Camera, Capteur

from gl_lib.sim.geometry import *
from math import pi

class Tete(Objet3D):
    """
    definit une tete, ses capteurs et ses primitives de rotation
    """
    # indices pour reperer les capteurs
    IR, ACC, CAM = 0, 1, 2

    def __init__(self, centre: Point=Point(0,0,0),dir_robot: Vecteur=Vecteur(1,0,0), dir_rel:Vecteur=Vecteur(1,0,0), direction:Vecteur=Vecteur(1,1,1),
                 lcapteurs:[Capteur]=None):
        """
        :param pave: Pave (forme du robot)
        :param direction: Vecteur norme
        """
        Objet3D.__init__(self, centre)
        self.dir_robot = dir_robot
        self.dir_rel = dir_rel
        angle=self.dir_rel.get_angle()
        self.direction=self.dir_robot.clone().rotate(angle)
        self.lcapteurs = [CapteurIR(self.centre, self.direction), Accelerometre(self.centre, self.direction),
                          Camera(self.centre, self.direction)]
        if lcapteurs is not None:
            self.lcapteurs = lcapteurs
        if direction is not None:
            self.direction = direction

    def add_sensors(self, ir = None, acc = None, cam = None) -> int:
        """ permet d'ajouter n'importequel type de sensor
        Tant qu'il respecte les type des capteurs
        """
        cpt = 0
        if ir is not None:
            self.lcapteurs[Tete.IR] = ir
            self.lcapteurs[Tete.IR].attach(self.centre, self.direction)
            cpt += 1
        if cam is not None:
            self.lcapteurs[Tete.CAM] = cam
            self.lcapteurs[Tete.CAM].attach(self.centre, self.direction)
            cpt += 1
        if acc is not None:
            self.lcapteurs[Tete.ACC] = acc
            self.lcapteurs[Tete.ACC].attach(self.centre, self.direction)
            cpt += 1
        return cpt

    def attach(self, centre:Point, direction:Vecteur):
        self.centre = centre
        self.dir_robot = direction
        self.direction = direction.clone()
        for i in range(len(self.lcapteurs)):
            if self.lcapteurs[i] is not None:
                self.lcapteurs[i].centre = centre
                self.lcapteurs[i].direction = self.direction.clone()

    def rotate(self, angle:float, axis=None):
        self.dir_rel.rotate(angle, axis)

    def set_dir(self):
        angle=self.dir_rel.get_angle()

        self.direction = self.dir_robot.clone().rotate(angle)
        for i in range(len(self.lcapteurs)):
            if self.lcapteurs[i] is not None:
                self.lcapteurs[i].direction = self.direction

    def update(self):
        self.set_dir()
        for i in range(len(self.lcapteurs)):
            if self.lcapteurs[i] is not None:
                self.lcapteurs[i].update()

    def __eq__(self, other):
        if Objet3D.__eq__(self, other) is False:
            return False
        if self.dir_robot != other.dir_robot or self.direction != other.direction:
            return False
        if self.dir_rel != other.dir_rel:
            return False
        for i in range(len(self.lcapteurs)):
            if self.lcapteurs[i] != other.lcapteurs[i]:
                return False
        return True

    def __dict__(self):
        dct = OrderedDict()
        dct["__class__"] = Tete.__name__
        l=list()
        if len(self.lcapteurs) >= 1:
            l=[self.lcapteurs[i].__dict__() for i in range(len(self.lcapteurs)) if self.lcapteurs[i] is not None]
        dct["centre"] = self.centre.__dict__()
        dct["direction"] = self.direction.__dict__()
        dct["dir_robot"] = self.dir_robot.__dict__()
        dct["dir_rel"] = self.dir_rel.__dict__()
        dct["lcapteurs"] = l
        return dct

    @staticmethod
    def deserialize(dct):
        if dct["__class__"] == Vecteur.__name__:
            return Vecteur.deserialize(dct)
        elif dct["__class__"] == Point.__name__:
            return Point.deserialize(dct)
        elif dct["__class__"] == CapteurIR.__name__:
            return CapteurIR.deserialize(dct)
        elif dct["__class__"] == Camera.__name__:
            return Camera.deserialize(dct)
        elif dct["__class__"] == Accelerometre.__name__:
            return Accelerometre.deserialize(dct)
        elif dct["__class__"] == Tete.__name__:
            return Tete(dct["centre"], dct["dir_robot"], dct["dir_rel"], dct["direction"], dct["lcapteurs"])

    @staticmethod
    def load(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f, object_hook=Tete.deserialize)


if __name__ == '__main__':
    t= Tete()

    t.save("tete.json")
    t2 = Tete.load("tete.json")
    print(t2)




