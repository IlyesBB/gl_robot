# -*- coding: utf-8 -*-
from collections import OrderedDict

from gl_lib.sim.geometry import *


class Balise(Objet3D):
    """
    Contient les informations concernant une balise
    """
    def __init__(self,width=1, length=1, colors=None):
        """
        Initialise une balise avec 4 couleurs
        :param couleurs: [tuple[4]] (r, g, v, o)
        """
        Objet3D.__init__(self, centre=Point(0,0,0))
        if colors is None:
            colors = [(255, 0, 0, 255), (0, 255, 0, 255),  (255,255,0,255), (0,0,255,255)]
        self.colors=colors

        self.length=length
        self.width=width

    def __dict__(self):
        dct = OrderedDict()
        dct["__class__"]=Balise.__name__
        dct["colors"] = list(self.colors)
        dct["width"] = self.width
        dct["length"] = self.length
        return dct

    @staticmethod
    def hook(dct):
        if not "__class__" in dct.keys():
            return dct
        if dct["__class__"]==Balise.__name__:
            return Balise(dct["width"], dct["length"], dct["colors"])

    def clone(self):
        return Balise(self.width, self.length, list(self.colors))
