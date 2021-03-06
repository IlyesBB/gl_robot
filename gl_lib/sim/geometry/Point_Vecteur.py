# -*- coding: utf-8 -*-
import json
from math import *
from gl_lib.config import PIX_PAR_M
from gl_lib.sim.geometry.fonctions import positive_angle
from collections import OrderedDict
from gl_lib.utils import Serializable


class Point(Serializable):
    """
        Classe définissant un point dans un espace 3D par 3 coordonnées
    """

    def __init__(self, x, y, z, type_coords=float):
        """
        Initialise les coordonnées du point
        :param x: Coordonnée en x
        :type x: float
        :param y: Coordonnée en y
        :type y: float
        :param z: Coordonnée en z
        :type z: float
        :param type_coords: Permet de passer de flottant à entier
        :type type_coords: type
        """
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
        if type_coords == int:
            self.x = int(self.x)
            self.y = int(self.y)
            self.z = int(self.z)

    def __dict__(self):
        dct = OrderedDict()
        dct["__class__"] = Point.__name__
        dct["x"] = self.x
        dct["y"] = self.y
        dct["z"] = self.z
        return dct

    def __repr__(self):
        """
        Quand on entre un vecteur dans l'interpreteur
        """
        return "Point(x={}, y={}, z={})".format(self.x, self.y, self.z)

    def __str__(self):
        return "p({:6.6},{:6.6},{:6.6})".format(self.x, self.y, self.z)

    def __getattr__(self, nom):
        print("L'attribut {} n'est pas accessible dans {} !".format(nom, type(self)))

    def __add__(self, vp):
        """
        A   ddition. Dans ce sens, renvoi un Point que vp soit un vecteur ou un point
        """
        if issubclass(type(vp), Point) or issubclass(type(vp), Vecteur):
            return Point(self.x + vp.x, self.y + vp.y, self.z + vp.z)

    def __sub__(self, vp):
        """
            Soustraction. Dans ce sens, renvoi un vecteur que vp soit un vecteur ou un point
        """
        if issubclass(type(vp), Point) or issubclass(type(vp), Vecteur):
            return Point(self.x - vp.x, self.y - vp.y, self.z - vp.z)

    def __radd__(self, vp):
        """
            Addition inverse. Dans ce sens, peut renvoyer un Vecteur, si vp en est un
        """
        if issubclass(type(vp), Vecteur):
            return Vecteur(self.x + vp.x, self.y + vp.y, self.z + vp.z)
        elif issubclass(type(vp), Point):
            return self + vp

    def __rsub__(self, vp):
        """
            Soustraction inverse. Dans ce sens, peut renvoyer un Point, si vp en est un
        """
        if issubclass(type(vp), Vecteur):
            return Vecteur(vp.x - self.x, vp.y - self.y, vp.z - self.z)
        if issubclass(type(vp), Point):
            return self - vp

    def __truediv__(self, n: int or float):
        """
            Division des coordonnees par un reel
        """
        try:
            if isinstance(n, int):
                return Point(self.x / float(n), self.y / float(n), self.z / float(n))
            elif isinstance(n, float):
                return Point(self.x / n, self.y / n, self.z / n)
        except ArithmeticError:
            # En cas de division par zéros
            return None

    def __eq__(self, point):
        """
        Quand on teste l'egalite
        """
        if issubclass(type(point), Point):
            if self.x == point.x and self.y == point.y and self.z == point.z:
                return True
        return False

    def __ne__(self, point):
        """
        Quand on teste l'inegalite
        """
        if self == point:
            return False
        return True

    def __mul__(self, vi):
        """
        multiplication par une constate reelle
        """

        if isinstance(vi, float):
            return Point(self.x * vi, self.y * vi, self.z * vi)
        if isinstance(vi, int):
            return Point(float(self.x * vi), float(self.y * vi), float(self.z * vi))

    def set_position(self, point):
        """
           Modifie les coordonnées du point

        :param point: Point dont on va copier les coordonnées
        :param point: Point

        """
        if issubclass(type(point), Point):
            self.x = point.x
            self.y = point.y
            self.z = point.z

    def move(self, vecteur):
        """
            Déplace le point d'un vecteur (dx, dy, dz)

        :param vecteur: Vecteur déplacement
        :type vecteur: Vecteur

        """
        if issubclass(type(vecteur), Point) or issubclass(type(vecteur), Vecteur):
            self.set_position(self + vecteur)
        return self

    def rotate_around(self, point, teta, axis=None):
        """
        Tourne le point courant autour du point en argument de teta
        :param point: Point autour duquel tourner
        :type point: Point
        :param teta: Angle en radians
        :type teta: float
        :param axis: 'z', 'x' ou 'y'
        """
        # v: Vecteur

        v = (self - point).to_vect()
        v.rotate(teta, axis)
        # dans ce sens, l'addition renvoi un Vecteur
        self.set_position(point + v)
        return self

    def to_vect(self):
        """
            Convertit self en vecteur et le renvoi

        :return: Vecteur
        """
        return Vecteur(self.x, self.y, self.z)

    def to_tuple(self, type_coords=float):
        """
            Conversion en tuple

        :return: Tuple

        """
        if type_coords is float:
            return self.x, self.y, self.z
        elif type_coords is int:
            return int(self.x), int(self.y), int(self.z)

    def clone(self, type_coords=float):
        """
        clone le point
        :return: Point
        """
        return Point(self.x, self.y, self.z, type_coords)

    @staticmethod
    def hook(dct):
        if dct["__class__"] == Point.__name__:
            return Point(dct["x"], dct["y"], dct["z"])

    @staticmethod
    def load(filename):
        """
            Permet de charger un objet Point depuis un fichier au format json adapté

        :param filename: Nom du fichier

        """
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f, object_hook=Point.hook)


