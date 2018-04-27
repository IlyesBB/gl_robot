# -*- coding: utf-8 -*-
import json
import os
from collections import OrderedDict

from gl_lib.sim.robot import RobotMotorise, Tete, RobotTarget
from gl_lib.sim.robot.sensor import Accelerometre, CapteurIR
from gl_lib.sim.robot.sensor.camera import Camera
from gl_lib.utils import Serializable


class Strategie(Serializable):
    """
    définit une strategie de robot de facon abstraite
    """
    ARGS = ["robot"]
    KEYS = ["robot"]
    INIT = {"robot": None}

    def __init__(self, robot):
        """
            Initialise l'attribut robot de la stratégie

            Une stratégie est suposée toujours appliquée à un robot
        :param robot: Robot sur lequel la stratégie agit
        :type robot: RobotMotorise
        """
        self.robot = robot
        if robot is None:
            raise NameError("{} not defined".format(robot))

    def __repr__(self):
        s = ""
        d = self.__dict__()
        for k in d.keys():
            if isinstance(d[k], list) and len(d[k]) > 0:
                s += k + " :\n"
                for i in range(len(d[k])):
                    s += "\t" + repr(d[k][i]) + "\n"
            else:
                s += k + " : " + repr(d[k]) + "\n"
        return s

    def __str__(self):
        return "{};\n-robot: {}".format(self.__class__.__name__, self.robot)

    def stop(self):
        """
            Toutes les stratégies sont supposées avoir une telle méthode, indiquant si elle ont besoin d'être mises
            à jour ou non

            Cette information est à destination de toute boucle qui ferait avancer la stratégie dans le temps
            Ici, elle ne s'arrête jamais
        """
        return False

    def update(self):
        """
            Méthode à redéfinir dans les classes filles

            Réalise les actions sur le robot pour un intervalle de temps

            Cet intervalle est une constante, PAS_TEMPS, définie dans gl_lib.config
        """
        pass

    def __dict__(self):
        dct = OrderedDict()
        dct["__class__"] = Strategie.__name__
        dct["robot"] = self.robot.__dict__()
        return dct

    @staticmethod
    def hook(dct):
        res = RobotMotorise.hook(dct)
        if res is not None:
            return res
        elif dct["__class__"] == RobotTarget.__name__:
            return RobotTarget.hook(dct)
        elif dct["__class__"] == Strategie.__name__:
            return Strategie(dct["robot"])

    @staticmethod
    def load(filename):
        """
            Permet de charger une Strategie à partir d'un fichier json
        """
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f, object_hook=Strategie.hook)


if __name__ == '__main__':
    s = Strategie(RobotMotorise())
    s.save("strategie.json")
    s2 = Strategie.load("strategie.json")
    print(s2)
