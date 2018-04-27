
from gl_lib.sim.geometry import Objet3D, Point


class Cylindre(Objet3D):
    """
        Définit géométriquement un cylindre
    """
    def __init__(self,centre=Point(0,0,0), diametre=0.5, height=1):
        """

        :param centre: Centre du cylindre
        :type centre: Point
        :param diametre: Diametre du cylindre
        :type diametre: float
        :param height: Hauteur du cylindre
        :type height: float

        """
        Objet3D.__init__(self, centre)
        self.diametre = diametre
        self.height = height