# ______________________________________________________________________________________________________________________#

class Vecteur(Serializable):
    """
        Définit tdes methodes de calcul sur les vecteurs
    """

    def __init__(self, x: int or float, y: int or float, z: int or float, echelle=True):
        """
            Intialise les coordonnées
        """
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
        if not echelle:
            self.x = float(x) * PIX_PAR_M
            self.y = float(y) * PIX_PAR_M
            self.z = float(z) * PIX_PAR_M

    def __dict__(self):
        dct = OrderedDict()
        dct["__class__"] = Vecteur.__name__
        dct["x"] = self.x
        dct["y"] = self.y
        dct["z"] = self.z
        return dct

    def __mul__(self, vi):
        """
            Produit scalaire ou multiplication par une constate réelle
        """
        if issubclass(type(vi), Vecteur):
            return self.x * vi.x + self.y * vi.y + self.z * vi.z
        if isinstance(vi, float):
            return Vecteur(self.x * vi, self.y * vi, self.z * vi)
        if isinstance(vi, int):
            return Vecteur(float(self.x * vi), float(self.y * vi), float(self.z * vi))

    def __rmul__(self, vi):
        """
            Produit scalaire ou multiplication par une constate réelle inverse
        """
        return self * vi

    def __pow__(self, vecteur):
        """
            Produit vectoriel
        """
        if issubclass(type(vecteur), Vecteur):
            return Vecteur(self.y * vecteur.z - self.z * vecteur.y, self.z * vecteur.x - self.x * vecteur.z,
                           self.x * vecteur.y - self.y * vecteur.x)

    def __add__(self, vp):
        """
         Addition. Dans ce sens, renvoi un vecteur que vp soit un vecteur ou un point
        """
        if issubclass(type(vp), Point) or issubclass(type(vp), Vecteur):
            return Vecteur(self.x + vp.x, self.y + vp.y, self.z + vp.z)

    def __sub__(self, point: Point):
        """
            Soustraction. Dans ce sens, renvoi un vecteur que vp soit un vecteur ou un point
        """
        if issubclass(type(point), Point) or issubclass(type(point), Vecteur):
            return Vecteur(self.x - point.x, self.y - point.y, self.z - point.z)

    def __truediv__(self, n):
        """
            Division des coordonnées par un réel
        """
        try:
            if isinstance(n, int):
                return Vecteur(self.x / float(n), self.y / float(n), self.z / float(n))
            elif isinstance(n, float):
                return Vecteur(self.x / n, self.y / n, self.z / n)
        except ArithmeticError:
            # float division by zero
            pass

    def __repr__(self):
        """
        Quand on entre un vecteur dans l'interpreteur
        """
        return "Vecteur(x={}, y={}, z={})".format(self.x, self.y, self.z)

    def __str__(self):
        return "v({:6.6},{:6.6},{:6.6})".format(self.x, self.y, self.z)

    def __getattr__(self, nom):
        """
        Permet d'acceder a un attribut. si ce n'est pas possible:
        """
        print("L'attribut {} n'est pas accessible dans {} !".format(nom, type(self)))

    def __eq__(self, vecteur):
        """
        Quand on teste l'egalite
        """
        if issubclass(type(vecteur), Vecteur):
            if self.x == vecteur.x and self.y == vecteur.y and self.z == vecteur.z:
                return True

        return False

    def __ne__(self, vecteur):
        """
        Quand on teste l'inegalite
        """
        if self == vecteur:
            return False
        return True

    def get_angle(self, axe='z', signe=None):
        """
            Retourne l'angle du vecteur par rapport a la verticale, dans le sens trigo, entre pi et -pi

            Peut être spécifié autrement, en donnant un nombre positif en argument avec signe

        :param axe: 'z', 'x' ou 'y'
        :param signe: Positif ou négatif
        :type signe: float

        """
        if axe == 'z':
            a1 = self.diff_angle(Vecteur(1, 0, 0))
        elif axe == 'x':
            v1 = self.clone()
            aux = v1.x
            v1.x = v1.y
            v1.y = aux

            aux = v1.z
            v1.z = v1.y
            v1.y = aux
            a1 = v1.diff_angle(Vecteur(1, 0, 0))
        else:
            v1 = self.clone()

            aux = v1.z
            v1.z = v1.x
            v1.x = aux
            a1 = v1.diff_angle(Vecteur(1, 0, 0))

        if signe is not None:
            if signe >= 0:
                return positive_angle(-a1)
            else:
                return (2 * pi) * positive_angle(-a1)
        else:
            return -a1

    def diff_angle(self, vecteur, signe=None):
        """
            Retourne la différence d'angle entre 2 vecteurs par rapport à Oz

        :param vecteur: Vecteur à comparer avec self
        :type vecteur: Vecteur
        :param signe: Signe de l'angle à retourner
        :type signe: float

        """
        # v: Vecteur
        angle = None
        v = self ** vecteur
        if self != Vecteur(0.0, 0.0, 0.0) and vecteur != Vecteur(0.0, 0.0, 0.0):
            # utilise les proprietes du produit vectoriel pour determiner si l'angle est positif ou negatif
            res = (self * vecteur) / (self.get_mag() * vecteur.get_mag())
            if v.z > 0:
                # si v est a gauche
                try:
                    angle = acos(res)
                except:
                    angle = acos(res % 1)
            elif v.z < 0:
                # si v est a droite
                try:
                    angle = -acos(res)
                except:
                    angle - acos(res % 1)
            else:
                if self == vecteur:
                    angle = 0
                else:
                    angle = pi
            if signe is not None:
                if signe > 0:
                    angle = positive_angle(angle)
                elif signe < 0:
                    angle = positive_angle(angle) - 2 * pi
            return angle

    def get_mag(self):
        """
            Retourne la norme du vecteur
        """
        return sqrt(pow(self.x, 2) + pow(self.y, 2) + pow(self.z, 2))

    def rotate(self, teta: float, axis=None):
        """
            Tourne le vecteur d'un angle teta, selon z  par défaut

        :param teta: Angle en radians
        :type teta: float
        :param axis: 'z', 'x' ou 'y'

        """
        if axis is None:
            # x: Copie de self.y
            x = self.x

            self.x = x * cos(teta) - self.y * sin(teta)
            self.y = x * sin(teta) + self.y * cos(teta)

        elif axis == 'x':
            # y: Copie de self.y
            y = self.y

            self.y = y * cos(teta) - self.z * sin(teta)
            self.z = y * sin(teta) + self.z * cos(teta)

        elif axis == 'y':
            # z: Copie de self.z
            z = self.z

            self.z = z * cos(teta) - self.x * sin(teta)
            self.x = z * sin(teta) + self.x * cos(teta)

        return self

    def to_point(self):
        """
            Conversion en point

        :return: Point

        """
        return Point(self.x, self.y, self.z)

    def to_tuple(self, type_coords=float):
        """
            Conversion en tuple

        :return: tuple

        """
        if type_coords is float:
            return self.x, self.y, self.z
        elif type_coords is int:
            return int(self.x), int(self.y), int(self.z)

    def clone(self):
        return Vecteur(self.x, self.y, self.z)

    def norm(self):
        """
            Norme le vecteur

        :return: Vecteur

        """
        return self / self.get_mag()

    @staticmethod
    def hook(dct):
        if dct["__class__"] == Vecteur.__name__:
            return Vecteur(dct["x"], dct["y"], dct["z"])

    @staticmethod
    def load(filename):
        """
            Permet de charger un objet Vecteur depuis un fichier au format json adapté

        :param filename: Nom fichier

        """
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f, object_hook=Vecteur.hook)


if __name__ == '__main__':
    v = Vecteur(1, 1, 1)
    import os

    os.chdir("/home/ilyes/")

    d = v.__dict__()
    v.save("vector.json")

    v3 = Vecteur.load("vector.json")
    print(v3)

    p = Point(2, 2, 2)

    d2 = p.__dict__()
    print(d2)
    p.save("dot.json")

    p3 = Point.load("dot.json")
    print(p3)
