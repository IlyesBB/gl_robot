# -*- coding: utf-8 -*-
from gl_lib.sim.geometry import Objet3D, Vecteur, Point, Pave, ApproximableAPave
from gl_lib.config import PAS_TEMPS
from math import pi, sqrt


class Robot(Objet3D, ApproximableAPave):
    """
    Classe definissant les elements essentiels d'un robot
    """
    KEY = ["direction", "pave", "rg", "rd"]

    def __init__(self, pave: Pave = Pave(1, 1, 1, Point(0, 0, 0)), rg: Objet3D = Objet3D(), rd: Objet3D = Objet3D(),
                 direction: Vecteur = Vecteur(0, 1, 0)):
        """
            Initialise les attributs, et place les roues par rapport à la direction

            On place les roues de part et d'autre de la direction, à 45°
        :param pave: Forme du robot
        :param rg: Roue droite
        :param rd: Roue gauche
        :param direction: direction du robot
        """
        Objet3D.__init__(self)
        self.direction = direction
        self.forme = pave
        self.forme.rotate(self.direction.get_angle())
        self.centre = pave.centre  # initalise le centre au centre du pave
        self.rd = rd
        self.rg = rg

        # initialisation des centres des roues
        self.rd.centre = self.centre + (self.direction.rotate(-pi / 4) * self.forme.width * sqrt(2) / 2)
        self.rg.centre = self.centre + (self.direction.rotate(pi / 4) * self.forme.width * sqrt(2) / 2)

        self.dist_wheels = self.forme.width

    def __str__(self):
        s = "({}; direction: {}; forme: {})".format(self.__class__.__name__, self.direction, self.forme)
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

    def rotate_around(self, point: Point, angle: float, axis=None):
        """
            Tourne le robot autour de point d'un angle angle en radians
        """
        self.forme.rotate_around(point, angle, axis)
        self.rd.rotate_around(point, angle, axis)
        self.rg.rotate_around(point, angle, axis)

    def rotate_all_around(self, point: Point, angle: float, axis=None):
        """
            Tourne le Robot et sa direction par rapport à son centre, et autour de point d'un angle en radians
        """
        Objet3D.rotate_around(self, point, angle, axis)
        self.forme.rotate_all_around(point, angle, axis)
        self.rg.rotate_around(point, angle, axis)
        self.rd.rotate_around(point, angle, axis)
        self.direction.rotate(angle, axis)

    def move(self, vecteur: Vecteur):
        """
            Déplace les composants du robot
        """
        self.forme.move(vecteur)
        self.rg.move(vecteur)
        self.rd.move(vecteur)

    def clone(self):
        return Robot(self.forme.clone(), self.rd.clone(), self.rg.clone(), self.direction.clone())

    def get_pave(self):
        return self.forme.get_pave()