# -*- coding: utf-8 -*-
from gl_lib.sim.display.d2.view import Vue2DPave, Vue2DVecteur
from gl_lib.sim.display.d2.view.Vue2D import Vue2D
from gl_lib.sim.geometry import *
from gl_lib.sim.robot import Robot
from tkinter import Canvas

class Vue2DRobot(Vue2D):
    """
        Représente un robot en 2D pour tkinter comme un pavé avec un trait pointant dans sa direction
    """
    def __init__(self, robot, canevas):
        """
            Construit la vue du robot comme combinaison de deux vues
        :param robot: Robot à afficher
        :type robot: Robot
        :param canevas: Canevas sur lequel dessiner
        :type canevas: Canvas
        """
        Vue2D.__init__(self)
        self.robot = robot
        self.vuePave = Vue2DPave(robot.forme, canevas)
        self.vueVitesse = Vue2DVecteur(robot.direction, canevas)

    def afficher(self, canevas):
        """ 
            Affiche le pave et la direction du robot
        """
        self.vuePave.afficher(canevas)
        self.vueVitesse.afficher(canevas, self.robot.forme.centre)


class Vue2DRobotPhysique(Vue2DRobot):
    """
        Représente un robot avec une tête en 2D pour tkinter

        TODO: Vérifier que cette classe fonctionne
    """
    def __init__(self, robot, canevas):
        Vue2DRobot.__init__(self, robot, canevas)
        self.vueTete = Vue2DVecteur(self.robot.tete.direction, canevas)

    def afficher(self, canevas):
        """
        affiche le pave et la direction du robot
        """
        Vue2DRobot.afficher(self, canevas)
        self.vueTete.afficher(canevas, self.robot.tete.centre)
