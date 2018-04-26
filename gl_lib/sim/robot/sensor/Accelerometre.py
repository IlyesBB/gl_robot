# -*- coding: utf-8 -*-
import json
from collections import OrderedDict

from gl_lib.sim.robot.sensor import Capteur
from gl_lib.sim.geometry import *
from gl_lib.config import PAS_TEMPS


class Accelerometre(Capteur):
    """
        Permet de mesurer la vitesse et l'accélération du robot à un instant donné

        Les données sont mises à jour tous les PAS_TEMPS
        sauf si PAS_TEMPS < DT_MESURE, la durée de la mesure
    """
    DT_MESURE = 0.01
    MAX_CPT = int(DT_MESURE / PAS_TEMPS)

    def __init__(self, centre: Point = Point(0, 0, 0), direction: Vecteur = Vecteur(1, 0, 0), prev_pos: Point = None,
                 speed: Vecteur = Vecteur(0, 0, 0), acc: Vecteur = Vecteur(0, 0, 0)):
        """
            On initialise les variables nécessaires pour calculer une vitesse et une accélération entre deux instants
        """
        Capteur.__init__(self, centre=centre, direction=direction)
        self.prev_pos = prev_pos
        self.prev_pos = Point(0, 0, 0)
        self.speed = speed
        self.acc = acc
        # Compteur pour savoir quand prendre la mesure
        self.cpt = 0
        if prev_pos is None:
            self.prev_pos = self.centre.clone()

    def __dict__(self):
        dct = OrderedDict()
        dct["__class__"] = Accelerometre.__name__
        dct["centre"] = self.centre.__dict__()
        dct["direction"] = self.direction.__dict__()

        dct["prev_pos"] = self.prev_pos.__dict__()
        dct["speed"] = self.speed.__dict__()
        dct["acc"] = self.acc.__dict__()
        dct["cpt"] = self.cpt

        return dct

    def __str__(self):
        s = "({}; sp: {} ; acc: {})".format(self.__class__.__name__, self.speed, self.acc)
        return s

    def get_mesure(self, value: int = 1):
        """
            Retourne la vitesse actuelle, et actualise le dernier point de mesure de la position
            Si value vaut 1 : retourne la dernière vitesse mesurée
            Si value vaut 2: retourne la dernière accélération mesurée
            Sommer pour obtenir les deux
        :return: float ou tuple selon value
        """
        if value == 1:
            return self.speed
        if value == 2:
            return self.acc
        if value == 3:
            return self.speed, self.acc

    def update(self):
        """
            Fonction destinée à être appelée tous les PAS_TEMPS
            Ne met à jour les mesures que si l'accéléromètre est prêt à répondre
            Sinon avance d'une unitée de temps
        """

        if Accelerometre.MAX_CPT < 1 or self.cpt >= Accelerometre.MAX_CPT - 1:
            # Si DT_MESURE < PAS_TEMPS, la mesure est mise à jour dès que possible
            # Ou alors on a attendu assez longtemps
            new_speed = (self.centre - self.prev_pos).to_vect() / PAS_TEMPS
            self.prev_pos = self.centre.clone()
            self.acc = (new_speed - self.speed) / PAS_TEMPS
            self.speed = new_speed

        else:
            # Sinon, on avance d'une unité de temps
            self.cpt += 1

    @staticmethod
    def hook(dct):
        """
            On ne récupère pas la liste d'objest à ignorer
        """
        if dct["__class__"] == Vecteur.__name__:
            return Vecteur.hook(dct)
        if dct["__class__"] == Point.__name__:
            return Point.hook(dct)
        if dct["__class__"] == Accelerometre.__name__:
            return Accelerometre(dct["centre"], dct["direction"], dct["prev_pos"], dct["speed"], dct["acc"])

    @staticmethod
    def load(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f, object_hook=Accelerometre.hook)

    def clone(self):
        p = self.prev_pos.clone() if self.prev_pos is not None else None
        return Accelerometre(self.centre.clone(), self.direction.clone(), p, self.speed.clone(), self.acc.clone())


if __name__ == '__main__':
    a = Accelerometre()

    a.save("accelerometre.json")

    a2 = Accelerometre.load("accelerometre.json")
    print(a2)
