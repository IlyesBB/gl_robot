from gl_lib.sim.geometry.Objet3D import Objet3D
from gl_lib.sim.geometry.point import Point, Vecteur

class Polygone3D(Objet3D):
    """
    Classe definissant un polygone de facon abstraite
    """

    def __init__(self, centre=Point(0,0,0), sommets=None):
        """
        initialise la liste des sommets
        """
        Objet3D.__init__(self, centre=centre)
        self.vertices=list()
        if sommets is not None:
            self.vertices=sommets

    def add_vertex(self, sommet:Point):
        """
        ajoute sommet a la liste sommets du polygone
        """
        if issubclass(type(sommet), Point):
            self.vertices.append(sommet)

    def add_vertices(self, sommets):
        """
        Ajoute les points les uns après les autres
        :param sommets:
        :return:
        """
        for vertex in sommets:
            self.add_vertex(vertex)

    def move(self, vecteur:Vecteur):
        """
        deplace les sommets et le centre
        """
        Objet3D.move(self, vecteur)
        for s in self.vertices:
            s.move(vecteur)
        #on ne verifie pas que vecteur est bien definit
        #car c'est une classe abstraite

    def __repr__(self):
        """
        Quand on entre un Polygone3D dans l'interpreteur
        """
        return "Polygone3D: centre: {}, liste de sommets[{}]({})".format(self.centre, len(self.vertices), self.vertices)



    def clone(self):
        l = [s.clone() for s in self.vertices]
        p=Polygone3D(sommets=l)
        return p

if __name__=='__main__':
    from gl_lib.sim.geometry import *
    p=Pave(10,10,0)
    p2=p.clone()
    print(p2)
    p2.move(Vecteur(10, 0, 0))
    print(p2)