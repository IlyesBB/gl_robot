from gl_lib.sim.robot.strategy.deplacement import DeplacementDroit, Tourner
from gl_lib.config import PAS_TEMPS
from gl_lib.sim.robot import Tete
from math import pi
from time import sleep


class DeplacementCarre(DeplacementDroit, Tourner):
    """
    Fais décrire au robot un carré de coté 70 cm
    """

    def __init__(self, robot, cote):
        """

        :param robot:
        """
        Tourner.__init__(self, robot, 90)
        DeplacementDroit.__init__(self, robot, cote)

        self.cpt_turn = 1
        self.turning = False
        self.cote = cote

    def update(self):
        if self.advancing:
            DeplacementDroit.update(self)
            if not self.advancing:
                DeplacementDroit.abort(self)
                Tourner.init_movement(self, 90)
        elif self.turning:
            Tourner.update(self)
        else:
            DeplacementDroit.init_movement(self, self.cote)
            self.cpt_turn += 1


    def stop(self):
        if self.cpt_turn > 4:
            return True
        else:
            return False


if __name__ == '__main__':
    from gl_lib.sim import Simulation
    from gl_lib.sim.display.d2.gui import AppAreneThread
    from gl_lib.sim.robot import *
    from gl_lib.sim.robot.sensor import Accelerometre
    from gl_lib.sim.geometry import *

    a = AreneFermee(10,10,10)
    r = RobotMotorise(Pave(centre=Point(3, 6, 0), width=1, height=1, length=1))
    sim = Simulation(DeplacementCarre(r, 1), 5)
    a.add(r)
    app = AppAreneThread(a)

    sim.start()
    app.start()
