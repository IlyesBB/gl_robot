from gl_lib.sim.display.d2.view import Vue2DPave, Vue2DVecteur
from gl_lib.sim.display.d2.view.Vue2D import Vue2D
from gl_lib.sim.geometry import *


class Vue2DRobot(Vue2D):
    def __init__(self, robot, canevas):
        """
        construit la view du robot = view de la direction + view du pave
        """
        self.robot = robot
        self.vuePave = Vue2DPave(robot.forme, canevas)
        self.vueVitesse = Vue2DVecteur(robot.direction, canevas)

    def afficher(self, canevas):
        """ 
        affiche le pave et la direction du robot
        """
        self.vuePave.afficher(canevas)
        self.vueVitesse.afficher(canevas, self.robot.forme.centre)


class Vue2DRobotPhysique(Vue2DRobot):
    def __init__(self, robot, canevas):
        Vue2DRobot.__init__(self, robot, canevas)
        self.vueTete = Vue2DVecteur(self.robot.tete.direction, canevas)

    def afficher(self, canevas):
        """
        affiche le pave et la direction du robot
        """
        Vue2DRobot.afficher(self, canevas)
        self.vueTete.afficher(canevas, self.robot.tete.centre)
