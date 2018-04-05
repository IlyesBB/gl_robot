from gl_lib.sim.geometry import *


class Balise(Objet3D):
    """
    Contient les informations concernant une balise
    """
    def __init__(self, width, length, height, colors, target:Pave, side):
        """
        Initialise une balise avec 4 couleurs
        :param couleurs: [tuple[4]] (r, g, v, o)
        """
        self.colors=colors
        if issubclass(target, point.Point):
            self.centre=target.clone()
        elif isinstance(target, Pave):
            self.centre=target.vertices[0]
        # A CORRIGER : s'adapter à la direction du robot pour trouver le bon sommet
        self.width=width
        self.height=height
        self.length=length
        self.side=side


