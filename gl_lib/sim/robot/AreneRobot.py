from gl_lib.sim.robot import *
from gl_lib.sim.geometry import *

class AreneRobot(Arene):

    @staticmethod
    def deserialize(dct):
        res = Robot.deserialize(dct)
        if res is not None:
            return res
        elif dct["__class__"] == RobotMotorise:
            return RobotMotorise.deserialize(dct)
        elif dct["__class__"] == RobotTarget:
            return RobotTarget.deserialize(dct)

