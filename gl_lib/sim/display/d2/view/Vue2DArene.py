from gl_lib.sim.display.d2.view import Vue2DRobot, Vue2DRobotPhysique, Vue2DPave, Vue2D
from gl_lib.sim.geometry import Arene, Pave



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
            try:
                view = Vue2DRobotPhysique(o, canevas)
                view.afficher(canevas)
                continue
            except:
                pass
            try:
                vue = Vue2DRobot(o, canevas)
                vue.afficher(canevas)
                continue
            except:
                pass
            try:
                vue = Vue2DPave(o, canevas)
                vue.afficher(canevas)
                continue
            except:
                pass