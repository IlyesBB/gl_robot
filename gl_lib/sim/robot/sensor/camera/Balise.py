# -*- coding: utf-8 -*-
from gl_lib.sim.geometry import *


class Balise(Objet3D):
    """
    Contient les informations concernant une balise
    """
    def __init__(self, width=1, length=1, height=1, colors=None):
        """
        Initialise une balise avec 4 couleurs
        :param couleurs: [tuple[4]] (r, g, v, o)
        """
        Objet3D.__init__(self, centre=Point(0,0,0))
        if colors is None:
            colors = [(255, 0, 0, 255), (0, 255, 0, 255), (255, 255, 0, 255), (0, 0, 255, 255)]
        self.colors=colors

        self.width=width
        self.height=height
        self.length=length

    def clone(self):
        return Balise(self.width, self.length, self. height, colors=list(self.colors))