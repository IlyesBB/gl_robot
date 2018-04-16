from tkinter import *
from gl_lib.sim.simulation import Simulation
from gl_lib.sim.geometry import *
from gl_lib.sim.robot.display.d2.view import Vue2DArene
from threading import Thread
from gl_lib.config import PAS_TEMPS


class AppArene(Tk):
    """
    Definit une structure d'display d'un robot dans une arene vide
    """

    def __init__(self, arene:Arene=None):
        """

        :param simulation:
        """
        Tk.__init__(self)
        if arene is not None:
            self.vue_arene = Vue2DArene(arene)
        else:
            a = Arene()
            self.vue_arene = Vue2DArene(a)

        self.stop = True

        self.canvas = Canvas(self, height=450, width=600, bg='white')

        self.canvas.bind("<Button-1>", self.start)
        self.canvas.bind("<Button-2>", self.stop)
        self.vue_arene.afficher(self.canvas)

        self.canvas.pack()

    def start(self, event):
        """
        lance la simulation
        :return:
        """
        self.stop = False
        self.update()

    def update(self):
        """
        Met a jour les vitesses
        """
        self.canvas.delete(ALL)
        self.vue_arene.afficher(self.canvas)

        self.after(int(PAS_TEMPS*1000), self.update)


class AppAreneThread(Thread):
    def __init__(self, arene):
        Thread.__init__(self)
        self.arene = arene

    def run(self):
        self.window = AppArene(self.arene)
        self.window.mainloop()

    def stop(self):
        self.window.quit()


if __name__ == '__main__':
    from gl_lib.sim.robot.strategy.deplacement import DeplacementDroit
    from gl_lib.sim.robot import RobotMotorise
    from gl_lib.sim.simulation import Simulation, ThreadTkStrategy
    from gl_lib.sim.geometry import Vecteur

    strat=DeplacementDroit(RobotMotorise(direction=Vecteur(1,1,0).norm()), 1)
    sim = Simulation(strat)

    thread= ThreadTkStrategy(strat)

    thread.start()
    sim.start()
