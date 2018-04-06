from gl_lib.sim.geometry import *
from gl_lib.sim.geometry.point import *
from gl_lib.sim.robot import *


class Balise(Objet3D):
    """
    Contient les informations concernant une balise
    """
    def __init__(self, width, length, height, colors, target:Point, side):
        """
        Initialise une balise avec 4 couleurs
        :param couleurs: [tuple[4]] (r, g, v, o)
        """
        self.colors=colors
        self.target=target

        # A CORRIGER : s'adapter à la direction du robot pour trouver le bon sommet
        self.width=width
        self.height=height
        self.length=length
        self.side=side



