from gl_lib.sim.geometry.point import Point

class Objet3D(object):
    """
    Classe definissant un objet 3D de facon abstraite
    """

    def __init__(self, centre=Point(0,0,0)):
        """
        centre : Point definissant le centre de l'objet. initialise a (0, 0, 0)
        """
        self.centre = centre.clone()

    def move(self, vecteur):
        """
        deplace les Point dans sommets et centre de l'objet
        """
        self.centre.move(vecteur)

    def rotate_around(self, point, teta):
        """
        tourne l'objet d'un angle teta auout d'un point
        :param point: Point
        :param teta: float en rad
        """
        self.centre.rotate_around(point, teta)

    def __repr__(self):
        """
        Quand on entre un objet3D dans l'interpreteur
        """
        return "Objet3D: centre: {}".format(self.centre)

    def __getattr__(self, nom):
        """
        Permet d'acceder a un attribut

        si ce n'est pas possible:
        """
        print("L'attribut {} n'est pas accessible dans {} !".format(nom, type(self)))
