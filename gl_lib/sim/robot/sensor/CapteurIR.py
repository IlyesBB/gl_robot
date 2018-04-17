from gl_lib.sim.robot.sensor import Capteur

from math import pi
from gl_lib.sim.geometry import Arene, Pave, Point, Vecteur, Objet3D
from gl_lib.config import PAS_IR, RES_M
from gl_lib.sim.robot import Robot, Tete

class CapteurIR(Capteur):
    """
    Capteur qui renvoi la distance du prochain pavé dans la trajectoire de sa direction en mètres
    """
    # Pas de recherche d'un obstacle
    dp = PAS_IR

    def __init__(self, centre: Point = Point(0, 0, 0), direction: Vecteur = Vecteur(1, 0, 0), portee: int or float = 3):
        Capteur.__init__(self, centre=centre, direction=direction)
        self.portee = portee
        self.arena_v = None
        self.l_ignore = list()

    def get_matrix_view(self, arene: Arene):
        self.arena_v = VueMatriceArene(arene, origine=self.centre, ox=self.direction, ajuste=True)
        return self.arena_v

    def get_mesure(self, arene: Arene, d_ingnore=0.0, ignore=None):
        """
        Retourne la distance entre le sensor et le premier objet dans la matrice cf dessous
        Retourne -1 si pas d'obstacle detecte

        :param arene: arène dans laquelle effectuer la mesure
        :return: float ou int
        """
        self.get_matrix_view(arene)
        m = self.arena_v.vueDessus(self.portee, ignore)

        # On parcours la matrice sur la diagonale, dans le sens croissant
        # ce qui correspond a la vue ajustée de la matrice
        v=Vecteur(1,1,0).norm()*VueMatriceArene.res
        n = int(self.portee / CapteurIR.dp)
        for cpt in range(n):
            pos = (v*cpt*CapteurIR.dp).to_point().clone(type_coords=int)
            try:
                # Au cas ou on sortirait du tableau
                if m[int(pos.x)][int(pos.y)] == 1:
                    res = cpt * CapteurIR.dp
                    if res >= d_ingnore:
                        return res
            except:
                print(pos, " est hors de portée")
        return -1

    def clone(self):
        return CapteurIR(self.centre, self.direction, self.portee)

    def __eq__(self, other):
        if self.centre != other.centre:
            return False
        if self.portee != other.portee:
            return False
        if self.direction != other.direction:
            return False
        return True

class VueMatriceArene(object):
    """Classe destinée à contenir les informations de la portion de l'arène à afficher, et les méthode pour
        produire la matrice correcpondante

        On peut configurer l'axe Ox du repère, ainsi que l'origine, pour afficher des portions de l'arène sous forme de
        matrice
    """
    res = RES_M

    def __init__(self, arene:Arene=Arene(), origine:Point=Point(0, 0, 0), ox:Vecteur=Vecteur(1, 0, 0), ajuste:bool=False):
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
        self.matrice = None # Destiné à stocker la dernière matrice crée

    def vueDessus(self, dx:int or float, ignore:Objet3D or [Objet3D]=None):
        """ Crée une matrice d'entiers avec 1 si le point est à l'intérieur d'une forme et 0 sinon

        Cette méthode ne détecte que les pavés, et les robots ayant comme forme un pavé

        Procédure globale
        - Pour chaque objet, si on trouve un pavé:
            - Pour chaque point de la matrice, on vérifie s'il est dedans

        :param dx: Taille de la matrice
        :param ignore: Liste ou simple objet à dans la matrice
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
                if len(ignore)>0:
                    for i in ignore:
                        if i == obj:
                            continue
            else:
                if ignore == obj:
                    continue

            # Si on ne peut pas récupérer les informations nécessaires au traitement, on passe
            # Sinon, on récupère les sommets du pavé, dans un repère où ce dernier est droit
            pave = self.get_pave(obj)
            if pave is None:
                continue
            # on commence par recuperer les infos importantes sur le pave
            ls = pave.vertices
            inclinaison_m = (ls[0] - ls[1]).to_vect().diff_angle(ox)
            inclinaison_m_abs = (ls[0] - ls[1]).to_vect().diff_angle(Vecteur(1,0,0))
            if self.ajuste:
                inclinaison_ajuste = inclinaison_m-pi/4
            else:
                inclinaison_ajuste = inclinaison_m
            ls = pave.rotate(inclinaison_m).vertices
            centre=obj.centre.clone()

            # ls correspond ici aux sommets d'un pavé droit, on récupère dont ses coordonnées limites
            s_xmax, s_ymax = max(ls[i].x for i in range(0, len(ls))), max(ls[i].y for i in range(0, len(ls)))
            s_xmin, s_ymin = min(ls[i].x for i in range(0, len(ls))), min(ls[i].y for i in range(0, len(ls)))

            for x in range(nxmax):
                # x: int (coordonnée en x du point dans le repère de la vue, en 1/RES_M mètres)
                for y in range(nymax):
                    # y: int (coordonnée en y du point dans le repère de la vue, en 1/RES_M mètres)

                    # p: Point (coordonnées du point dans le repère de l'arène, en mètres)
                    p = self.origine + (ox*x+oy*y)/VueMatriceArene.res
                    # On met p dans le bon repère par rapport au pavé
                    p = p.rotate_around(centre, inclinaison_ajuste)

                    if s_xmin <= p.x <= s_xmax and s_ymin <= p.y <= s_ymax:
                        matrice2d[x][y] = 1
        self.matrice = matrice2d
        return matrice2d

    def get_pave(self, obj):
        pave = None
        if issubclass(type(obj), Pave):
            # ls: [Point]
            pave = obj.clone()
        elif issubclass(type(obj), Robot):
            # ls: [Point]
            pave = obj.forme.clone()
        return pave

    def __repr__(self):
        """
        Retourne une chaine décrivant précisemment la vue et la dernière matrice
        :return: string
        """
        ox = self.ox.clone()
        if self.ajuste:
            ox.rotate(-pi/4)
        s="ox: "+str(ox)+"\n"
        s+="origine: "+str(self.origine)+"\n"
        s+="resolution: " + str(VueMatriceArene.res) + "\n"
        if self.matrice is not None:
            for i in range(len(self.matrice)):
                s += str(self.matrice[i])+"\n"
        return s

if __name__ == '__main__':
    from gl_lib.sim.robot import RobotMotorise, Tete
    from gl_lib.sim.geometry import Pave
    from gl_lib.sim.robot.strategy.deplacement import DeplacementDroitAmeliore
    from gl_lib.sim import Simulation
    from gl_lib.sim.display.d2.gui import AppSimulationThread
    v=Vecteur(1,1,0).norm()
    c = CapteurIR(centre=Point(0, 0, 0), direction=v.clone(), portee=3)
    p = Pave(1, 1, 0)
    p.move(v*3)
    p.rotate(-pi/4)

    r=RobotMotorise(direction=v.clone())
    a = Arene()
    a.add(p)
    a.add(r)
    m = c.creer_matrice(a)
    n = 4
    rotation = 2 * pi / n

    # Le sensor suit le pave, et on affiche la mesure a chaque rotation
    s = Simulation(DeplacementDroitAmeliore(r,3, a))
    app=AppSimulationThread(s)

    app.start()
    s.start()


