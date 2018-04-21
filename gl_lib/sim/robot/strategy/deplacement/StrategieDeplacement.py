from gl_lib.sim.robot.strategy.Strategie import Strategie
from gl_lib.sim.robot import Tete, Robot
from threading import RLock

class StrategieDeplacement(Strategie):
    """
    definit une strategy de deplacement de facon abstraite
    """
    KEYS = ["robot"]
    def __init__(self, robot):
        Strategie.__init__(self, robot)

    def update(self):
        Strategie.update(self)
        self.robot.update()

    def stop(self):
        return False