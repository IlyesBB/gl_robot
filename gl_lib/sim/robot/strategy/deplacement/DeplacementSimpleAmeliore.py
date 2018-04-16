from gl_lib.sim.robot.strategy.deplacement.DeplacementSimple import DeplacementSimple
from gl_lib.sim.geometry import Arene
from gl_lib.sim.robot import *
from gl_lib.config import PAS_IR
from gl_lib.sim.geometry import Vecteur, Point
from gl_lib.sim.robot.strategy.analyse.image import trouver_balise
from multiprocessing import Process
from math import pi


class DeplacementSimpleAmeliore(DeplacementSimple):
    """
    definit une strategy qui execute un mouvement du robot vers sa destination

    le robot balaye constamment l'espace avec sa tete pour detecter les obstacle

    Ne s'applique qu'a un robot disposant d'au minimum un capteurIR
    """

    def __init__(self, robot:RobotPhysique, arene:Arene):
        """
        :param robot: robot a deplacer
        :param: arene: environnement du robot
        """
        DeplacementSimple.__init__(self, robot)
        self.arene = arene

        # le robot n'a encore verifie ni la droite ni la gauche
        self.check_left, self.check_right = False, False
        # contient vrai si le robot est en train de scanner l'arene
        self.scan = True

    def obstacle_imminent(self):
        """
        Detecte les obstacles à une distance definie ici (a modifier)
        :return: Boolean
        """
        limite = Vecteur(self.robot.forme.largeur / 2.0, self.robot.forme.longueur / 2.0,0).get_mag() + PAS_IR

        if not self.check_left:
            if self.robot.tete.turn_towards_rel(pi / 4):
                self.check_left = True
            res = self.robot.tete.lcapteurs[Tete.IR].mesure(self.arene)
        elif not self.check_right:
            if self.robot.tete.turn_towards_rel(-pi / 4):
                self.check_right = True
            res = self.robot.tete.lcapteurs[Tete.IR].mesure(self.arene)
        else:
            self.scan = False
            res = self.robot.tete.lcapteurs[Tete.IR].mesure(self.arene)

        try:
            if res>0:
                print("prochain obstacle a : ", res-limite, " unites")
            return limite < res < limite + self.robot.vitesse
        except:
            return None

    def deplacement_vers(self, destination:Point):
        """
        execute un deplacement simple, s'il n'y a pas d'obstacle a proximite
        :param destination: Point
        """
        res = self.obstacle_imminent()

        if res:
            self.robot.destination = None
            return
        if not self.scan:
            DeplacementSimple.deplacement_vers(self, destination)
            self.scan = True
            self.check_right = False
            self.check_left = False

    def deplacement_vers_balise(self):
        """
        configure la destination du robot pour se deplacer vers la premiere balise, s'il y en a une
        on la detecte avec la camera
        :return:
        """
        p = Process(self.robot.tete.lcapteurs[Tete.CAM].picture, args=(self.arene,))
        p.start()
        p.join()
        if p.exitcode == 0:
            dest = trouver_balise()
            if dest is None:
                print("Aucune balise visible")
            else:
                self.robot.destination = dest.to_point() + self.robot.centre
        else:
            print("L'image n'a pas ete enregistree correctement")

