from gl_lib.sim.geometry import Arene, AreneFermee, Pave, Polygone3D
from gl_lib.sim.geometry.point import Point, Vecteur
from math import pi
from gl_lib.config import RES_M


class VueMatriceArene(object):
    """
    definit une view matricielle de l'arene
    """
    res = RES_M

    def __init__(self, arene: Arene, origine=Point(0, 0, 0), ox=Vecteur(1, 0, 0), ajuste=False):
        """
        Initialise la matrice
        :param arene: representre
        """
        self.origine = origine
        self.arene = arene
        self.ox = ox
        self.ajuste = ajuste

    def vueDessus(self, dx, dy):
        """
        N'affiche que les paves dans la matrice

        S'appuie sur une rotation du repere, pour resoudre les cas ou les sommets
        du rectangle ont tous des coordonnees differentes

        :param origine: point autour duquel on va representer la matrice
        :param dx: dimension x d'display de l'arene
        :param dy: dimension y d'display de l'arene
        :return: [[Bool]]
        """
        # on part du principe qu'aucun point n'est dans un pave
        ox = self.ox.clone() / VueMatriceArene.res
        ox.rotate(pi / 2 + pi)
        if self.ajuste:
            ox.rotate(pi / 4)
        oy = ox.clone()
        oy.rotate(pi / 2)
        nxmax = int(dx / ox.get_mag())
        nymax = int(dy / oy.get_mag())

        # matrice2d: [[int]]
        matrice2d = [[0] * nymax for _ in range(nxmax)]
        # on part du principe qu'aucun point n'est dans un pave
        for obj in self.arene.objets3D:
            # obj: Objet3D
            if issubclass(type(obj), Pave):
                # on commence par recuperer les infos importantes sur le pave
                # ls: [Point]
                ls = obj.vertices
                # inclinaison_m: float
                inclinaison_m = (ls[0] - ls[1]).to_vect().get_angle()


                # on recupere les coordonnees limites des sommets
                s_xmax = int(max(ls[i].x for i in range(0, len(ls))))
                s_ymax = int(max(ls[i].y for i in range(0, len(ls))))
                s_xmin = int(min(ls[i].x for i in range(0, len(ls))))
                s_ymin = int(min(ls[i].y for i in range(0, len(ls))))

                pmax=(oy+ox)*max(dx,dy)/(oy+ox).get_mag()
                for x in range(nxmax):
                    for y in range(nymax):
                        p = Point(pmax.x*(float(x)/nxmax), pmax.y*(float(y)/nymax), 0)
                        #aux: point p dans le nouveau repere
                        aux = self.origine + p
                        aux.rotate_around(obj.centre, inclinaison_m)
                        if s_xmin <= aux.x <= s_xmax and s_ymin <= aux.y <= s_ymax:
                            matrice2d[x][y] = 1
        return matrice2d

    def __repr__(self):
        """
        retourne un display sous forme de tableau
        :return: string
        """
        for i in range(0, len(self.m)):
            print(m[i])
        print("\nattributs matrice: ", vmatrice.ox, vmatrice.origine)


if __name__ == '__main__':

    p = Pave(5, 5, 0)
    p.move(Vecteur(5, 5, 0) * -1)
    a = Arene(objets3D=[p])
    v = Vecteur(0, 1, 0)
    vmatrice = VueMatriceArene(a, ox=v, ajuste=True)
    m = vmatrice.vueDessus(20, 20)
    # 1: largeur en x de la matrice
    # 2: lngueur en y
    # 3: origine

    n = 10
    rotation = 2 * pi / n
    for i in range(n + 1):
        p.rotate_around(vmatrice.origine, rotation)
        vmatrice.ox = (p.centre - vmatrice.origine).to_vect().norm()
        m = vmatrice.vueDessus(30, 30)

        for i in range(0, len(m)):
            print(m[i])
        print("\nattributs matrice: ", vmatrice.ox, vmatrice.origine)
        print()
