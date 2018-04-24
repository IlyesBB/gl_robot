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
    SENSORS = ["acc", "ir", "cam"]

    def __init__(self, centre: Point = Point(0, 0, 0), dir_robot: Vecteur = Vecteur(1, 0, 0),
                 dir_rel: Vecteur = Vecteur(1, 0, 0), direction: Vecteur = Vecteur(1, 1, 1),
                 lcapteurs: {CapteurIR, Accelerometre, Camera} = None):
        """
        :param pave: Pave (forme du robot)
        :param direction: Vecteur norme
        """
        Objet3D.__init__(self, centre)
        self.dir_robot = dir_robot
        self.dir_rel = dir_rel
        angle = self.dir_rel.get_angle()
        self.direction = self.dir_robot.clone().rotate(angle)
        self.sensors = dict()
        self.sensors["ir"] = CapteurIR(self.centre, self.direction)
        self.sensors["acc"] = Accelerometre(self.centre, self.direction)
        self.sensors["cam"] = Camera(self.centre, self.direction)
        if lcapteurs is not None:
            self.sensors = lcapteurs
            for c in self.sensors.keys():
                (self.sensors[c]).attach(self.centre, (self.sensors[c]).direction)
        if direction is not None:
            self.direction = direction

    def add_sensors(self, ir=None, acc=None, cam=None) -> int:
        """ permet d'ajouter n'importequel type de sensor
        Tant qu'il respecte les type des capteurs
        """
        cpt = 0
        if ir is not None:
            self.sensors["ir"] = ir
            self.sensors["ir"].attach(self.centre, self.direction)
            cpt += 1
        if cam is not None:
            self.sensors["cam"] = cam
            self.sensors["cam"].attach(self.centre, self.direction)
            cpt += 1
        if acc is not None:
            self.sensors["acc"] = acc
            self.sensors["acc"].attach(self.centre, self.direction)
            cpt += 1
        return cpt

    def attach(self, centre: Point, direction: Vecteur):
        self.centre = centre
        self.dir_robot = direction
        self.direction = direction.clone()
        for k in Tete.SENSORS:
            if self.sensors[k] is not None:
                self.sensors[k].centre = centre
                self.sensors[k].direction = self.direction.clone()

    def rotate(self, angle: float, axis=None):
        self.dir_rel.rotate(angle, axis)

    def set_dir(self):
        angle = self.dir_rel.get_angle()

        self.direction = self.dir_robot.clone().rotate(angle)
        for k in Tete.SENSORS:
            if self.sensors[k] is not None:
                self.sensors[k].direction = self.direction

    def update(self):
        self.set_dir()
        for k in self.sensors.keys():
            if self.sensors[k] is not None:
                self.sensors[k].update()

    def __eq__(self, other):
        if Objet3D.__eq__(self, other) is False:
            return False
        if self.dir_robot != other.dir_robot or self.direction != other.direction:
            return False
        if self.dir_rel != other.dir_rel:
            return False
        for i in range(len(self.sensors)):
            if self.sensors[k] != other.lcapteurs[k]:
                return False
        return True

    def __dict__(self):
        dct = OrderedDict()
        dct["__class__"] = Tete.__name__
        l = list()
        if len(self.sensors) >= 1:
            l = {k:self.sensors[k].__dict__() for k in Tete.SENSORS if self.sensors[k] is not None}
        dct["centre"] = self.centre.__dict__()
        dct["direction"] = self.direction.__dict__()
        dct["dir_robot"] = self.dir_robot.__dict__()
        dct["dir_rel"] = self.dir_rel.__dict__()
        dct["lcapteurs"] = l
        return dct

    @staticmethod
    def hook(dct):
        if not "__class__" in dct.keys():
            return dct
        if dct["__class__"] == Vecteur.__name__:
            return Vecteur.hook(dct)
        elif dct["__class__"] == Point.__name__:
            return Point.hook(dct)
        elif dct["__class__"] == CapteurIR.__name__:
            return CapteurIR.hook(dct)
        elif dct["__class__"] == Camera.__name__:
            return Camera.hook(dct)
        elif dct["__class__"] == Accelerometre.__name__:
            return Accelerometre.hook(dct)
        elif dct["__class__"] == "sensors_dict":
            return dct
        elif dct["__class__"] == Tete.__name__:
            return Tete(dct["centre"], dct["dir_robot"], dct["dir_rel"], dct["direction"], dct["lcapteurs"])

    @staticmethod
    def load(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f, object_hook=Tete.hook)

    def clone(self):
        l = [self.sensors[k].clone() for k in Tete.SENSORS if self.sensors[k] is not None]
        return Tete(self.centre.clone(), self.dir_robot.clone(), self.dir_rel.clone(), self.direction.clone(), l)


if __name__ == '__main__':
    t = Tete()

    t.save("tete.json")
    t2 = Tete.load("tete.json")
    print(t2)
