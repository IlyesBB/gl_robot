<<<<<<< HEAD
import pdb
from threading import Thread, Event
=======
from threading import Thread
>>>>>>> parent of 2cc9880... ajout d'un set_trace pour trouver le bug dans deplacement droit
from gl_lib.config import PAS_TEMPS
from gl_lib.sim.geometry import Arene
from gl_lib.sim.robot.strategy import Strategie
from time import sleep

from gl_lib.utils import Serializable


class Simulation(Thread):
    """
    Classe qui gère les stratégies et compte le temps, jusqu'à ce qu'elles aient toutes envoyé un signal de fin
    """

<<<<<<< HEAD
    def __init__(self, strategies:[Strategie], acceleration_factor=1.0, tmax=None, tic=None, final_actions=None):
=======
    def __init__(self, strategie:[Strategie], acceleration_factor=1.0, tic=None):
>>>>>>> parent of 2cc9880... ajout d'un set_trace pour trouver le bug dans deplacement droit
        """

        :param strategie: liste de stratégies à exécuter
        :param acceleration_factor: le temps s'écoule acceleration_factor fois plus vite
        :param tic: Affiche un petit message tous les tic secondes
        """
        Thread.__init__(self)
<<<<<<< HEAD
        self.final_actions = final_actions
        if len(strategies)<1:
=======
        if len(strategie)<1:
>>>>>>> parent of 2cc9880... ajout d'un set_trace pour trouver le bug dans deplacement droit
            raise NameError("list of strategies not defined")
        self.strategies = strategie
        self.strategie = strategie[0]
        self.acceleration_factor = float(acceleration_factor)
        self.cpt = 0
        self.stop = True
<<<<<<< HEAD
        self.tic = int(tic/PAS_TEMPS) if tic is not None else None
        self.tmax = int(tmax/PAS_TEMPS) if tmax is not None else None
        self.close = Event()
        self.close.clear()

=======
        self.tic = tic
>>>>>>> parent of 2cc9880... ajout d'un set_trace pour trouver le bug dans deplacement droit

    def run(self):
        """Lance une boucle qui met à jour les stratégies tous les PAS_TEMPS (gl_lib.config)
        Peut être accéléré en ajustant acceleration_factor
        """
        print("Starting simulation...")
<<<<<<< HEAD
        print(self.strategie.stop(), self.stop)
=======
        b = False
        self.stop = False
>>>>>>> parent of 2cc9880... ajout d'un set_trace pour trouver le bug dans deplacement droit
        while not self.stop:
            # La boucle s'arrête quand toutes méthodes stop() les stratégies on renvoyé True
            b = True
            for strategy in self.strategies:
                strategy.update()
                b = b and strategy.stop()
            if self.tic is not None:
<<<<<<< HEAD
                if self.cpt % self.tic == 0:
                    print(self.cpt*PAS_TEMPS, " seconds passed")
                    print(self.strategie.sens)
            self.cpt += 1
=======
                if self.cpt % (int(self.tic/PAS_TEMPS)) == 0:
                    print("Tic: ", self.cpt, " seconds passed")
            self.cpt += 1
            sleep(PAS_TEMPS/self.acceleration_factor)
>>>>>>> parent of 2cc9880... ajout d'un set_trace pour trouver le bug dans deplacement droit
            self.stop = b
            if self.tmax is not None:
                if self.cpt > self.tmax:
                    print("Maximum time passed ({})".format(self.cpt*PAS_TEMPS))
                    self.stop = True
                    break
            sleep(dt)

<<<<<<< HEAD
        self.time_end = self.cpt*PAS_TEMPS
        print("End simalution ({} s)".format(self.time_end))
        if self.final_actions is not None and len(self.final_actions)>0:
            for f in self.final_actions:
                f()



=======
        print("Simulation stopped\nSimulation time: ", self.cpt*PAS_TEMPS, "s\n")
>>>>>>> parent of 2cc9880... ajout d'un set_trace pour trouver le bug dans deplacement droit

if __name__ == '__main__':
    from gl_lib.sim.robot import RobotMotorise
    strat = Strategie(RobotMotorise())
    sim = Simulation([strat])

    sim.start()

