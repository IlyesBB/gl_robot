from tkinter import *
from gl_lib.sim.simulation import Simulation
from gl_lib.sim.geometry import *
from gl_lib.sim.display.d2.view import Vue2DArene
from threading import Thread
from gl_lib.config import PAS_TEMPS

class AppSimulation(Tk):
    """
    Definit une structure d'display d'un robot dans une arene vide
    """

    def __init__(self, simulation: Simulation):
        """

        :param simulation:
        """
        Tk.__init__(self)
        self.simulation = simulation
        try:
            self.vue_arene = Vue2DArene(self.simulation.arene)
        except:
            a = Arene()
            a.add(self.simulation.strategie.robot)
            self.vue_arene=Vue2DArene(a)

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


class AppSimulationThread(Thread):
    def __init__(self, simulation):
        Thread.__init__(self)
        self.simulation=simulation

    def run(self):
        self.window=AppSimulation(self.simulation)
        self.window.mainloop()


if __name__=='__main__':
    from gl_lib.sim.robot import RobotMotorise
    from gl_lib.sim.geometry.point import Point
    r=RobotMotorise(Pave(30,30,0,centre=Point(100,100,0)))

