from gl_lib.sim.geometry.point import *
from gl_lib.sim.geometry import *

class Capteur(Objet3D):
    """
    Classe abstraite

    La positione et la direction du capteur sont liées a celles de la tête s'il y en a une
    """

    def __init__(self, centre=Point(0, 0, 0), direction=Vecteur(1, 0, 0), tete=None):
        Objet3D.__init__(self, centre=centre)
        self.direction = direction.clone()
        if tete is not None:
            #si on entre une tete en argument, on lie le sensor a celle ci
            self.centre=tete.centre
            self.direction=tete.direction

    def __repr__(self):
        return "Sensor de type : {} , position : {}".format(type(self), self.centre)


