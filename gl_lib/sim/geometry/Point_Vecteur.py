from math import *
from gl_lib.config import PIX_PAR_M
from gl_lib.sim.geometry.fonctions import positive_angle


class Point(object):
    """
    Classe definissant un point dans un espace 3D (x,y,z)
    x : coordonnee en x
    y : coordonnee en y
    z : coordonnee en z
    """

    def __init__(self, x: object, y: object, z: object, type_coords: object = float) -> object:
        """
        Initialise les coordonnees du point 
        """
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
        if type_coords == int:
            self.x = int(self.x)
            self.y = int(self.y)
            self.z = int(self.z)

    def set_position(self, point):
        """
        Modifie les coordonnees du point
        """
        if issubclass(type(point), Point):
            self.x = point.x
            self.y = point.y
            self.z = point.z

    def move(self, vecteur):
        """
        Deplace le point d'un vecteur (dx, dy, dz)
        """
        if issubclass(type(vecteur), Point) or issubclass(type(vecteur), Vecteur):
            self.set_position(self + vecteur)
        return self

    def rotate_around(self, point, teta: float, axis=None):
        """
        Tourne le point courant autour du point en argument de teta
        """
        # v: Vecteur

        v = (self - point).to_vect()
        v.rotate(teta, axis)
        # dans ce sens, l'addition renvoi un Vecteur
        self.set_position(point+v)
        return self

    def to_vect(self):
        """
        Converti le point en vecteur et 
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

    def __repr__(self):
        """
        Quand on entre un Point dans l'interpreteur
        """
        return "({:6.6}, ".format(self.x)+"{:6.6}, ".format(self.y)+"{:6.6})".format(self.z)


    def __getattr__(self, nom):
        """
        Permet d'acceder a un attribut. si ce n'est pas possible:
        """
        print("L'attribut {} n'est pas accessible dans {} !".format(nom, type(self)))

    def __add__(self, vp):
        """
        Addition. Dans ce sens, renvoi un Point que vp soit un vecteur ou un point
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
        division des coordonnees par un reel
        """
        if isinstance(n, int):
            return Point(self.x / float(n), self.y / float(n), self.z / float(n))
        elif isinstance(n, float):
            return Point(self.x / n, self.y / n, self.z / n)

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

    def clone(self, type_coords=float):
        """
        clone le point
        :return: Point
        """

        return Point(self.x, self.y, self.z, type_coords)


"""_______________________________________________________________________________________________________________"""


class Vecteur(object):
    """
    Defini des methodes de calcul sur les vecteurs
    """

    def __init__(self, x: int or float, y: int or float, z: int or float, echelle=True):
        """
        Intialise les coordonnees
        """
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
        if not echelle:
            self.x = float(x) * PIX_PAR_M
            self.y = float(y) * PIX_PAR_M
            self.z = float(z) * PIX_PAR_M

    def get_angle(self, axe='z', signe=None):
        """
        Retourne l'angle du vecteur 
        par rapport a la verticale,
        dans le sens trigo, entre pi et -pi
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
                return (2*pi)*positive_angle(-a1)
        else:
            return -a1

    def diff_angle(self, vecteur, signe=None):
        """
        retourne la difference d'angle entre 2 vecteurs dans le repere (x, y)
        """
        # v: Vecteur
        angle=None
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
                    angle -acos(res % 1)
            else:
                if self == vecteur:
                    angle = 0
                else:
                    angle = pi
            if signe is not None:
                if signe > 0:
                    angle = positive_angle(angle)
                elif signe < 0:
                    angle = positive_angle(angle)-2*pi
            return angle


    def get_mag(self):
        """
        Retourne la norme du vecteur
        """
        return sqrt(pow(self.x, 2) + pow(self.y, 2) + pow(self.z, 2))

    def rotate(self, teta: float, axis=None):
        """
        Tourne le vecteur d'un angle teta, selon z,  par défaut
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
        :return: Tuple
        """
        if type_coords is float:
            return self.x, self.y, self.z
        elif type_coords is int:
            return int(self.x), int(self.y), int(self.z)

    def clone(self):
        return Vecteur(self.x, self.y, self.z)

    def __mul__(self, vi):
        """
        produit scalaire ou multiplication par une constate reelle
        """
        if issubclass(type(vi), Vecteur):
            return self.x * vi.x + self.y * vi.y + self.z * vi.z
        if isinstance(vi, float):
            return Vecteur(self.x * vi, self.y * vi, self.z * vi)
        if isinstance(vi, int):
            return Vecteur(float(self.x * vi), float(self.y * vi), float(self.z * vi))

    def __rmul__(self, vi):
        """
        produit scalaire ou multiplication par une constate reelle
        """
        return self * vi

    def __pow__(self, vecteur):
        """
        produit vectoriel 
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
        division des coordonnees par un reel
        """
        try:
            if isinstance(n, int):
                return Vecteur(self.x / float(n), self.y / float(n), self.z / float(n))
            elif isinstance(n, float):
                return Vecteur(self.x / n, self.y / n, self.z / n)
        except:
            # float division by zero
            pass

    def __repr__(self):
        """
        Quand on entre un vecteur dans l'interpreteur
        """
        return "v->({:6.6}, ".format(self.x)+"{:6.6}, ".format(self.y)+"{:6.6})".format(self.z)

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

    def norm(self):
        """
        Norme le vecteur
        :return: Vecteur
        """
        return self / self.get_mag()


if __name__ == '__main__':
    p=Point(0,0,0)
    p2=p
    p2.move(Vecteur(1,1,0))
    print(p,p2)