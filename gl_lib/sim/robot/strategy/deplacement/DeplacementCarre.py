from gl_lib.sim.robot.strategy.deplacement import DeplacementDroit, Tourner
from gl_lib.config import PAS_TEMPS
from gl_lib.sim.robot import Tete
from math import pi
from time import sleep


class DeplacementCarre(DeplacementDroit):
    """
    Fais décrire au robot un carré de coté 70 cm
    """

    def __init__(self, robot, cote):
        """

        :param robot:
        """
        Tourner.__init__(self, robot, 45)
        DeplacementDroit.__init__(self, robot, cote)

        self.cpt_turn = 1
        self.turning = False

    def update(self):
        if self.advancing:
            DeplacementDroit.update(self)
            if not self.advancing:
                Tourner.init_movement(self, 45)
        if self.turning:
            Tourner.update(self)
            if not self.turning:
                print(self.robot.direction, self.robot.tete.direction)
                DeplacementDroit.init_movement(self, self.distance_max)

                self.cpt_turn += 1

    def stop(self):
        if self.cpt_turn > 4:
            return True
        else:
            return False


if __name__ == '__main__':
    from gl_lib.sim.simulation import Simulation
    from gl_lib.sim.display.d2.gui import AppSimulationThread
    from gl_lib.sim.robot import *
    from gl_lib.sim.robot.sensor import Accelerometre
    from gl_lib.sim.geometry import *

    r = RobotMotorise(Pave(centre=point.Point(3, 6, 0), width=1, height=1, length=1))
    sim = Simulation(DeplacementCarre(r, 1))
    app = AppSimulationThread(sim)

    sim.start()
    app.start()
