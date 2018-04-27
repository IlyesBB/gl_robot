# -*- coding: utf-8 -*-
import json
from collections import OrderedDict

from gl_lib.sim.geometry import Objet3D, Vecteur, Point, Pave, ApproximableAPave
from gl_lib.config import PAS_TEMPS
from math import pi, sqrt

from gl_lib.sim.robot import Roue


class Robot(Objet3D, ApproximableAPave):
    """
    Classe definissant les elements essentiels d'un robot
    """
    KEYS = ["direction", "forme", "rg", "rd"]
    INIT = {"direction":Vecteur(0,1,0), "forme":Pave(1,1,1,Point(0,0,0)), "rg":Objet3D(), "rd":Objet3D()}

    def __init__(self, **kwargs):
        """
            Initialise les attributs, et place les roues par rapport à la direction
            On place les roues de part et d'autre de la direction, à 45°
        :param forme: Forme du robot
        :type forme: Pave
        :param rg: Roue droite, représentée comme un point
        :type rg: Objet3D
        :param rd: Roue gauche, représentée comme un point
        :type rd: Objet3D
        :param direction: Direction du robot
        :type direction: Vecteur
        """
        Objet3D.__init__(self)
        keys = kwargs.keys()
        for key in Robot.INIT.keys():
            if not key in keys:
                kwargs[key] = Robot.INIT[key]

        self.direction = kwargs["direction"]
        self.forme = kwargs["forme"]
        self.rd = kwargs["rd"]
        self.rg = kwargs["rg"]
        self.forme.rotate(self.direction.get_angle())
        self.centre = self.forme.centre  # initalise le centre au centre du pave

        # initialisation des centres des roues
        self.rd.centre = self.centre + (self.direction.rotate(-pi / 4) * self.forme.width * sqrt(2) / 2)
        self.rg.centre = self.centre + (self.direction.rotate(pi / 4) * self.forme.width * sqrt(2) / 2)

        self.dist_wheels = self.forme.width

    def __dict__(self):
        dct = OrderedDict()
        dct["__class__"] = Robot.__name__
        dct["direction"] = self.direction.__dict__()
        dct["forme"] = self.forme.__dict__()
        dct["rg"] = self.rg.__dict__()
        dct["rd"] = self.rd.__dict__()
        return dct


    def __str__(self):
        s = "{}; direction: {}; forme: {}".format(self.__class__.__name__, self.direction, self.forme)
        return s

    def __eq__(self, other):
        if not Objet3D.__eq__(self, other):
            return False
        if other.forme != self.forme:
            return False
        if other.rd != self.rd or other.rg != self.rg:
            return False
        if other.direction != self.direction:
            return False
        if other.dist_wheels != self.dist_wheels:
            return False
        return True

    def rotate_around(self, point, angle, axis=None):
        """
            Tourne le robot autour de point d'un angle angle en radians

        :param point: Point autour duquel tourner
        :type point: Point
        :param teta: Angle en radians
        :type teta: float
        :param axis: 'x', 'y' ou 'z'

        """
        self.forme.rotate_around(point, angle, axis)
        self.rd.rotate_around(point, angle, axis)
        self.rg.rotate_around(point, angle, axis)

    def rotate_all_around(self, point, angle, axis=None):
        """
            Tourne le Robot et sa direction par rapport à son centre, et autour de point d'un angle en radians

        :param point: Point autour duquel tourner
        :type point: Point
        :param teta: Angle en radians
        :type teta: float
        :param axis: 'x', 'y' ou 'z'

        """
        Objet3D.rotate_around(self, point, angle, axis)
        self.forme.rotate_all_around(point, angle, axis)
        self.rg.rotate_around(point, angle, axis)
        self.rd.rotate_around(point, angle, axis)
        self.direction.rotate(angle, axis)

    def move(self, vecteur):
        """
            Déplace les composants du robot

        :param vecteur: Vecteur Déplacement
        :type vecteur: Vecteur

        """
        self.forme.move(vecteur)
        self.rg.move(vecteur)
        self.rd.move(vecteur)

    def get_pave(self):
        return self.forme.get_pave()

    @staticmethod
    def load(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f, object_hook=Robot.hook)

    @staticmethod
    def hook(dct):
        if dct["__class__"] == Vecteur.__name__:
            return Vecteur.hook(dct)
        elif dct["__class__"] == Roue.__name__:
            return Roue.hook(dct)
        elif dct["__class__"] == Pave.__name__:
            return Pave.hook(dct)
        elif dct["__class__"] == Robot.__name__:
            return Robot(**dct)

if __name__ == '__main__':
    r = Robot(forme=Pave(1,1,1, Point(30,30,0)))
    print(r.forme)