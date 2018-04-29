# -*- coding: utf-8 -*-
from gl_lib.sim.geometry import Arene


class AreneFermee(Arene):
    """
        définit une arène avec des limites
    """

    def __init__(self, height = 10, width = 10, length = 10):
        """
        :param height: Hauteur de l'arène
        :type height: float
        :param width: Largeur de l'arène
        :type width: float
        :param length: Longueur de l'arène
        :type length: float
        """
        Arene.__init__(self)
        self.height = height
        self.width = width
        self.length = length


if __name__ == '__main__':
    print(AreneFermee())
