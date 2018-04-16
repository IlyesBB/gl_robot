from gl_lib.sim.robot.strategy import Strategie
from gl_lib.sim.robot import Tete
from threading import RLock

class StrategieVision(Strategie):
    def __init__(self, robot, arene):
        Strategie.__init__(self, robot)
        self.arene=arene
        self.lock = RLock()
        self.robot.tete.lcapteurs[Tete.CAM].arene=arene

    def start_3D(self):
        self.robot.tete.lcapteurs[Tete.CAM].start()
        self.robot.tete.lcapteurs[Tete.CAM].join()
        self.robot.tete.lcapteurs[Tete.CAM].lock = self.lock


    def stop_3D(self):
        self.robot.tete.lcapteurs[Tete.CAM].stop()

    def update(self):
        pass

