# -*- coding: utf-8 -*-
import json
from collections import OrderedDict
from gl_lib.sim.robot.sensor import CapteurIR, Accelerometre, Camera, Capteur

from gl_lib.sim.geometry import *
from math import pi


class Tete(Objet3D):
    """
    Définit une tête, ses capteurs et ses primitives de rotation

    Le centre et la direction de la tête peuvent être liés à un couple (centre, dir_robot) (cf __init__)
    La tête peut toujours tourner par rapport à dir_robot, à condition de mettre à jour direction avec set_dir()
    """
    # indices pour repérer les capteurs
    SENSORS = ["acc", "ir", "cam"]

    def __init__(self, centre: Point = Point(0, 0, 0), dir_robot: Vecteur = Vecteur(1, 0, 0),
                 dir_rel: Vecteur = Vecteur(1, 0, 0), direction: Vecteur = Vecteur(1, 1, 1),
                 lcapteurs: {CapteurIR, Accelerometre, Camera} = None):
        """
            Initialise les attributs de la tête, avec la direction de la tête égale en valeur à la direction de
            référence

            La tête crée par défaut est équipée de 3 capteurs: infrarouge de distance, caméra et accéléromètre
        :param centre: Centre de la tête
        :param dir_robot: Direction de référence de la tête
        :param dir_rel: Direction relative de la tête par rapport à la direction de référence
        :param direction: Direction réelle de la tête
        :param lcapteurs: liste de capteurs
        """
        Objet3D.__init__(self, centre)
        self.dir_robot = dir_robot
        self.dir_rel = dir_rel
        angle = self.dir_rel.get_angle()
        self.direction = self.dir_robot.clone().rotate(angle)

        # On intialise directement les capteurs
        self.sensors = dict()
        self.sensors["ir"] = CapteurIR(self.centre, self.direction)
        self.sensors["acc"] = Accelerometre(self.centre, self.direction)
        self.sensors["cam"] = Camera(self.centre, self.direction)
        if lcapteurs is not None:
            # Sauf si spécifié autrement
            self.sensors = lcapteurs
            for c in self.sensors.keys():
                (self.sensors[c]).attach(self.centre, (self.sensors[c]).direction)
        if direction is not None:
            self.direction = direction

    def add_sensors(self, dict_sensors: {}) -> int:
        """
            Permet d'ajouter n'importequel type de capteur
            Il suffit de le donner, avec son nom, en argument dans un dictionnaire
        """
        if len(dict_sensors.keys()) < 1:
            return 0
        cpt = 0
        for key in dict_sensors.keys():
            self.sensors[key] = dict_sensors[key].clone()
            cpt += 1
        return cpt

    def attach(self, centre: Point, direction: Vecteur):
        """
            Permet d'attacher la tête et ses capteurs à un point et une direction
            contrairement au centre de la tête par rapport à centre

        :param centre: On copie la référence
        :param direction: On copie la référence
        """
        self.dir_robot = direction
        # La direction de la tête est initialisée à direction, mais ne pointe pas vers l'argument
        self.direction = direction.clone()
        # Contrairement au centre de la tête
        self.centre = centre
        for k in Tete.SENSORS:
            if self.sensors[k] is not None:
                # Il en va de même pour les capteurs
                self.sensors[k].centre = centre
                self.sensors[k].direction = self.direction.clone()

    def __dict__(self):
        dct = OrderedDict()
        dct["__class__"] = Tete.__name__
        l = list()
        if len(self.sensors) >= 1:
            l = {k: self.sensors[k].__dict__() for k in Tete.SENSORS if self.sensors[k] is not None}
        dct["centre"] = self.centre.__dict__()
        dct["direction"] = self.direction.__dict__()
        dct["dir_robot"] = self.dir_robot.__dict__()
        dct["dir_rel"] = self.dir_rel.__dict__()
        dct["lcapteurs"] = l
        return dct

    def __str__(self):
        """
            Affiche uniquement la classe et la liste de capteurs sous forme simplifiée
        """
        s = "({}; sensors: {})".format(self.__class__.__name__, [str(self.sensors[key]) for key in self.sensors.keys()])
        return s

    def __eq__(self, other):
        if Objet3D.__eq__(self, other) is False:
            return False
        if self.dir_robot != other.dir_robot or self.direction != other.direction:
            return False
        if self.dir_rel != other.dir_rel:
            return False
        for k in self.sensors.keys():
            if self.sensors[k] != other.sensors[k]:
                return False
        return True

    def rotate(self, angle: float, axis=None):
        """
            Tourne le vecteur qui représenta la direction de la tête relativement à celle du robot, prise à (1,0,0)
        """
        self.dir_rel.rotate(angle, axis)

    def set_dir(self):
        """
            Met à jour la direction de la tête en fonction de sa direction relative dir_rel et la direction de
            référence dir_robot
        """
        angle = self.dir_rel.get_angle()
        self.direction = self.dir_robot.clone().rotate(angle)
        for k in Tete.SENSORS:
            if self.sensors[k] is not None:
                self.sensors[k].direction = self.direction

    def update(self):
        """
            Met à jour la direction et les capteurs
        """
        self.set_dir()
        for k in self.sensors.keys():
            if self.sensors[k] is not None:
                self.sensors[k].update()

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

    def clone(self):
        l = [self.sensors[k].clone() for k in Tete.SENSORS if self.sensors[k] is not None]
        return Tete(self.centre.clone(), self.dir_robot.clone(), self.dir_rel.clone(), self.direction.clone(), l)

    @staticmethod
    def load(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f, object_hook=Tete.hook)



if __name__ == '__main__':
    t = Tete()

    t.save("tete.json")
    t2 = Tete.load("tete.json")
    print(str(t2))
