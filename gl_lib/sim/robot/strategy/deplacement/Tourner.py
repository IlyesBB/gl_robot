# -*- coding: utf-8 -*-
import json
from collections import OrderedDict

from gl_lib.sim.geometry import fonctions
from gl_lib.sim.robot.strategy.deplacement import StrategieDeplacement, DeplacementCercle
from gl_lib.sim.geometry.fonctions import signe
from gl_lib.config import PAS_TEMPS
from gl_lib.sim.robot import Tete, RobotMotorise
from math import pi
from time import sleep


class Tourner(DeplacementCercle):
    """
    Fais décrire au robot un carré de coté 70 cm
    """
    KEYS = DeplacementCercle.KEYS
    INIT = DeplacementCercle.INIT
    def __init__(self, **kwargs):
        """

        :param robot:
        """
        DeplacementCercle.__init__(self, **kwargs)
        self.diametre = self.robot.dist_wheels

        kwargs["diametre"] = self.robot.forme.get_length()
        if self.angle_max is not None:
            self.sens = fonctions.signe(self.angle_max)
            if "vitesse" in kwargs.keys():
                DeplacementCercle.init_movement(self,self.angle_max, self.diametre,kwargs["vitesse"])
            else:
                DeplacementCercle.init_movement(self,self.angle_max, self.diametre,100)


if __name__ == '__main__':
    st.save("tourner.json")

    st2 = Tourner.load("tourner.json")
    print(st2)
