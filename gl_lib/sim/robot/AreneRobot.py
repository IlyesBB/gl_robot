import json
from collections import OrderedDict

from gl_lib.sim.robot import *
from gl_lib.sim.geometry import *

class AreneRobot(Arene):

    @staticmethod
    def hook(dct):
        res = RobotMotorise.hook(dct)
        if res is not None:
            return res
        elif dct["__class__"] == RobotTarget:
            return RobotTarget.hook(dct)

    @staticmethod
    def load(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f, object_hook=AreneRobot.hook)


if __name__=='__main__':
    a = AreneRobot()

    a.add(RobotMotorise())

    d = a.__dict__()
    print(a)

    #a2 = AreneRobot.load("arene_robot.json")
    #print(a2)

