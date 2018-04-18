from gl_lib.sim.robot import RobotMotorise, Tete
from gl_lib.sim.robot.sensor import Accelerometre, CapteurIR
from gl_lib.sim.robot.sensor.camera import Camera
class Strategie(object):
    """
    definit une strategy de robot de facon abstraite
    """
    def __init__(self, robot:RobotMotorise):
        """
        robot : Robot
        """
        self.robot = robot
        self.robot.tete = Tete(self.robot.centre, self.robot.direction)
        self.robot.tete.add_sensors(acc=Accelerometre(self.robot.tete.centre, self.robot.tete.direction),
                                    ir=CapteurIR(self.robot.tete.centre, self.robot.tete.direction, portee=3),
                                    cam=Camera(self.robot.tete.centre, self.robot.tete.direction))
    def stop(self):
        return False

    def update(self):
        pass

