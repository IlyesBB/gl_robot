# -*- coding: utf-8 -*-
from gl_lib.sim.display.d2.view import Vue2D
from gl_lib.sim.geometry import Vecteur
from tkinter import Canvas
from gl_lib.config import PIX_PAR_M_2D


class Vue2DVecteur(Vue2D):
    """
        Représente un vecteur en 2D pour tkinter
    """
    def __init__(self, vecteur, canevas):
        """
            Construit la vue du vecteur comme une ligne
        :param vecteur: Vecteur à représenter
        :type vecteur: Vecteur
        :param canevas: Canevas sur lequel dessiner
        :type canevas: Canvas
        """
        Vue2D.__init__(self)
        self.vecteur=vecteur
        self.ligne=canevas.create_line(0, 0, vecteur.x*PIX_PAR_M_2D, vecteur.y*PIX_PAR_M_2D)
        
    def afficher(self, canevas, position):
        """
            Actualise la position de la vue
        """
        canevas.coords(self.ligne, position.x*PIX_PAR_M_2D, position.y*PIX_PAR_M_2D, (position.x+self.vecteur.x)*PIX_PAR_M_2D, (position.y+self.vecteur.y)*PIX_PAR_M_2D)
