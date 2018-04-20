from threading import Thread
from gl_lib.config import PAS_TEMPS
from gl_lib.sim.geometry import Arene
from gl_lib.sim.robot.strategy import Strategie
from time import sleep



class Simulation(Thread):
    """
    Classe gerant la simulation
    """

    def __init__(self, strategie: Strategie or [Strategie], acceleration_factor=1.0, tic=None):
        """

        """
        Thread.__init__(self)
        self.strategie = strategie
        self.acceleration_factor = float(acceleration_factor)
        self.cpt = 0
        self.stop = True
        self.is_list = isinstance(self.strategie, list)
        self.tic = tic

    def run(self):
        """

        :return:
        """
        print("Starting simulation...")
        b = False
        self.stop = False
        while not b and not self.stop:
            if not self.is_list:
                self.strategie.update()
                b = self.strategie.stop()
            else:
                b = True
                for strategy in self.strategie:
                    strategy.update()
                    b = b and strategy.stop()
            if self.tic is not None:
                if self.cpt % (int(self.tic/PAS_TEMPS)) == 0:
                    print("Tic: ", self.cpt, " seconds passed")
            self.cpt += 1
            sleep(PAS_TEMPS/self.acceleration_factor)
        self.stop = True
        try:
            print("Simulation stopped\nSimulation time: ", self.cpt*PAS_TEMPS, "s\n")
        except:
            pass

if __name__ == '__main__':
    from gl_lib.sim.robot import RobotMotorise
    strat = Strategie(RobotMotorise())
    sim = Simulation(strat)

    sim.start()
