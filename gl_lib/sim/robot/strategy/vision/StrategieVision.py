from gl_lib.sim.robot.strategy import Strategie
from gl_lib.sim.robot import Tete

class StrategieVision(Strategie):
    def __init__(self, robot, arene):
        Strategie.__init__(self, robot)
        self.arene=arene
        self.robot.tete.lcapteurs[Tete.CAM].arene=arene
        self.robot.tete.lcapteurs[Tete.CAM].start()
