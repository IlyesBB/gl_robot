from gl_lib.sim.display.d2.view.Vue2D import Vue2D
from gl_lib.sim.display.d2.view import Vue2DRobot, Vue2DRobotPhysique, Vue2DPave
from gl_lib.sim.robot import Robot, RobotPhysique
from gl_lib.sim.geometry import Arene

from gl_lib.sim.geometry import Pave


class Vue2DArene(Vue2D):
    """
    contient tout les objets de l'arene et les affiche 
    """

    def __init__(self, arene: Arene):
        """
        stockage de l'arene
        """
        self.arene = arene

    def afficher(self, canevas):
        """ 
        affiche les objets de l'arene sur le canevas, s'ils sont reconnus
        """
        # objets: [Objet3D]
        objets = self.arene.objets3D

        for o in objets:
            # o : Objet3D
            # if isinstance(o, RobotPhysique):
            #    view = Vue2DRobotPhysique(o, canevas)
            #    view.afficher(canevas)
            if isinstance(o, Robot):
                vue = Vue2DRobot(o, canevas)
                vue.afficher(canevas)
            if isinstance(o, Pave):
                vue = Vue2DPave(o, canevas)
                vue.afficher(canevas)
