from gl_lib.sim.robot.strategy.Strategie import Strategie

class StrategieDeplacement(Strategie):
    """
    definit une strategy de deplacement de facon abstraite
    """
    def __init__(self, robot):
        Strategie.__init__(self, robot)
    
    def update(self):
        self.robot.update()

    def stop(self):
        return False