from gl_lib.sim.robot.strategy.deplacement import DeplacementDroit, StrategieDeplacement
from gl_lib.config import PAS_TEMPS
from gl_lib.sim.robot import Tete, RobotMotorise
from math import pi
from time import sleep


class Tourner(StrategieDeplacement):
    """
    Fais décrire au robot un carré de coté 70 cm
    """

    def __init__(self, robot: RobotMotorise, angle_max):
        """

        :param robot:
        """
        StrategieDeplacement.__init__(self, robot)
        self.turning = True
        self.rot_angle = 0

        if angle_max < 0:
            self.sens = -1
        elif angle_max > 0:
            self.sens = 1
        self.angle_max = abs(angle_max)

        if self.sens > 0:
            self.robot.set_wheels_rotation(1, 30)
            self.robot.set_wheels_rotation(2, 0)
        elif self.sens < 0:
            self.robot.set_wheels_rotation(2, 30)
            self.robot.set_wheels_rotation(1, 0)

    def init_movement(self, angle_max):
        print("turning...")
        self.turning = True
        self.rot_angle = 0

        if angle_max < 0:
            self.sens = -1
        elif angle_max > 0:
            self.sens = 1
        self.angle_max = abs(angle_max)

        if self.sens > 0:
            self.robot.set_wheels_rotation(2, 30)
            self.robot.set_wheels_rotation(1, 0)
        elif self.sens < 0:
            self.robot.set_wheels_rotation(1, 30)
            self.robot.set_wheels_rotation(2, 0)
        self.robot.reset_wheels_angles()

    def update(self):

        if self.turning is True:
            self.robot.update()
            vitesse_rot = max(abs(self.robot.rd.vitesseRot), abs(self.robot.rg.vitesseRot))
            self.rot_angle += vitesse_rot * PAS_TEMPS * (self.robot.rd.diametre / self.robot.dist_wheels)

            if abs(self.rot_angle) > self.angle_max:
                print("done turning ", self.angle_max, "degrees")
                self.rot_angle = 0
                self.sens = 0
                self.turning = False

    def stop(self):
        return not self.turning


if __name__ == '__main__':
    from gl_lib.sim.simulation import Simulation
    from gl_lib.sim.display.d2.gui import AppSimulationThread
    from gl_lib.sim.robot import RobotMotorise
    from gl_lib.sim.robot.sensor import Accelerometre
    from gl_lib.sim.geometry import *
    from gl_lib.sim.geometry.point import *

    r = RobotMotorise(Pave(centre=point.Point(3, 6, 0), width=1, height=1, length=1), direction=Vecteur(1,0,0))
    sim = Simulation(Tourner(r, 90))
    app = AppSimulationThread(sim)

    sim.start()
    app.start()
