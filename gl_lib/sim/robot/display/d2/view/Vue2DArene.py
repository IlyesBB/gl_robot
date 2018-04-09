from gl_lib.sim.robot.display.d2.view import Vue2DRobot, Vue2DRobotPhysique, Vue2DPave, Vue2D
from gl_lib.sim.geometry import Arene, Pave
from gl_lib.sim.robot import *



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
            if issubclass(type(o), Pave):
                vue = Vue2DPave(o, canevas)
                vue.afficher(canevas)
            elif issubclass(type(o), RobotPhysique):
                view = Vue2DRobotPhysique(o, canevas)
                view.afficher(canevas)
            elif issubclass(type(o), Robot):
                vue = Vue2DRobot(o, canevas)
                vue.afficher(canevas)

