# -*- coding: utf-8 -*-
import json
from collections import OrderedDict

from gl_lib.sim.robot.strategy import Strategie
from gl_lib.sim.robot.strategy.deplacement import StrategieDeplacement
from gl_lib.sim.robot.strategy.vision import StrategieVision
from gl_lib.sim.robot import RobotMotorise, Tete, RobotTarget
from gl_lib.config import PAS_TEMPS
from gl_lib.sim.geometry import Point, Arene
from gl_lib.config import PIX_PAR_M
from math import sin, pi
from math import sqrt


def my_print(**kwargs):
    for key in kwargs.keys():
        print(key, kwargs[key])


class DeplacementDroit(StrategieDeplacement):
    """
        Fais avancer un robot en argument sur une certaine distance
    """
    INIT = {'advancing': True, 'distance': 0.0, 'distance_max': 1.0, 'vitesse': 60, 'posDepart': None}
    KEYS = StrategieDeplacement.KEYS + ["advancing", "distance", "distance_max", "posDepart"]

    def __init__(self, **kwargs):
        """
            Prend en argument obligatoire un robot. Par défaut, la classe commande le robot pour avancer sur un mètre
        :param distance_max: Distance maximale de laquelle avancer en mètres
        :param vitesse: Vitesse en degrés par seconde à laquelle intialiser les roues
        """
        keys = kwargs.keys()
        for key in DeplacementDroit.INIT.keys():
            if not key in keys:
                kwargs[key] = DeplacementDroit.INIT[key]
        StrategieDeplacement.__init__(self, robot=kwargs["robot"])
        self.advancing = kwargs["advancing"]  # Booléen indiquant si le robot est en marche
        self.distance = kwargs["distance"]
        self.distance_max = kwargs["distance_max"]
        self.posDepart = kwargs["posDepart"]
        if self.distance_max is not None:
            try:
                self.init_movement(self.distance_max, kwargs["vitesse"])
            except KeyError:
                # Si la vitesse n'est pas initialisée
                self.init_movement(self.distance_max)

    def __dict__(self):
        dct = OrderedDict()
        dct["__class__"] = DeplacementDroit.__name__
        for key in DeplacementDroit.KEYS:
            try:
                dct[key] = self.__getattribute__(key).__dict__()
            except:
                dct[key] = self.__getattribute__(key)
        return dct

    def __str__(self):
        d_str = StrategieDeplacement.__str__(self)
        s = d_str[:len(d_str)-1]+"\n"
        s += "-advancing: {}; distance: {}; distance_max: {}".format(self.advancing, self.distance, self.distance_max)
        return s

    def init_movement(self, distance_max, vitesse=60):
        """
            Réinitialise les variables du mouvement, et active la mise à jour dans update()

        :param distance_max: Distance maximale de laquelle avancer en mètres
        :param vitesse: Vitesse en degrés par seconde à laquelle initialiser les roues

        """
        self.advancing = True  # Booléen indiquant si le robot est en marche
        self.distance = 0
        self.distance_max = distance_max
        self.posDepart = self.robot.forme.centre.clone()
        self.robot.set_wheels_rotation(3, vitesse)
        self.robot.reset_wheels_angles()

    def update(self):
        """
            Met à jour la robot, et mesure la distance parcourue
        """
        if self.advancing:
            self.robot.update()
            d = max(abs(self.robot.get_wheels_rotations(1)), abs(self.robot.get_wheels_rotations(2))) * \
                max(self.robot.rd.diametre, self.robot.rg.diametre) * PAS_TEMPS * (pi / 180)
            self.distance += d

            if self.distance > self.distance_max:
                self.advancing = False
                # print("Done advancing ", self.distance, " meters")
                DeplacementDroit.abort(self)

    def abort(self):
        """
            Désactive la mise à jour
        """
        self.advancing = False

    def stop(self):
        """
            Indique si on est au milieu d'un mouvement
        """
        return not self.advancing

    def reset(self):
        """
            Désactive la mise à jour, et réinitialise les variables du mouvement
        """
        DeplacementDroit.abort(self)
        self.distance_max = None
        self.distance = 0
        self.posDepart = None

    @staticmethod
    def hook(dct):
        res = RobotMotorise.hook(dct)
        if res is not None:
                return res
        if dct["__class__"] == DeplacementDroit.__name__:
            return DeplacementDroit(**dct)

    @staticmethod
    def load(filename):
        """
            Permet de charger un objet DeplacementDroit à partir d'un fichier au format json adapté

        :param filename:

        """
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f, object_hook=DeplacementDroit.hook)


