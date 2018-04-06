from gl_lib.sim.robot.sensor import Capteur

from math import pi
from gl_lib.sim.geometry.point import Vecteur, Point
from gl_lib.sim.geometry import Arene
from gl_lib.sim.display.d2.view import VueMatriceArene
from gl_lib.config import PAS_IR


class CapteurIR(Capteur):
    """
    Capteur qui renvoi la distance du prochain pavé dans la trajectoire de sa direction en mètres
    """
    # Pas de recherche d'un obstacle
    dp = PAS_IR

    def __init__(self, centre: Point = Point(0, 0, 0), direction: Vecteur = Vecteur(1, 0, 0), portee: int or float = 10,
                 tete=None):
        Capteur.__init__(self, centre=centre, direction=direction, tete=tete)
        self.portee = portee

    def creer_matrice(self, arene: Arene):
        return VueMatriceArene(arene, origine=self.centre, ox=self.direction, ajuste=True).vueDessus(self.portee,
                                                                                                     self.portee)

    def mesure(self, arene: Arene):
        """
        Retourne la distance entre le sensor et le premier objet dans la matrice cf dessous
        Retourne -1 si pas d'obstacle detecte

        :param arene: arène dans laquelle effectuer la mesure
        :return: float ou int
        """
        m = self.creer_matrice(arene)

        # On parcours la matrice sur la diagonale, dans le sens croissant
        # ce qui correspond a la vue ajustée de la matrice
        pmax = Point(len(m), len(m[0]), 0)
        n = int(self.portee / CapteurIR.dp)
        for cpt in range(n):
            coef = float(cpt) / n
            pos = Point(pmax.x * coef, pmax.y * coef, 0)
            try:
                if m[int(pos.x)][int(pos.y)] == 1:
                    return float(cpt) * CapteurIR.dp
            except:
                print(pos, " est hors de portee")
        return -1


if __name__ == '__main__':
    from gl_lib.sim.robot import RobotPhysique, Tete
    from gl_lib.sim.geometry import Pave

    c = CapteurIR(centre=Point(0, 0, 0), direction=Vecteur(1, 0, 0))

    p = Pave(5, 5, 0)
    p.move(Vecteur(7, 0, 0))

    a = Arene([p])

    n = 4
    rotation = 2 * pi / n

    # Le sensor suit le pave, et on affiche la mesure a chaque rotation
    for rot in range(n):
        p.rotate_around(Point(0, 0, 0), rotation)
        c.direction = ((p.centre - c.centre).to_vect().norm())
        m = c.creer_matrice(a)
        print("mesure :", c.mesure(a))
        for i in range(0, len(m)):
            print(m[i])
