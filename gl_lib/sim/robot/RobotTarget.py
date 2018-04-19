import json
from collections import OrderedDict

from gl_lib.sim.robot import RobotMotorise, Roue, Tete
from gl_lib.sim.geometry import *

class RobotTarget(RobotMotorise, PaveTarget):
    """
    Robot destiné à avoir une balise sur le dos
    """
    def __init__(self, pave=Pave(1,1,1),rg=Roue(0.25),rd=Roue(0.25), direction=Vecteur(1,1,0).norm(), tete:Tete=None, balise=None):
        """

        :param balise:
        """
        RobotMotorise.__init__(self, pave, rg, rd, direction, tete)
        self.balise=balise

    def get_face(self):
        return 1

    def get_target(self):
        return self.balise

    def __dict__(self):
        dct = OrderedDict()
        dct["__class__"] = RobotTarget.__name__
        dct["direction"] = self.direction.__dict__()
        dct["tete"] = self.tete.__dict__() if self.tete is not None else None
        dct["balise"] = self.balise.__dict__()
        dct["forme"] = self.forme.__dict__()
        dct["dist_wheels"] = self.dist_wheels
        dct["rg"] = self.rg.__dict__()
        dct["rd"] = self.rd.__dict__()
        return dct

    @staticmethod
    def deserialize(dct):
        res = RobotMotorise.deserialize(dct)
        if res is not None:
            return res
        elif dct["__class__"] == RobotTarget.__name__:
            return RobotTarget(dct["forme"], dct["rg"], dct["rd"], dct["direction"], dct["tete"], dct["balise"] )

    @staticmethod
    def load(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f, object_hook=RobotTarget.deserialize)

    def clone(self):
        return RobotTarget(self.forme.clone(), self.rg.clone(), self.rd.clone(), self.direction.clone(), self.tete.clone(),
                             self.balise.clone())

