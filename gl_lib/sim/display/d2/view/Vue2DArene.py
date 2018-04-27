# -*- coding: utf-8 -*-
from gl_lib.sim.display.d2.view import Vue2DRobot, Vue2DRobotPhysique, Vue2DPave, Vue2D
from gl_lib.sim.geometry import Arene, Pave
from gl_lib.sim.robot import *
from tkinter import Canvas



class Vue2DArene(Vue2D):
    """
        Contient tous les objets de l'arène et les affiche
    """

    def __init__(self, arene):
        """
            Intialisation de l'attribut arene
        :param arene: Arène à représenter
        :type arene: Arene
        """
        Vue2D.__init__(self)
        self.arene = arene

    def afficher(self, canevas):
        """ 
            Affiche les objets de l'arène sur le canevas, s'ils sont reconnus

        :param canevas: Canevas tkinter sur lequel dessiner
        :param canevas: Canvas

        """
        # objets: [Objet3D]
        objets = self.arene.objets3D

        for o in objets:
            # o : Objet3D
            if issubclass(type(o), Pave):
                vue = Vue2DPave(o, canevas)
                vue.afficher(canevas)
            elif issubclass(type(o), RobotMotorise):
                view = Vue2DRobotPhysique(o, canevas)
                view.afficher(canevas)
            elif issubclass(type(o), Robot):
                vue = Vue2DRobot(o, canevas)
                vue.afficher(canevas)

