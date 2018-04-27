# -*- coding: utf-8 -*-
import json
from collections import OrderedDict

from gl_lib.sim.robot import RobotMotorise, Roue, Tete
from gl_lib.sim.geometry import *


class RobotTarget(RobotMotorise, PaveTarget):
    """
        Robot destiné à avoir une balise accorchée sur lui
    """

    def __init__(self, forme=Pave(1, 1, 1), rg=Roue(0.25), rd=Roue(0.25), direction=Vecteur(1, 1, 0).norm(),
                 tete: Tete = Tete(), balise=None):
        """

        :param balise: Contient les couleurs à afficher

        """
        RobotMotorise.__init__(self, forme=forme, rg=rg, rd=rd, direction=direction, tete=tete)
        self.balise = balise

    def get_face(self):
        return 1

    def __dict__(self):
        dct = OrderedDict()
        dct["__class__"] = RobotTarget.__name__
        dct["direction"] = self.direction.__dict__()
        dct["tete"] = self.tete.__dict__() if self.tete is not None else None
        dct["balise"] = self.balise.__dict__() if self.balise is not None else None
        dct["forme"] = self.forme.__dict__()
        dct["dist_wheels"] = self.dist_wheels
        dct["rg"] = self.rg.__dict__()
        dct["rd"] = self.rd.__dict__()
        return dct

    def get_target(self):
        return self.balise

    @staticmethod
    def hook(dct):
        res = RobotMotorise.hook(dct)
        if res is not None:
            return res
        elif dct["__class__"] == RobotTarget.__name__:
            return RobotTarget(dct["forme"], dct["rg"], dct["rd"], dct["direction"], dct["tete"], dct["balise"])

    @staticmethod
    def load(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f, object_hook=RobotTarget.hook)

    def clone(self):
        return RobotTarget(self.forme.clone(), self.rg.clone(), self.rd.clone(), self.direction.clone(),
                           self.tete.clone(),
                           self.balise.clone())
