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
    """Fais avancer un robot en argument sur une certaine distance
    """
    advancing = ...  # type: bool
    posDepart = ...  # type: Point
    INIT = {'advancing': True, 'distance': 0.0, 'distance_max': 1.0, 'vitesse': 60, 'posDepart': None}

    def __init__(self, **kwargs):
        """Prend en argument obligatoire un robot. Par défaut, la classe commande le robot pour avancer sur un mètre
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

    def __dict__(self):
        dct = OrderedDict()
        dct["__class__"] = DeplacementDroit.__name__
        dct["robot"] = self.robot.__dict__()
        dct["advancing"] = self.advancing
        dct["distance"] = self.distance
        dct["distance_max"] = self.distance_max
        dct["posDepart"] = self.posDepart.__dict__() if self.posDepart is not None else None
        return dct

    @staticmethod
    def hook(dct):
        res = RobotMotorise.hook(dct)
        if res is not None:
                return res
        if dct["__class__"] == DeplacementDroit.__name__:
            return DeplacementDroit(**dct)

    @staticmethod
    def load(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f, object_hook=DeplacementDroit.hook)

    def init_movement(self, distance_max, vitesse):
        self.advancing = True  # Booléen indiquant si le robot est en marche
        self.distance = 0
        self.distance_max = distance_max
        self.posDepart = self.robot.forme.centre.clone()
        self.robot.set_wheels_rotation(3, vitesse)
        self.robot.reset_wheels_angles()

    def update(self):
        """
        Met à jour la robot, et mesure la distance parcourue
        :return:
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
        self.advancing = False
        self.distance_max = 0
        self.distance = 0
        self.robot.reset_wheels_angles()

    def stop(self):
        return not self.advancing

    def clone(self):
        d = self.__dict__()
        return DeplacementDroit.hook(d)


class DeplacementDroitAmeliore(DeplacementDroit):
    INIT = {'proximite_max': 1.0, 'last_detected': None}
    ARGS = ["robot", "arene"]

    def __init__(self, **kwargs):
        keys = kwargs.keys()
        for arg in DeplacementDroitAmeliore.ARGS:
            if not arg in keys:
                raise NameError("{} not defined".format(arg))

        for key in DeplacementDroitAmeliore.INIT.keys():
            if not key in keys:
                kwargs[key] = DeplacementDroitAmeliore.INIT[key]

        # robot, distance_max, arene, proximite_max=None, advancing=True, distance=0, posDepart:Point=None, last_detected = None
        DeplacementDroit.__init__(self, **kwargs)
        self.arene = kwargs["arene"]
        self.proximite_max = kwargs["proximite_max"]
        self.last_detected = kwargs["last_detected"]

    def update(self):
        if self.advancing:
            res = self.robot.tete.lcapteurs[Tete.IR].get_mesure(self.arene, ignore=self.robot)
            if res > -1:
                if res < self.proximite_max:
                    # print("Obstacle ahead detected ( ", res, " meters )")
                    DeplacementDroit.abort(self)
            self.last_detected = res
        DeplacementDroit.update(self)

    def __dict__(self):
        dct = OrderedDict()
        dct["__class__"] = DeplacementDroitAmeliore.__name__
        dct["robot"] = self.robot.__dict__()
        dct["arene"] = self.arene.__dict__()

        dct["advancing"] = self.advancing
        dct["distance"] = self.distance
        dct["distance_max"] = self.distance_max
        dct["posDepart"] = self.posDepart.__dict__() if self.posDepart is not None else None

        dct["proximite_max"] = self.proximite_max
        dct["last_detected"] = self.last_detected

        return dct

    @staticmethod
    def hook(dct):
        res = RobotTarget.hook(dct)
        if res is not None:
            return res
        elif dct["__class__"] == DeplacementDroitAmeliore.__name__:
            return DeplacementDroitAmeliore(**dct)

    @staticmethod
    def load(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f, object_hook=DeplacementDroitAmeliore.hook)

    def clone(self):
        return DeplacementDroitAmeliore(**self.__dict__())

    def dict(self):
        dda = DeplacementDroitAmeliore.clone(self)
        return dda.__dict__()


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
    s = Simulation(strat)
    # s.start()
    while not s.stop:
        pass

    dda = DeplacementDroit(robot=RobotMotorise())
    d = dda.__dict__()
    dda.save("deplacement_droit.json")

    dda2 = DeplacementDroit.load("deplacement_droit.json")

    print(dda2)


