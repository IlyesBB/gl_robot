from gl_lib.sim.robot import Robot
from gl_lib.sim.geometry import *

class RobotAutonome(Robot):
    """
    definit un robot capable d'executer des strategies
    
    on doit initialiser sa strategy
    """

    def __init__(self, pave:Objet3D=Pave(0, 0, 0), rg:Objet3D=Objet3D(), rd:Objet3D=Objet3D(), direction:Vecteur=Vecteur(0, -1, 0)):
        """
        initialise les attributs de l'objet courant
        initialise l'attribut robot de la strategy
        """
        Robot.__init__(self, pave, rg, rd, direction)
        self.stratDeplacement = None
        self.destination = None

    def deplacer_vers_dest(self):
        if not self.destination is None:
            self.stratDeplacement.deplacement_vers(self.destination)

    def deplacer_vers(self, destination:Point):
        self.destination = destination
        self.deplacer_vers_dest()

    def update(self):
        self.deplacer_vers_dest()
