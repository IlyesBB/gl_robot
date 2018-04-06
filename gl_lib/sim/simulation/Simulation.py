from threading import Thread

class Simulation(Thread):
    """
    Classe gerant la simulation
    """

    def __init__(self, strategie, arene=None):
        """

        """
        Thread.__init__(self)
        self.strategie = strategie
        self.arene=arene

    def run(self):
        """

        :return:
        """
        cpt = 0
        while not self.strategie.stop():
            self.strategie.update()
            cpt += 1
        print("stop")


if __name__ == '__main__':
    from gl_lib.sim.robot import RobotMotorise
    from gl_lib.sim.robot.strategy import Strategie

    strat = Strategie(RobotMotorise())
    sim = Simulation(strat)

    sim.run()
