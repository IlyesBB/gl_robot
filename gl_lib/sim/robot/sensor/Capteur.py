# -*- coding: utf-8 -*-
import json
from collections import OrderedDict

from gl_lib.sim.geometry import *

class Capteur(Objet3D):
    """
        Classe abstraite

        La positione et la direction du capteur sont liées a celles de la tête s'il y en a une
    """

    def __init__(self, centre:Point=Point(0, 0, 0), direction:Vecteur=Vecteur(1, 0, 0)):
        Objet3D.__init__(self, centre)
        self.direction = direction

    def __dict__(self):
        dct = OrderedDict()
        dct["__class__"] = Capteur.__name__
        dct["centre"] = self.centre.__dict__() if self.centre is not None else None
        dct["direction"] = self.direction.__dict__() if self.direction is not None else None
        return dct

    @staticmethod
    def hook(dct):
        if dct["__class__"] == Point.__name__:
            return Point.hook(dct)
        elif dct["__class__"] == Vecteur.__name__:
            return Vecteur.hook(dct)
        elif dct["__class__"] == Capteur.__name__:
            return Capteur(centre=dct["centre"], direction=dct["direction"])
        return dct

    @staticmethod
    def load(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f, object_hook=Capteur.hook)

    def update(self):
        """
            Fonction destinée à être appelée touts les PAS_TEMPS (gl_lib.config)
        """
        pass

    def rotate(self, teta, axis=None):
        """
            Tourne la direction du capteur

        :param teta: Angle en radians
        :type teta: float
        :param axis: 'x', 'y' ou 'z'

        """
        self.direction.rotate(teta, axis)

    def rotate_around(self, point, teta, axis=None):
        """
            Tourne le centre du capteur autour d'un point

        :param point: Point autour duquel tourner
        :type point: Point
        :param teta: Angle en radians
        :type teta: float
        :param axis: 'x', 'y' ou 'z'

        """
        self.centre.rotate_around(point, teta, axis)

    def rotate_all_around(self, point, teta, axis=None):
        """
            Tourne le centre du capteur aucour du pointen plus de tourner la direction

        :param point: Point autour duquel tourner
        :type point: Point
        :param teta: Angle en radians
        :type teta: float
        :param axis: 'x', 'y' ou 'z'

        """
        self.rotate_around(point, teta, axis)
        self.rotate(teta, axis)

    def move(self, vector):
        """
            Déplace le capteur

        :param vector: Vecteur de déplacement
        :type vector: Vecteur

        """
        self.centre.move(vector)

    def attach(self, position, direction):
        """
            Permet de lier le centre et la direction du capteur à un couple (position, direction)

        :param position: Position que va référencer le centre du capteur
        :type position: Point
        :param direction: Direction que va référencer la direction du capteur
        :type direction: Vecteur

        """
        self.centre = position
        self.direction = direction