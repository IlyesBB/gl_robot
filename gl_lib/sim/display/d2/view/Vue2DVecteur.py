from gl_lib.sim.display.d2.view.Vue2D import Vue2D
from gl_lib.sim.geometry import *
from tkinter import *
from gl_lib.config import PIX_PAR_M
class Vue2DVecteur(Vue2D):
    """ Classe contenant un vecteur et sa representation2D """
    def __init__(self, vecteur, canevas):
        """Constructeur de la view
        vecteur: Vecteur
        ligne: ligne 2D
        canevas: Canevas
        
        Cree la ligne dans canevas
        """
        self.vecteur=vecteur
        self.ligne=canevas.create_line(0, 0, vecteur.x*PIX_PAR_M, vecteur.y*PIX_PAR_M)
        
    def afficher(self, canevas, position):
        """ actualise la position de ligne """

        canevas.coords(self.ligne, position.x*PIX_PAR_M, position.y*PIX_PAR_M, (position.x+self.vecteur.x)*PIX_PAR_M, (position.y+self.vecteur.y)*PIX_PAR_M)