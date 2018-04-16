import numpy as np
from gl_lib.sim.geometry import *
import imageio as imo
import os
from math import pi
from gl_lib.config import PIX_PAR_M


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
        s = fname
        im=imo.imread(s)
        w_im, l_im = int(im.shape[0] - 1), int(im.shape[1] - 1)
    elif image is not None:
        im = np.asarray(image)
        w_im, l_im = int(im.shape[0] - 1), int(im.shape[0] - 1)
        return None
    else:
        return None
    PAS_RECH = min(w_im, l_im)/50
    pas = int(PAS_RECH)
    # Côté du carré cherché
    RAYON_RECH = PAS_RECH
    # Dans l'affichae 3D, l'ordre des sommets change
    l_lvertices = [[0, 3, 2, 1]]
    # La deuxième liste sert juste à corriger le bug d'affichage 3D (n'affiche pas la balise à l'endroit)
    i0 = int(RAYON_RECH / PAS_RECH)+1
    # Pour éviter que le carré cherché sorte du tableau

    centre_balise = None
    for x in [i * pas for i in range(i0, int(w_im / pas) - i0)]:
        for y in [i * pas for i in range(i0, int(l_im / pas) - i0)]:
            point_act=Point(x,y,0)
            pave = Pave(RAYON_RECH * 2, RAYON_RECH * 2, 0, centre=point_act.clone())
            for lvertices in l_lvertices:
                balise = True
                for i in range(len(couleurs)):
                    p = pave.vertices[lvertices[i]].to_tuple(type_coords=int)
                    #print(p, lvertices[i])
                    #print(couleurs[i], " != ",tuple(im[p[0]][p[1]]), "\n")
                    if couleurs[i] != tuple(im[p[0]][p[1]]):
                        balise = False
                        break
                if balise:
                    centre_balise = (point_act.x/w_im, point_act.y/l_im, 0)
                    multibreak()
    if output is None:
        return centre_balise
    else:
        output.put(centre_balise)


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
