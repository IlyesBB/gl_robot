# -*- coding: utf-8 -*-
import json
from _thread import RLock
from collections import OrderedDict

from gl_lib.sim.robot import *
from gl_lib.sim.geometry import *
from gl_lib.config import PAS_TEMPS
from math import pi


class RobotMotorise(Robot):
    """
        Robot dont on commande les moteurs des roues, auquel on attache une tête
    """
    PAS_MAX = 0.01
    KEYS = Robot.KEYS + ["tete", "dist_wheels"]
    INIT = {"rg":Roue(), "rd":Roue(), "tete":Tete()}

    def __init__(self, **kwargs):
        """
            Initialise un robot dont les roues sont "motorisées" et la tête est intialisée pour suivre les
            mouvement du robot

        :param tete: Objet contenant les capteurs du robot
        :type tete: Tete
        :param rg: Roue gauche
        :type rg: Roue
        :param rd: Roue droite
        :type rd: Roue
        :param dist_wheels: Distance entre les centres des roues. Si non initialisé, est calculé
        :type dist_wheels: float

        """
        keys = kwargs.keys()
        for key in RobotMotorise.INIT.keys():
            if not key in keys:
                kwargs[key] = RobotMotorise.INIT[key]
        Robot.__init__(self,**{key:kwargs[key] for key in keys if key in Robot.KEYS})
        self.tete = kwargs["tete"]
        self.tete.dir_robot = self.direction
        self.tete.centre = self.centre
        self.dist_wheels = (self.rd.centre - self.rg.centre).to_vect().get_mag()

        self.set_wheels_rotation(3, 0)

    def __dict__(self):
        dct = OrderedDict()
        dct["__class__"] = RobotMotorise.__name__
        dct["direction"] = self.direction.__dict__()
        dct["tete"] = self.tete.__dict__() if self.tete is not None else None
        dct["forme"] = self.forme.__dict__()
        dct["dist_wheels"] = self.dist_wheels
        dct["rg"] = self.rg.__dict__()
        dct["rd"] = self.rd.__dict__()
        return dct

    def __str__(self):
        """
            Affiche les caractéristiques essentielles du robot et de sa tête
        """
        r_str = Robot.__str__(self)
        s = r_str + "\n-tete:" + str(self.tete)
        return s

    def __eq__(self, other):
        if not Robot.__eq__(self, other):
            return False
        if self.tete != other.tete:
            return False
        if self.dist_wheels != other.dist_wheels:
            return False
        return True

    def set_wheels_rotation(self, port, dps):
        """
            Change la vitesse des roues

        :param port: 1 pour roue gauche, 2 pour roue droite, sommer pour accéder au deux
        :param dps: vitesse de rotation en degrés par seconde

        """
        if port == 1:
            self.rd.vitesseRot = dps
        elif port == 2:
            self.rg.vitesseRot = dps
        elif port == 3:
            self.rd.vitesseRot = dps
            self.rg.vitesseRot = dps

    def get_wheels_rotations(self, port):
        """
            Renvoie les vitesses des roues

        :param port: 1 pour roue gauche, 2 pour roue droite, sommer pour accéder au deux
        :return: Peut renvoyer un tuple ou un flottant, selon le port choisi

        """
        if port == 1:
            return self.rd.vitesseRot
        elif port == 2:
            return self.rg.vitesseRot
        elif port == 3:
            return self.rd.vitesseRot, self.rg.vitesseRot

    def get_wheels_angles(self, port):
        """
            Renvoie l'angle des roues

        :param port: 1 pour roue gauche, 2 pour roue droite, sommer pour accéder au deux
        :return: Peut renvoyer un tuple ou un flottant, selon le port choisi

        """
        if port == 1:
            return self.rg.angle
        elif port == 2:
            return self.rd.angle
        elif port == 3:
            return self.rd.angle, self.rg.angle

    def reset_wheels_angles(self):
        """
            Réinitialise l'angle des roues
        """
        self.rg.angle = 0
        self.rd.angle = 0

    def update(self):
        """
            Met à jour la tête et la position du robot
        """
        self.update_pos()
        self.tete.update()

    def update_pos(self):
        """
            Met à jour la position du robot en fonction de la vitesse de rotation des roues

            On approxime le mouvement du robot par une succession de rotation et de mouvement rectilignes

            Pour les mouvement rectilignes:
            On considère que la rotation effective des roues dans la direction du robot est égale au maximum des
            rotations des roues.

            Pour les rotations:
            On considère que le robot tourne de la différence des rotation des roues

            Conséquences sur la trajectoire
            Le robot tourne autour d'un cercle (approximé) tangent à sa direction, dont le rayon dépend de la
            différence de rotation des roues

            TODO: Vérifier que la méthode fonctionne pour des vitesse de rotation négatives
        """
        # pas: float (représente la pas de temps)
        # angle_d, angle_g: float (angle de rotation de chaque roue pour cette mise à jour)
        pas = PAS_TEMPS
        angle_g = self.rg.vitesseRot * pas
        angle_d = self.rd.vitesseRot * pas
        # d_rot: float (la différence)
        d_rot = (self.rg.vitesseRot - self.rd.vitesseRot) * pas

        if d_rot == 0.0:
            # Dans ce cas, c'est un déplacement simple
            v = self.direction * (angle_d * self.rd.diametre * (pi / 180))
            self.move(v)
        else:
            # diffs: tuple[float] (contient les angles de rotation du robot par rapport à son centre
            diffs = (angle_d * (pi / 180) * (self.rd.diametre / self.dist_wheels),
                     angle_g * (pi / 180) * (self.rg.diametre / self.dist_wheels))

            # Angles dans le sens trigonométriques
            # négatif pour la roue droite, positif pour la roue gauche
            # v: Vecteur (celui dont le robot va avancer)
            if angle_d >= 0.0 and angle_g >= 0.0:
                v = self.direction * ((abs(angle_g - angle_d) + min(abs(angle_g), abs(angle_d))) *
                                      min(self.rd.diametre, self.rg.diametre) * (1 / 2.0) * (pi / 180))
            elif angle_d <= 0.0 and angle_g <= 0.0:
                v = self.direction * (-(abs(angle_g - angle_d) + min(abs(angle_g), abs(angle_d))) *
                                      min(self.rd.diametre, self.rg.diametre) * (1 / 2.0) * (pi / 180))
            else:
                # Cas non gérés
                v = Vecteur(0, 0, 0)

            self.move(v)
            self.direction.rotate(-diffs[0] + diffs[1])
            self.forme.rotate_all_around(self.centre, -diffs[0] + diffs[1])

        self.rg.angle += angle_g
        self.rd.angle += angle_d

    @staticmethod
    def hook(dct):
        res = Tete.hook(dct)
        if res is not None:
            return res
        elif dct["__class__"] == Roue.__name__:
            return Roue.hook(dct)
        elif dct["__class__"] == Pave.__name__:
            return Pave.hook(dct)
        elif dct["__class__"] == RobotMotorise.__name__:
            return RobotMotorise(**dct)

    @staticmethod
    def load(filename):
        """
            Permet de charger un objet RobotMotorise au format json
        :param filename: Nom du fichier

        """
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f, object_hook=RobotMotorise.hook)



if __name__ == '__main__':
    r = RobotMotorise(forme=Pave(1,1,1, Point(50,50,10)))
    print(repr(r.forme), repr(r.tete))
    r.set_wheels_rotation(3,60)
    n=20
    for i in range(n):
        r.update()
    print(r.centre, r.tete.centre)