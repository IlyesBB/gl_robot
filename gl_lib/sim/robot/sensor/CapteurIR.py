# -*- coding: utf-8 -*-
import json
import os
import pdb
from collections import OrderedDict

from gl_lib.sim.robot.sensor import Capteur
from math import pi
from gl_lib.sim.geometry import Arene, ApproximableAPave, Point, Vecteur, Objet3D
from gl_lib.config import PAS_IR, RES_M


class CapteurIR(Capteur):
    """
    Capteur qui renvoi la distance du prochain pavé dans la trajectoire de sa direction en mètres
    """
    # Pas de recherche d'un obstacle
    dp = PAS_IR

    def __init__(self, centre: Point = Point(0, 0, 0), direction: Vecteur = Vecteur(1, 0, 0), portee: int or float = 3,
                 arena_v=None, l_ignore=list()):
        Capteur.__init__(self, centre=centre, direction=direction)
        self.portee = portee
        self.arena_v = arena_v
        self.l_ignore = l_ignore

    def __dict__(self):
        dct = OrderedDict()
        dct["__class__"] = CapteurIR.__name__
        dct["centre"] = self.centre.__dict__()
        dct["direction"] = self.direction.__dict__()
        dct["portee"] = self.portee
        if self.l_ignore is not None and len(self.l_ignore) > 0:
            dct["l_ignore"] = [self.l_ignore[i].__dict__() for i in range(len(self.l_ignore))]
        else:
            dct["l_ignore"] = None
        if self.arena_v is not None:
            dct["arena_v"] = self.arena_v.__dict__()
        else:
            dct["arena_v"] = None
        return dct

    def __eq__(self, other):
        if self.centre != other.centre:
            return False
        if self.portee != other.portee:
            return False
        if self.direction != other.direction:
            return False
        return True

    def __str__(self):
        s = "{}; portee: {}".format(self.__class__.__name__, self.portee)
        return s

    def get_matrix_view(self, arene):
        """
            Crée une nouvelle vue matricielle de l'arène, la sauvegarde et la renvoie

        :param arene: Arène à analyser
        :type arene: Arene
        :return: VueMatriceArene

        """
        self.arena_v = VueMatriceArene(arene, origine=self.centre, ox=self.direction, ajuste=True)
        return self.arena_v

    def get_mesure(self, arene, d_ignore=0.0, ignore=None):
        """
            Retourne la distance entre le capteur et le premier objet dans la matrice
            Retourne -1 si pas d'obstacle detecté

        :param arene: arène dans laquelle effectuer la mesure
        :type arene: Arene
        :param d_ignore: Distance à partir de laquelle commencer à mesurer
        :type d_ignore: float
        :param ignore: Liste d'objets à masquer des mesures
        :type ignore: [Objet3D]
        :return: float ou None

        """
        self.get_matrix_view(arene)
        m = self.arena_v.vueDessus(self.portee, ignore)

        # On parcours la matrice sur la diagonale, dans le sens croissant
        # ce qui correspond a la vue ajustée de la matrice
        v = Vecteur(1, 1, 0).norm() * VueMatriceArene.res
        n = int(self.portee / CapteurIR.dp)
        for cpt in range(n):
            pos = (v * cpt * CapteurIR.dp).to_point().clone(type_coords=int)
            try:
                # Au cas ou on sortirait du tableau
                if m[int(pos.x)][int(pos.y)] == 1:
                    res = cpt * CapteurIR.dp
                    if res >= d_ignore:
                        return res
            except:
                print(pos, " est hors de portée")
        return -1

    @staticmethod
    def hook(dct):
        """
            On ne récupère pas la liste d'objest à ignorer
        """
        res = VueMatriceArene.hook(dct)
        if res is not None:
            return res
        if dct["__class__"] == CapteurIR.__name__:
            return CapteurIR(dct["centre"], dct["direction"], dct["portee"], dct["arena_v"], dct["l_ignore"])

    @staticmethod
    def load(filename):
        """
            Permet de charger un objet CapteurIR à partir d'un fichier au format json adapté

        :param filename: Nom du fichier

        """
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f, object_hook=CapteurIR.hook)




