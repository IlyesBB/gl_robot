from gl_lib.sim.geometry.point import Vecteur, Point
from gl_lib.sim.geometry.Objet3D import Objet3D
from gl_lib.sim.geometry import Pave
from gl_lib.config import PAS_TEMPS
from math import pi


class Robot(Objet3D):
    """
    Classe definissant les elements essentiels d'un robot
    """

    def __init__(self, pave:Objet3D=Pave(0,0,0), rg:Objet3D=Objet3D(), rd:Objet3D=Objet3D(), direction:Vecteur=Vecteur(0,1,0), vitesserot:float=0.1, vitesse:float=5.0, echelle:bool=True):
        """
        Constructeur du robot
        
        direction: Vecteur norme montrant la direction initiale du robot
        forme: Pave attendu (correspond aux methodes de deplacement)
        rd: Objet3D, roue droite
        rg: Objet3D, roue gauche
        """
        Objet3D.__init__(self)
        self.direction = direction
        if echelle:
            self.vitesse = vitesse*PAS_TEMPS
            self.vitesseRot = vitesserot*PAS_TEMPS
        self.forme = pave
        self.centre = pave.centre.clone()  # initalise le centre au centre du pave
        self.rd = rd
        self.rg = rg

        # initialisation des centres des roues
        self.rd.centre = self.centre+(self.direction.rotate(-pi/4)*self.forme.width/2)
        self.rg.centre = self.centre+(self.direction.rotate(pi/4)*self.forme.width/2)

        self.dist_wheels=self.forme.width




    def move_forward(self, sens: int or float):
        """
        deplace le robot dans le sens voulu (1 pour l'avant, -1 pour l'arriere par ex), sur sa direction
        La fonction deplacer vien du module Vecteur eet se trouve dans la class point
        """
        if sens < 0:
            self.move(self.direction * -self.vitesse)
        elif sens > 0:
            self.move(self.direction * self.vitesse)

    def turn(self, sens: int or float):
        """
        tourne le robot par rapport a une des roues selon le sens 
        """
        if sens > 0:
            self.direction.rotate(-self.vitesseRot)
            self.rotate_around(self.rd.centre, -self.vitesseRot)
        elif sens < 0:
            self.direction.rotate(self.vitesseRot)
            self.rotate_around(self.rg.centre, self.vitesseRot)

    def rotate_around(self, point:Point, angle:float):
        """
        tourne le robot autour de point d'un angle teta
        """
        # rotation du pave et des roues
        Objet3D.rotate_around(self, point, angle)
        self.forme.rotate_around(point, angle)

    def rotate_all_around(self, point:Point, angle:float):
        Objet3D.rotate_around(self, point, angle)
        self.forme.rotate_all_around(point, angle)
        self.rg.centre.rotate_around(point, angle)
        self.rd.centre.rotate_around(point, angle)
        self.direction.rotate(angle)

    def move(self, vecteur:Vecteur):
        """
        deplace le corps et les roues du robot
        """
        Objet3D.move(self, vecteur)
        self.forme.move(vecteur)
        self.rg.move(vecteur)
        self.rd.move(vecteur)
