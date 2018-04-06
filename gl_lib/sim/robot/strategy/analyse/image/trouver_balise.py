from gl_lib.sim.robot.strategy import Strategie
from gl_lib.sim.geometry import *
from gl_lib.sim.geometry.point import *
import imageio as imo
import os
from math import pi
from gl_lib.config import PIX_PAR_M


def trouver_balise(im, couleurs: [tuple]):
    """
    Retourne le centre de la balise sur l'image

    Si pas de matrice, retourne le vide

    :param couleurs: les 4 couleurs de la balise (avec leur opacite)
    :return: Point
    """
    PAS_RECH = 20
    pas = int(PAS_RECH)
    RAYON_RECH = 4
    w_im, l_im = int(im.shape[0] - 1), int(im.shape[1] - 1)
    i0 = int(RAYON_RECH / PAS_RECH)

    for x in [i * pas for i in range(i0, int(w_im / pas) - i0)]:
        for y in [i * pas for i in range(i0, int(l_im / pas) - i0)]:
            balise = True
            # Teste dans les axes
            signes = [(-1, -1), (1, -1), (1, 1), (-1, 1)]
            for l_couleurs in [couleurs, [couleurs[3-i] for i in range(4)]]:
                lc=l_couleurs
                for i in range(4):
                    signe = signes[i]
                    p = Point(x + signe[0] * RAYON_RECH, y + signe[1] * RAYON_RECH, 0).to_tuple(type_coords=int)
                    if lc[i] != tuple(im[p[0]][p[1]]):
                        balise = False
                if balise:
                    return Point(x, y, 0)

            # Teste dans les diagonales
            balise = True
            pave = Pave(RAYON_RECH * 2, RAYON_RECH * 2, 0, centre=Point(x, y, 0))
            for l_couleurs in [couleurs, [couleurs[3-i] for i in range(4)]]:
                lc=l_couleurs
                for i in range(4):
                    p = pave.vertices[i].to_tuple(type_coords=int)
                    if lc[i] != tuple(im[p[0]][p[1]]):
                        balise = False
                if balise:
                    return Point(x, y, 0)
    return None


def ajouterBalise(im, couleurs: [tuple], pave):
    p = pave
    xmin = int(min(p.vertices[i].x for i in range(len(p.vertices))))
    ymin = int(min(p.vertices[i].y for i in range(len(p.vertices))))
    xmax = int(max(p.vertices[i].x for i in range(len(p.vertices))))
    ymax = int(max(p.vertices[i].y for i in range(len(p.vertices))))
    print(xmin,ymin,xmax,ymax)
    y2 = int(ymin+(ymax - ymin) / 2)
    x2 = int(xmin+(xmax - xmin) / 2)

    im[xmin:x2, ymin:y2] = couleurs[0]
    im[x2:xmax, ymin:y2] = couleurs[1]
    im[x2:xmax, y2:ymax] = couleurs[2]
    im[xmin:x2, y2:ymax] = couleurs[3]

    return im


def trouverAngleBalise(couleurs: tuple, im):
    """
    utilise trouverBalise, et retourne l'angle par rapport a la verticale
    :param couleurs:
    :return:
    """
    res = trouver_balise(im, couleurs)
    if res is not None:
        v = (Point(im.shape[0] / 2, im.shape[1]/2, 0) - res).to_vect().norm()
        return v.diff_angle(Vecteur(0, 1, 0))
    return None


if __name__ == '__main__':
    im = imo.imread('screenshot.png')

    #on ajoute une balise artificiellement
    p=Pave(100, 100, 0,centre=Point(im.shape[0]/4,im.shape[1]/4,0))
    couleurs = [(255, 0, 0, 255), (0, 255, 0, 255), (0, 0, 255, 255), (255, 255, 0, 255)]
    im=ajouterBalise(im, couleurs, pave=p)
    imo.imsave("screenphotMod.png", im)

    print(trouverAngleBalise(couleurs, im))
    print(p)
