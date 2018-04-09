from gl_lib.sim.geometry import Arene, AreneFermee, Pave, Polygone3D
from gl_lib.sim.geometry.point import Point, Vecteur
from math import pi
from gl_lib.sim.robot import Robot
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
        ox = self.ox.clone()
        if self.ajuste:
            ox.rotate(-pi / 4)
        oy = ox.clone()
        oy.rotate(pi / 2)
        nxmax = int(dx * VueMatriceArene.res)
        nymax = int(dy * VueMatriceArene.res)

        # matrice2d: [[int]]
        matrice2d = [[0] * nymax for _ in range(nxmax)]
        # on part du principe qu'aucun point n'est dans un pave
        for obj in self.arene.objets3D:
            # obj: Objet3D
            if issubclass(type(obj), Pave):
                # on commence par recuperer les infos importantes sur le pave
                # ls: [Point]
                ls = obj.clone().vertices
                inclinaison_m = (ls[0] - ls[1]).to_vect().diff_angle(ox)

                ls= obj.clone().rotate(inclinaison_m).vertices

            elif issubclass(type(obj), Robot):
                ls = obj.forme.clone().vertices
                inclinaison_m = (ls[0] - ls[1]).to_vect().diff_angle(ox)
                ls= obj.forme.clone().rotate(-inclinaison_m).vertices

            else:
                continue

            centre=obj.centre.clone()
            # inclinaison_m: float

            # on recupere les coordonnees limites des sommets
            s_xmax, s_ymax = max(ls[i].x for i in range(0, len(ls))), max(ls[i].y for i in range(0, len(ls)))
            s_xmin, s_ymin = min(ls[i].x for i in range(0, len(ls))), min(ls[i].y for i in range(0, len(ls)))

            print(s_xmin, s_xmax, s_ymin, s_ymax)
            for x in range(nxmax):
                for y in range(nymax):
                    p = (ox*x+oy*y).to_point()/VueMatriceArene.res
                    #aux: point p dans le nouveau repere
                    aux = self.origine + p
                    aux=aux.rotate_around(centre, inclinaison_m).clone()
                    if s_xmin <= aux.x <= s_xmax and s_ymin <= aux.y <= s_ymax:
                        if nxmax > aux.x > -1 and nymax > aux.y > -1:
                            try:
                                matrice2d[x][y] = 1
                            except:
                                pass
        return matrice2d

    def __repr__(self):
        """
        retourne un display sous forme de tableau
        :return: string
        """
        print("\nox : ", self.ox,"\norigine: ",self.origine)