class DeplacementDroitAmeliore(DeplacementDroit):
    """
        Permet de réaliser un déplacement rectiligne sur un robot, et de vérifier qu'il n'y à pas d'obstacle
        pendant le déplacement
    """
    INIT = {'proximite_max': 1.0, 'last_detected': None}
    ARGS = ["robot", "arene"]
    KEYS = DeplacementDroit.KEYS + ["last_detected","proximite_max", "arene"]

    def __init__(self, **kwargs):
        """
            Initialise la stratégie

            Pour détecter les obstacles, il est nécessaire d'entrer une arène en argument, qui sera analysée par
            le capteur infrarouge du robot
        :param proximite_max: Procimité limite à laquelle on tolère la présence d'un obstacle en mètres
        :param last_detected: Distance à laquelle le dernier obstacle rencontré a été évalué en mètres
        """
        keys = kwargs.keys()
        for arg in DeplacementDroitAmeliore.ARGS:
            if not arg in keys:
                raise NameError("{} not defined".format(arg))

        for key in DeplacementDroitAmeliore.INIT.keys():
            if not key in keys:
                kwargs[key] = DeplacementDroitAmeliore.INIT[key]

        # robot, distance_max, arene, proximite_max=None, advancing=True, distance=0, posDepart:Point=None, last_detected = None
        DeplacementDroit.__init__(self, **{key : kwargs[key] for key in DeplacementDroit.KEYS if key in kwargs.keys()})
        self.arene = kwargs["arene"]
        self.proximite_max = kwargs["proximite_max"]
        self.last_detected = kwargs["last_detected"]

    def __dict__(self):
        dct = OrderedDict()
        dct["__class__"] = DeplacementDroitAmeliore.__name__
        for key in DeplacementDroitAmeliore.KEYS:
            try:
                dct[key] = self.__getattribute__(key).__dict__()
            except:
                dct[key] = self.__getattribute__(key)
        return dct

    def update(self):
        """
            Met à jour les actions à réaliser

            Si on est au milieu d'un mouvement, on vérifie qu'il n'y à pas d'obstacle trop près
            Si c'est le cas, on s'arrềte. Sinon on avance
        """
        if self.advancing:
            res = self.robot.tete.sensors["ir"].get_mesure(self.arene, ignore=self.robot)
            if res > -1:
                if res < self.proximite_max:
                    # print("Obstacle ahead detected ( ", res, " meters )")
                    DeplacementDroit.abort(self)
            self.last_detected = res
        DeplacementDroit.update(self)

    @staticmethod
    def hook(dct):
        res = RobotTarget.hook(dct)
        if res is not None:
            return res
        elif dct["__class__"] == DeplacementDroitAmeliore.__name__:
            return DeplacementDroitAmeliore(**dct)

    @staticmethod
    def load(filename):
        """
            Permet de charger un DeplacementDroitAmeliore depuis un fichier au format json adapté

        :param filename: Nom du fichier

        """
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f, object_hook=DeplacementDroitAmeliore.hook)

    def __str__(self):
        return DeplacementDroit.__str__(self)+"; last_detected: {}".format(self.last_detected)


class DDroitAmelioreVision(DeplacementDroitAmeliore, StrategieVision):
    def __init__(self, robot, distance, arene):
        StrategieVision.__init__(self, robot, arene)
        DeplacementDroitAmeliore.__init__(self, robot=robot, distance_max=distance, arene=arene)


if __name__ == '__main__':
    from gl_lib.sim.robot import RobotMotorise, Tete
    from gl_lib.sim.geometry import *
    from gl_lib.sim.robot.strategy.deplacement import DeplacementDroitAmeliore
    from gl_lib.sim import Simulation

    v = Vecteur(1, 1, 0).norm()
    p = Pave(1, 1, 0)
    p.move(v * 3)
    p.rotate(-pi / 4)

    r = RobotMotorise(direction=v.clone())
    a = Arene()
    a.add(p)
    # a.add(r)

    strat = DeplacementDroit(robot=r, distance_max=3)
    s = Simulation(strategies=[strat])
    s.start()
