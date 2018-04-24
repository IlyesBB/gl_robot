import json
from collections import OrderedDict

from gl_lib.sim.robot.strategy import Strategie
from gl_lib.sim.robot import Tete, AreneRobot, RobotMotorise
from threading import RLock

class StrategieVision(Strategie):
    def __init__(self, robot:RobotMotorise, arene):
        Strategie.__init__(self, robot)
        self.arene=arene
        self.robot.tete.sensors["cam"].arene=arene

    def start_3D(self):
        self.robot.tete.sensors["cam"].run()


    def stop_3D(self):
        self.robot.tete.sensors["cam"].stop()

    def print_screen(self, filename):
        self.robot.tete.sensors["cam"].get_picture()
        while not self.robot.tete.sensors["cam"].is_set:
            pass
        self.robot.tete.sensors["cam"].picture()
        self.robot.tete.sensors["cam"].print_picture(filename)



    def update(self):
        pass

    def __dict__(self):
        dct = OrderedDict()
        dct["__class__"] = StrategieVision.__name__
        dct["robot"] = self.robot.__dict__()
        dct["arene"] = self.arene.__dict__()

        return dct

    @staticmethod
    def hook(dct):
        res = AreneRobot.hook(dct)
        if res is not None:
            return res
        elif dct["__class__"] == StrategieVision.__name__:
            return StrategieVision(dct["robot"], dct["arene"])

    @staticmethod
    def load(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f, object_hook=StrategieVision.hook)

if __name__=='__main__':
    st = StrategieVision(RobotMotorise(), AreneRobot())

    st.save("strategie_vision.json")
    print(st)

    st2 = StrategieVision.load("strategie_vision.json")
