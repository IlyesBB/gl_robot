# -*- coding: utf-8 -*-
import numpy as np
from PIL import Image

from gl_lib.sim.geometry import *
from gl_lib.config import RATIO_SEARCH_SCREENSHOT


def trouver_balise(couleurs: [tuple],image=None,fname=None, output=None):
    """
    Retourne le centre de la balise sur l'image
    Les coordonnées sont pondérées par les mesures de l'image
    Par exemple, les coordonnées (0.5,0.5,0) indiquent que le centre repéré est
    au centre de l'image

    Si pas de balise trouvée, retourne None

    :param couleurs: les 4 couleurs de la balise (avec leur opacite)
    :return: Point or None
    """

    if fname is not None:
        im = Image.open(fname)
    elif image is not None:
        im = image
    else:
        return None
    w_im, l_im = image.size[0], image.size[1]
    PAS_RECH = min(w_im, l_im)/RATIO_SEARCH_SCREENSHOT
    pas = int(PAS_RECH)
    # Côté du carré cherché
    RAYON_RECH = PAS_RECH/2
    l_lvertices = [[0, 1, 2, 3]]
    i0 = int(RAYON_RECH / PAS_RECH)+1
    # Pour éviter que le carré cherché sorte du tableau

    centre_balise = None
    wn_im=int(w_im / pas)
    ln_im=int(l_im / pas)

    for x in [i * pas for i in range(i0, wn_im - i0)]:
        for y in [i * pas for i in range(i0, ln_im - i0)]:
            p0=Point(x,y,0)
            #print("\n","*"*10,p0, "*"*10)
            pave = Pave(RAYON_RECH * 2, RAYON_RECH * 2, 0, centre=p0.clone())
            for lvertices in l_lvertices:
                balise = True
                for i in range(len(couleurs)):
                    p = pave.vertices[lvertices[i]].to_tuple(type_coords=int)
                    if couleurs[i] != im.getpixel((p[0], p[1])):
                        #print(couleurs[i], " != ",im.getpixel((p[0], p[1])), (Point(p[0],p[1],0)-p0).to_vect(), "\n")
                        balise = False
                        break
                    #print(couleurs[i], " == ", im.getpixel((p[0], p[1])))

                if balise:
                    centre_balise = (float(x)/w_im, float(y)/l_im, 0)
                    multibreak()
    if output is None:
        return centre_balise
    else:
        output.put(centre_balise)


def ind(i, j, w, h):
    return i*w+j*h




from contextlib import contextmanager


# on fait une exception qui hérite de StopIteration car c'est ce qui est utilisé
# de toute façon pour arrêter une boucle
class MultiStopIteration(StopIteration):
    # la classe est capable de se lever elle même comme exception
    def throw(self):
        raise self


@contextmanager
def multibreak():
    # le seul boulot de notre context manager c'est de donne le moyen de lever
    # l'exception tout en l'attrapant
    try:
        yield MultiStopIteration().throw
    except MultiStopIteration:
        pass

if __name__ == '__main__':
    from gl_lib.sim.robot.strategy import Balise
    import os

    print(os.getcwd())
    im=imo.imread("../../../../screenshot.png")
    b=Balise()


    p=trouver_balise(im, b.colors)
    print(p)
    centre=Point(im.shape[0]/2, im.shape[1]/2, 0)
    v=(centre-p).to_vect()
    angle=v.diff_angle(Vecteur(0,-1, 0))
    if angle > 0.0:
        print("gauche")
    elif angle < 0.0:
        print("droite")
    else:
        print("devant")
