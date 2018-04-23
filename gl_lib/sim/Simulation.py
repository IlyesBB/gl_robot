import pdb
from threading import Thread
from gl_lib.config import PAS_TEMPS
from gl_lib.sim.geometry import Arene
from gl_lib.sim.robot.strategy import Strategie
from time import sleep

from gl_lib.utils import Serializable


class Simulation(Thread):
    """
    Classe qui gère les stratégies et compte le temps, jusqu'à ce qu'elles aient toutes envoyé un signal de fin
    """

    def __init__(self, strategies:[Strategie], acceleration_factor=1.0, tic=None):
        """

        :param strategie: liste de stratégies à exécuter
        :param acceleration_factor: le temps s'écoule acceleration_factor fois plus vite
        :param tic: Affiche un petit message tous les tic secondes
        """
        Thread.__init__(self)
        if len(strategies)<1:
            raise NameError("list of strategies not defined")
        self.strategies = strategies
        self.strategie = strategies[0]
        self.acceleration_factor = float(acceleration_factor)
        self.cpt = 0
        self.stop = True
        self.tic = int(tic/PAS_TEMPS) if tic is not None else None

    def run(self):
        """Lance une boucle qui met à jour les stratégies tous les PAS_TEMPS (gl_lib.config)
        Peut être accéléré en ajustant acceleration_factor
        """
        self.stop = False
        b = False
        dt = PAS_TEMPS/self.acceleration_factor
        print("Starting simulation...")
        while not self.stop:
            # La boucle s'arrête quand toutes méthodes stop() les stratégies on renvoyé True
            b = True
            for strategy in self.strategies:
                strategy.update()
                b = b and strategy.stop()
            if self.tic is not None:
                if self.cpt % self.tic == 0:
                    print(self.cpt, " seconds passed")
                    pdb.set_trace()
            self.cpt += 1
            sleep(dt)
            self.stop = b

        self.time_end = self.cpt*PAS_TEMPS

if __name__ == '__main__':
    from gl_lib.sim.robot import RobotMotorise
    strat = Strategie(RobotMotorise())
    sim = Simulation([strat])

    sim.start()
