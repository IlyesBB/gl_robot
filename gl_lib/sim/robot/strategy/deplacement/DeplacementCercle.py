# -*- coding: utf-8 -*-
import json
from collections import OrderedDict
from threading import Thread
from time import sleep

import pyglet

from gl_lib.config import PAS_TEMPS
from gl_lib.sim.robot import RobotMotorise
from gl_lib.sim.robot.strategy.deplacement import StrategieDeplacement
from math import pi, cos, sin
from gl_lib.sim.geometry import fonctions


class DeplacementCercle(StrategieDeplacement):
    """
        Dirige le robot pour dessiner un cercle, approximé par un polygone dont tous les points sont sur ce cercle

        Le robot commence à dessiner le cercle dans le sens de sa direction
    """
    KEYS = StrategieDeplacement.KEYS + ["turning", "rot_angle", "sens", "angle_max", "diametre"]
    INIT = {"turning": False, "rot_angle": 0, "sens": None, "angle_max": None, "diametre": None}

    def __init__(self, **kwargs):
        """
            Initialise les attributs gérant la rotation

            Si un angle et un diamètre son donnés en argument, le mouvement est lancé
        :param robot: Robot à déplacer
        :type robot: RobotMotorise
        :param angle_max: Angle duquel se déplacer sur le cercle
        :param diametre: Diamètre du cercle en mètres
        :param vitesse: Vitesse en degrés par seconde
        """
        keys = kwargs.keys()
        StrategieDeplacement.__init__(self, **{key: kwargs[key] for key in StrategieDeplacement.KEYS if key in keys})

        for key in DeplacementCercle.INIT.keys():
            if not key in keys:
                kwargs[key] = DeplacementCercle.INIT[key]
        # A True, la rotation est en cours. False sinon
        self.turning = kwargs["turning"]
        # Angle tourné depuis le début de la rotation
        self.rot_angle = kwargs["rot_angle"]
        # Sens actuel (positif: gauche, négatif: droite - par rapport à la direction du robot)
        self.sens = kwargs["sens"]
        self.diametre = kwargs["diametre"]
        self.angle_max = kwargs["angle_max"]

        if self.angle_max is not None and self.diametre is not None:
            self.sens = fonctions.signe(self.angle_max)
            if "vitesse" in kwargs.keys():
                DeplacementCercle.init_movement(self, self.angle_max, self.diametre, kwargs["vitesse"])
            else:
                DeplacementCercle.init_movement(self, self.angle_max, self.diametre, 100)

    def __dict__(self):
        dct = OrderedDict()
        dct["__class__"] = DeplacementCercle.__name__
        for key in DeplacementCercle.KEYS:
            try:
                dct[key] = self.__getattribute__(key).__dict__()
            except:
                dct[key] = self.__getattribute__(key)
        return dct

    def __str__(self):
        s = StrategieDeplacement.__str__(self) + "\n"
        return s + "-turning: {}; rot_angle: {}; angle_max:".format(self.turning, self.rot_angle, self.angle_max)

    def init_movement(self, angle_max, diametre_cercle=1, dps_moy=30):
        """ Initilise la trajectoire circulaire

            On Initialise les vitesses en résolvant un système à deux équations, du fait qu'on connaît le diamètre,
            et le périmètre du cercle (approché) qu'on dessine selon les vitesses

        :param angle_max: Angle de rotation à atteindre
        :type angle_max: float
        :param diametre_cercle: Diamètre du cercle décrit par la trajectoire
        :type diametre_cercle: float
        :param dps_moy: Vitesse maximale des roues en degrés par seconde
        :type dps_moy: float

        """
        if angle_max is None:
            return
        self.angle_max = abs(angle_max)
        self.rot_angle = 0
        self.turning = True
        diametre = diametre_cercle / 0.90199
        # L'approximation du mouvement induit un écart presque constant entre le diamètre dessiné et le diamètre voulu
        # 0.90199 est le facteur trouvé pour une dizaine de diamètres

        vitesse = abs(dps_moy) * self.robot.rd.diametre
        sens = fonctions.signe(angle_max)

        vd = 2 * vitesse / self.robot.rd.diametre
        vg = (1 - (2 * self.robot.rd.diametre / diametre)) * vd
        if sens > 0:
            aux = vg
            vg = vd
            vd = aux

        self.robot.set_wheels_rotation(1, vd)
        self.robot.set_wheels_rotation(2, vg)

    def update(self):
        """
            Actualise le mouvement de rotation s'il y en a un

            Si on est au milieu d'une rotation, on actualise la position du robot
            Si on a atteint l'angle maximum de rotation, on arrête la rotation
        """
        if self.turning is True:
            self.robot.update()
            dps_wheels = self.robot.get_wheels_rotations(3)
            vitesse_rot = abs(dps_wheels[0] - dps_wheels[1]) * (pi / 180)
            self.rot_angle += vitesse_rot * PAS_TEMPS * (self.robot.rd.diametre / self.robot.dist_wheels)

            if self.rot_angle > (self.angle_max * pi / 180):
                # print("Done turning ", self.sens*self.angle_max, "degrees")
                DeplacementCercle.abort(self)
                self.robot.set_wheels_rotation(3, 0)

    def stop(self):
        """
            Indique si la stratégie a fini son action

        :return: bool

        """
        try:
            return self.rot_angle > (self.angle_max * pi / 180)
        except:
            return False

    def abort(self):
        """
            Désative la mise à jour des actions
        """
        self.turning = False
        self.sens = None

    def reset(self):
        """
            Désactive la mise à jour, et réinitialise l'angle de rotation
        """
        DeplacementCercle.abort(self)
        self.rot_angle = 0
        self.angle_max = None
        self.diametre = None

    @staticmethod
    def hook(dct):
        res = StrategieDeplacement.hook(dct)
        if res is not None:
            return res
        elif dct["__class__"] == DeplacementCercle.__name__:
            return DeplacementCercle(**dct)

    @staticmethod
    def load(filename):
        """
            Permet de charger un objet DeplacementCercle depuis un fichier au format json adapté

        :param filename: Nom du fichier

        """
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f, object_hook=DeplacementCercle.hook)


