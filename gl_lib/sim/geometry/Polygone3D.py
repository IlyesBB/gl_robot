from gl_lib.sim.geometry import Objet3D, Point, Vecteur

class Polygone3D(Objet3D):
    """
    Classe definissant un polygone de facon abstraite
    """

    def __init__(self, centre=Point(0,0,0), vertices=None):
        """
        initialise la liste des sommets
        """
        Objet3D.__init__(self, centre=centre)
        self.vertices=list()
        if vertices is not None:
            self.add_vertices(vertices)



    def add_vertex(self, sommet):
        """
        ajoute sommet a la liste sommets du polygone
        """
        self.vertices.append(sommet.clone())

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
        return self
        #on ne verifie pas que vecteur est bien definit
        #car c'est une classe abstraite

    def __repr__(self):
        """
        Quand on entre un Polygone3D dans l'interpreteur
        """
        return str(type(self))+" Center: {}\nVertices[{}]({})".format(self.centre, len(self.vertices), self.vertices)


if __name__=='__main__':
    from gl_lib.sim.geometry import *
    p=Pave(10,10,0)
    p2=p.clone()
    print(p2)
    p2.move(Vecteur(10, 0, 0))
    print(p2)
