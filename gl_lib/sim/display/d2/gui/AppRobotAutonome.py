from gl_lib.sim.display.d2.gui import AppRobot
from gl_lib.sim.geometry.point import *
from gl_lib.sim.geometry import Arene
from time import sleep
from tkinter import *
from gl_lib.config import PAS_TEMPS

class AppRobotAutonome(AppRobot):
    dt=PAS_TEMPS

    def __init__(self, robot, arene: Arene ):
        """
        initialise les commandes supplementaires pour piloter le robot
        :param robot: a chaque clic, on actualisera les action de ce robot
        :param arene: contient les objets à afficher, le root compris
        """
        AppRobot.__init__(self, robot, arene)
        self.canvas.bind('<Button-1>', self.setDestRobot)
        self.canvas.bind('<Button-2>', self.stopRobot)

    def keyCommand(self, event):
        """
        dirige le robot selon la touche tapee, et lui donne une destination avec la sourie
        """
        self.robot.destination=None

        touche=event.keysym
        if touche=='z':
            self.robot.move_forward(1)
        elif touche=='s':
            self.robot.move_forward(-1)
        elif touche=='q':
            self.robot.turn(1)
        elif touche=='d':
            self.robot.turn(-1)

        self.robot.update()
        self.update()

    def setDestRobot(self, event: Button):
        """
        donne une destination au robot, et lui fait executer la trajectoire
        """
        self.robot.deplacer_vers(Point(event.x, event.y, 0))
        self.actionRobot()

    def action_robot(self):
        """
        Met a jour la simulation, et fais passez une unite de temps
        
        si le robot n'a pas atteint sa cible, la simulation avance encore d'une unite
        """
        while self.robot.destination is not None:
            self.robot.update()
            self.update()
            sleep(AppRobotAutonome.dt)


    def stop_robot(self, event: Button):
        """
        le robot arrete de poursuivre la cible
        appele si clic milieu
        """
        self.robot.destination=None
        self._commandes_clavier=True

    def update_values(self):
        """
        Met a jour les vitesses, et la position du robot
        """
        self.robot.vitesse=float(self.vitesse.get())
        self.robot.vitesseRot=float(self.vitesseRot.get())
    
    def update_canvas(self):
        """
        Met a jour le canvas
        """
        self.canvas.delete(ALL)
        self.arene.afficher(self.canvas)
        self.canvas.update()

    def update(self):
        """
        Met a jour les vitesses, la simulation du mouvement du robot et l'display
        """
        self.update_values()
        self.update_canvas()