from gl_lib.sim.robot.strategy import Strategie
from gl_lib.sim.robot import Tete
from threading import RLock

class StrategieVision(Strategie):
    def __init__(self, robot, arene):
        Strategie.__init__(self, robot)
        self.arene=arene
        self.robot.tete.lcapteurs[Tete.CAM].arene=arene

    def start_3D(self):
        self.robot.tete.lcapteurs[Tete.CAM].run()


    def stop_3D(self):
        self.robot.tete.lcapteurs[Tete.CAM].stop()

    def print_screen(self):
        self.robot.tete.lcapteurs[Tete.CAM].get_picture()
        self.robot.tete.lcapteurs[Tete.CAM].picture()
        self.robot.tete.lcapteurs[Tete.CAM].print_picture()


    def update(self):
        pass

