from gl_lib.sim.robot import RobotMotorise, Roue
from gl_lib.sim.geometry import *

class RobotTarget(RobotMotorise):
    """
    Robot destiné à avoir une balise sur le dos
    """
    def __init__(self, pave=Pave(1,1,1),rg=Roue(0.25),rd=Roue(0.25), direction=Vecteur(1,1,0).norm(), balise=None):
        """

        :param balise:
        """
        RobotMotorise.__init__(self, pave, rg, rd, direction)
        self.balise=balise

