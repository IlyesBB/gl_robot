# -*- coding: utf-8 -*-
from gl_lib.sim.display.d2.view.Vue2D import Vue2D
from gl_lib.sim.geometry import Pave
from gl_lib.config import PIX_PAR_M_2D
from tkinter import Canvas

class Vue2DPave(Vue2D):
    """
        Représentation en 2 dimensions d'un pavé pour tkinter
    """
    def __init__(self, pave, canevas):
        """
            Crée une copie du pavé en argument à la bonne échelle pour l'affichage 2D, puis le convertis en lignes tkinter

            Il est supposé que les sommets du pave sont rangés dans le bon ordre (anti-horaire) et que les 4 premiers sont
            les plus hauts
        :param pave: Pavé à représenter
        :type pave: Pave
        :param canevas: Canevas sur lequel dessiner
        :type canevas: Canvas
        """
        Vue2D.__init__(self)
        self.pave=Pave(width=pave.width * PIX_PAR_M_2D, length=pave.length * PIX_PAR_M_2D, height=pave.height * PIX_PAR_M_2D, centre=pave.centre * PIX_PAR_M_2D)
        self.pave.rotate((pave.vertices[1] - pave.vertices[0]).to_vect().get_angle())
        self.cotes=list()
        for i in range(0,3):
            self.cotes.append(canevas.create_line(pave.vertices[i].x,pave.vertices[i].y, pave.vertices[i+1].x, pave.vertices[i+1].y))
        self.cotes.append(canevas.create_line(pave.vertices[3].x,pave.vertices[3].y, pave.vertices[0].x, pave.vertices[0].y))

    def afficher(self, canevas):
        """ 
            Met à jour les coordonnées des points
        """
        if self.pave and canevas:
            #sommets: [Point]
            sommets=self.pave.vertices
            for i in range (0,3):
                canevas.coords(self.cotes[i], sommets[i].x, sommets[i].y, sommets[i+1].x, sommets[i+1].y)
            canevas.coords(self.cotes[3], sommets[3].x, sommets[3].y, sommets[0].x, sommets[0].y)