class VueMatriceArene(object):
    """
        Permet de représenter les objets héritant de ApproximableAPave (gl_lib.sim.gemoetry) d'une portion d'arène dans
        une matrice d'entiers


        On peut configurer la taille, l'axe Ox ainsi que l'origine du repère de la matrice
    """
    res = RES_M



    def __init__(self, arene: Arene = Arene(), origine: Point = Point(0, 0, 0), ox: Vecteur = Vecteur(1, 0, 0),
                 ajuste: bool = False, matrice: [[int]] = None):
        """
            Initialise la matrice
        :param arene: Arène dont on prélève une portion
        :param origine: Origine de la vue, dans le repère de l'arène
        :param ox: Direction horizontale de la vue, dans le repère de l'arène
        :param ajuste: On représente la matrice selon Ox tourné de -45 degrés dans le sens trigonométrique
        """
        self.origine = origine
        self.arene = arene
        self.ox = ox
        self.ajuste = ajuste
        self.matrice = matrice  # Destiné à stocker la dernière matrice crée

    def __str__(self):
        ox = self.ox.clone()
        if self.ajuste:
            ox.rotate(-pi / 4)
        s = "{}; origine: {}; Ox:".format(self.__class__.__name__, self.origine, self.ox)
        return s

    def __repr__(self):
        """
            Retourne une chaine décrivant précisemment la vue et la dernière matrice

        :return: string

        """
        s = str(self) + "\n"
        if self.matrice is not None:
            for i in range(len(self.matrice)):
                s += str(self.matrice[i]) + "\n"
        return s

    def __dict__(self):
        dct = OrderedDict()
        dct["__class__"] = "VueMatriceArene"
        dct["origine"] = self.origine.__dict__()
        dct["ox"] = self.ox.__dict__()
        dct["ajuste"] = self.ajuste
        dct["arene"] = self.arene.__dict__()
        if self.matrice is not None:
            dct["matrice"] = [list(self.matrice[i])
                              for i in range(len(self.matrice))]
        else:
            dct["matrice"] = None
        return dct

    def vueDessus(self, dx, ignore= None):
        """
            Crée une matrice d'entiers avec 1 si le point est à l'intérieur d'une forme et 0 sinon

            Cette méthode ne détecte que les pavés, et les robots ayant comme forme un pavé

            Procédure globale
            - Pour chaque objet, si on trouve un pavé:
            - Pour chaque point de la matrice, on vérifie s'il est dedans

        :param dx: Taille de la matrice
        :type dx: int
        :param ignore: Objets à ignorer dans l'arène
        :type ignore: [Objet3D]
        :return: [[int]]

        """
        ox = self.ox.clone()
        if self.ajuste:
            ox.rotate(-pi / 4)
        oy = ox.clone().rotate(pi / 2)
        nxmax = int(dx * VueMatriceArene.res)
        nymax = nxmax

        # matrice2d: [[int]]
        matrice2d = [[0] * nymax for _ in range(nxmax)]
        for obj in self.arene.objets3D:
            # obj: Objet3D

            # Si obj est un objet masqué, on passe à l'objet suivant
            if ignore is None:
                pass
            elif isinstance(ignore, list):
                if len(ignore) > 0:
                    for i in ignore:
                        if i == obj:
                            continue
            else:
                if ignore == obj:
                    continue

            # Si on ne peut pas récupérer les informations nécessaires au traitement, on passe
            # Sinon, on récupère les sommets du pavé, dans un repère où ce dernier est droit
            if issubclass(type(obj), ApproximableAPave):
                pave = obj.get_pave()
            else:
                continue
            # on commence par recuperer les infos importantes sur le pave
            ls = pave.vertices
            inclinaison_m = (ls[0] - ls[1]).to_vect().diff_angle(ox)
            if self.ajuste:
                inclinaison_ajuste = inclinaison_m - pi / 4
            else:
                inclinaison_ajuste = inclinaison_m
            ls = pave.clone().rotate(inclinaison_m).vertices
            centre = obj.centre.clone()

            # ls correspond ici aux sommets d'un pavé droit, on récupère dont ses coordonnées limites
            s_xmax, s_ymax = max(ls[i].x for i in range(0, len(ls))), max(ls[i].y for i in range(0, len(ls)))
            s_xmin, s_ymin = min(ls[i].x for i in range(0, len(ls))), min(ls[i].y for i in range(0, len(ls)))

            for x in range(nxmax):
                # x: int (coordonnée en x du point dans le repère de la vue, en 1/RES_M mètres)
                for y in range(nymax):
                    # y: int (coordonnée en y du point dans le repère de la vue, en 1/RES_M mètres)

                    # p: Point (coordonnées du point dans le repère de l'arène, en mètres)
                    p = self.origine + (ox * x + oy * y) / VueMatriceArene.res
                    # On met p dans le bon repère par rapport au pavé
                    p = p.rotate_around(centre, inclinaison_ajuste)

                    if s_xmin <= p.x <= s_xmax and s_ymin <= p.y <= s_ymax:
                        matrice2d[x][y] = 1

        self.matrice = matrice2d

        return matrice2d



    @staticmethod
    def hook(dct):
        """ On ne copie pas la liste d'objets à ingorer"""
        if dct["__class__"] == Point.__name__:
            return Point.hook(dct)
        elif dct["__class__"] == Vecteur.__name__:
            return Vecteur.hook(dct)
        elif dct["__class__"] == Arene.__name__:
            return Arene.hook(dct)
        elif dct["__class__"] == VueMatriceArene.__name__:
            return VueMatriceArene(dct["arene"], dct["origine"], dct["ox"], dct["ajuste"], dct["matrice"])

    @staticmethod
    def load(filename):
        """
            Charge un objet VueMatriceArene depuis un fichier au format json adapté

        :param filename:

        """
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f, object_hook=VueMatriceArene.hook)


if __name__ == '__main__':
    from gl_lib.sim.robot import RobotMotorise, Tete
    from gl_lib.sim.geometry import Pave
    from gl_lib.sim.robot.strategy.deplacement import DeplacementDroitAmeliore
    from gl_lib.sim import Simulation

    v = Vecteur(1, 1, 0).norm()

    c = CapteurIR()
    c.save("capteurIR.json")
    dct = c.__dict__()
    print(dct)
    c3 = CapteurIR.hook(dct)
    print(c3)

    # c2 = CapteurIR.load("capteurIR.json")
