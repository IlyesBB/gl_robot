from gl_lib.sim.robot.strategy.deplacement import DeplacementDroit70
from gl_lib.config import PAS_TEMPS
from gl_lib.sim.robot import Tete
from math import pi
from time import sleep

class DeplacementCarre70(DeplacementDroit70):
    """
    Fais décrire au robot un carré de coté 70 cm
    """

    def __init__(self, robot):
        """

        :param robot:
        """
        DeplacementDroit70.__init__(self, robot)
        self.cpt_turn = 1
        self.turning = False
        self.rot_angle = 0

    def update(self):

        if self.turning is True:
            self.robot.update()
            self.rot_angle += abs(
                max(self.robot.rd.vitesseRot,
                    self.robot.rg.vitesseRot) * PAS_TEMPS * self.robot.rd.diametre / (
                        self.robot.dist_wheels))

            if self.rot_angle > 90:
                print("done turn ", self.cpt_turn)
                self.cpt_turn += 1
                self.posDepart = self.robot.centre.clone()
                self.rot_angle = 0

                self.in_action = True
                print("advancing...")
                self.robot.set_wheels_rotation(3, 60)
                self.distance = 0
                self.turning = False
        else:
            DeplacementDroit70.update(self)
            if not self.in_action:
                self.in_action=False
                print("done advancing")
                self.turning = True
                print("turning...")
                self.robot.reset_wheels_angles()
                self.robot.set_wheels_rotation(2, 60)
                self.robot.set_wheels_rotation(1, 0)

    def stop(self):
        if self.in_action:
            DeplacementDroit70.stop(self)
        if self.cpt_turn > 4:
            return True
        return False


if __name__ == '__main__':
    from gl_lib.sim.simulation import Simulation
    from gl_lib.sim.display.d2.gui import AppSimulationThread
    from gl_lib.sim.robot import RobotMotorise
    from gl_lib.sim.robot.sensor import Accelerometre
    from gl_lib.sim.geometry import *

    r = RobotMotorise(Pave(centre=point.Point(3, 6, 0), width=1, height=1, length=1))
    sim = Simulation(DeplacementCarre70(r))
    app = AppSimulationThread(sim)

    sim.start()
    app.start()
