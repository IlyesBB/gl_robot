from gl_lib.sim.geometry import Objet3D, Vecteur, Point, Pave, ApproximableAPave
from gl_lib.config import PAS_TEMPS
from math import pi


class Robot(Objet3D, ApproximableAPave):
    """
    Classe definissant les elements essentiels d'un robot
    """

    def __init__(self, pave:Objet3D=Pave(1,1,1, Point(0,0,0)), rg:Objet3D=Objet3D(), rd:Objet3D=Objet3D(), direction:Vecteur=Vecteur(0,1,0)):
        """
        Constructeur du robot
        
        direction: Vecteur norme montrant la direction initiale du robot
        forme: Pave attendu (correspond aux methodes de deplacement)
        rd: Objet3D, roue droite
        rg: Objet3D, roue gauche
        """
        Objet3D.__init__(self)
        self.direction = direction
        self.forme = pave
        self.forme.rotate(self.direction.get_angle())
        self.centre = pave.centre.clone()  # initalise le centre au centre du pave
        self.rd = rd
        self.rg = rg

        # initialisation des centres des roues
        self.rd.centre = self.centre+(self.direction.rotate(-pi/4)*self.forme.width/2)
        self.rg.centre = self.centre+(self.direction.rotate(pi/4)*self.forme.width/2)

        self.dist_wheels=self.forme.width



    def rotate_around(self, point:Point, angle:float, axis=None):
        """
        tourne le robot autour de point d'un angle teta
        """
        # rotation du pave et des roues
        Objet3D.rotate_around(self, point, angle, axis)
        self.forme.rotate_around(point, angle, axis)
        self.rd.rotate_around(point, angle, axis)
        self.rg.rotate_around(point, angle, axis)

    def rotate_all_around(self, point:Point, angle:float, axis=None):
        Objet3D.rotate_around(self, point, angle, axis)
        self.forme.rotate_all_around(point, angle, axis)
        self.rg.rotate_around(point, angle, axis)
        self.rd.rotate_around(point, angle, axis)
        self.direction.rotate(angle, axis)

    def move(self, vecteur:Vecteur):
        """
        deplace le corps et les roues du robot
        """
        Objet3D.move(self, vecteur)
        self.forme.move(vecteur)
        self.rg.move(vecteur)
        self.rd.move(vecteur)

    def __eq__(self, other):
        if not Objet3D.__eq__(self, other):
            return False
        if other.forme != self.forme:
            return False
        if other.rd != self.rd or other.rg != self.rg:
            return False
        if other.direction != self.direction:
            return False
        if other.dist_wheels != self.dist_wheels:
            return False
        return True

    def clone(self):
        return Robot(self.forme.clone(), self.rd.clone(), self.rg.clone(), self.direction.clone())

    def get_pave(self):
        return self.forme