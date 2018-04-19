import json
from collections import OrderedDict

from gl_lib.sim.robot import RobotMotorise, Tete, RobotTarget
from gl_lib.sim.robot.sensor import Accelerometre, CapteurIR
from gl_lib.sim.robot.sensor.camera import Camera
from gl_lib.utils import Serializable


class Strategie(Serializable):
    """
    definit une strategy de robot de facon abstraite
    """

    def __init__(self, robot: RobotMotorise):
        """
        robot : Robot
        """
        self.robot = robot

    def stop(self):
        return False

    def update(self):
        pass

    def __dict__(self):
        dct = OrderedDict()
        dct["__class__"] = self.__class__.__name__
        dct["robot"] = self.robot.__dict__()
        return dct

    @staticmethod
    def deserialize(dct):
        res = RobotMotorise.deserialize(dct)
        if res is not None:
            return res
        elif dct["__class__"] == RobotTarget.__name__:
            return RobotTarget.deserialize(dct)
        elif dct["__class__"] == Strategie.__name__:
            return Strategie(dct["robot"])

    @staticmethod
    def load(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f, object_hook=Strategie.deserialize)

    def __repr__(self):
        """
        """
        s = ""
        d = self.__dict__()
        for k in d.keys():
            if isinstance(d[k], list) and len(d[k]) > 0:
                s += k + " :\n"
                for i in range(len(d[k])):
                    s += "\t" + str(d[k][i]) + "\n"
            else:
                s += k + " : " + str(d[k]) + "\n"
        return s