if __name__ == '__main__':
    from gl_lib.sim import Simulation
    from gl_lib.sim.display.d2.gui import AppAreneThread
    from gl_lib.sim.robot import *
    from gl_lib.sim.robot.sensor import Accelerometre
    from gl_lib.sim.geometry import *

    a = AreneRobot()
    r = RobotMotorise(forme=Pave(centre=Point(3.7, 6.7, 0), width=1, height=1, length=1))
    r.tete.sensors["cam"].arene = AreneFermee(3, 3, 3)
    td = Thread(target=r.tete.sensors["cam"].run)
    sim = Simulation(strategies=[DeplacementCercle(robot=r, angle_max=360, diametre=1)])
    a.add(r)
    app = AppAreneThread(a)
    app.start()
    min_x, min_y = sim.strategie.robot.centre.x, sim.strategie.robot.centre.y
    max_x, max_y = sim.strategie.robot.centre.x, sim.strategie.robot.centre.y
    dps_wheels = sim.strategie.robot.get_wheels_rotations(3)
    # td.start()
    sim.start()
    # print(sim.stop, sim.strategie.stop())
    while not sim.stop:
        sleep(1)
        print(sim.cpt, sim.strategie.robot.get_wheels_rotations(3))
        if sim.strategie.robot.centre.x < min_x:
            min_x = sim.strategie.robot.centre.x
        if sim.strategie.robot.centre.x > max_x:
            max_x = sim.strategie.robot.centre.x
        if sim.strategie.robot.centre.y < min_y:
            min_y = sim.strategie.robot.centre.y
        if sim.strategie.robot.centre.y > max_y:
            max_y = sim.strategie.robot.centre.y

    d_rot = abs(dps_wheels[0] - dps_wheels[1]) * PAS_TEMPS * (pi / 180)
    max_rot = max(dps_wheels[0], dps_wheels[1]) * PAS_TEMPS * (pi / 180)
    d_dist = max_rot * (sim.strategie.robot.rd.diametre / 2)
    n = (2 * pi) / d_rot
    gr_diametre = n * d_dist / (2 * pi)
    app.stop()
    # pyglet.app.exit()

    print(abs(max_x - min_x), abs(max_y - min_y))

    # sim.strategie.save("deplacementcercle.json")

    strat2 = DeplacementCercle.load("deplacementcercle.json")
    print(strat2.clone())
