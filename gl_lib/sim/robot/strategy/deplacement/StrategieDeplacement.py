# -*- coding: utf-8 -*-
from gl_lib.sim.robot.strategy.Strategie import Strategie
from gl_lib.sim.robot import Tete, Robot
from threading import RLock

class StrategieDeplacement(Strategie):
    """
        Stratégie qui ne fait qu'actualiser la position du robot
    """
    KEYS = ["robot"]
    def __init__(self, robot):
        Strategie.__init__(self, robot)

    def update(self):
        """
            Actualise la position du robot
        """
        self.robot.update()

    def stop(self):
        """
            La stratégie ne s'arrète jamais: Renvoi toujours False
        """
        return False
