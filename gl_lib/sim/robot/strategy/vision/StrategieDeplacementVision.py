from gl_lib.sim.robot.strategy.deplacement import StrategieDeplacement
from gl_lib.sim.robot.strategy.vision import StrategieVision

class StrategieDeplacementVision(StrategieDeplacement, StrategieVision):
    def __init__(self, robot, arene):
        StrategieDeplacement.__init__(self, robot)
        StrategieVision.__init__(self,robot, arene)


    def update(self):
        StrategieDeplacement.update(self)
