from gl_lib.sim.geometry import Objet3D, Vecteur, Point


class Dirigeable(Objet3D):
    def __init__(self, centre:Point=Point(0,0,0), direction:Vecteur=Vecteur(1,0,0)):
        Objet3D.__init__(self, centre)
        self.direction = direction

    def rotate(self, teta:int or float, axis=None):
        self.direction.rotate(teta, axis)