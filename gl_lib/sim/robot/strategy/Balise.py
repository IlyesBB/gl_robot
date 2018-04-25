# -*- coding: utf-8 -*-
from collections import OrderedDict

from gl_lib.sim.geometry import *


class Balise(object):
    """
    Contient les informations concernant une balise
    """
    def __init__(self, width=1, length=1, height=1, colors=None):
        """
        Initialise une balise avec 4 couleurs
        :param couleurs: [tuple[4]] (r, g, v, o)
        """
        if colors is None:
            colors = [(255, 0, 0, 255), (0, 255, 0, 255),  (255,255,0,255), (0,0,255,255)]
        self.colors=colors

        self.width=width
        self.height=height
        self.length=length

    def __dict__(self):
        dct = OrderedDict()
        dct["__class__"]=Balise.__name__
        dct["colors"] = self.colors
        dct["width"] = self.width
        dct["length"] = self.length
        dct["height"] = self.height
        return dct

    @staticmethod
    def hook(dct):
        if dct["__class__"]==Balise.__name__:
            return Balise(dct["widtch"], dct["length"], dct["height"], dct["colors"])

    def clone(self):
        return Balise(self.width, self.length, self.height, list(self.colors))
