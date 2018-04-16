from gl_lib.sim.geometry import Arene


class AreneFermee(Arene):
    """
    definit une arene avec des limites
    """

    def __init__(self, height: int or float = 10, width: int or float = 10, length: int or float = 10):
        """
        :param height: hauteur
        :param width: largeur
        :param length: longueur
        """
        Arene.__init__(self)
        self.height = height
        self.width = width
        self.length = length


if __name__ == '__main__':
    print(AreneFermee())
