from gl_lib.sim.robot import RobotMotorise, Roue
from gl_lib.sim.robot.strategy import Balise
from gl_lib.sim.geometry import *
from gl_lib.sim.geometry.point import *
class RobotTarget(RobotMotorise):
    """
    Robot destiné à avoir une balise sur le dos
    """
    def __init__(self, pave=Pave(1,1,1),rg=Roue(0.15),rd=Roue(0.15), direction=Vecteur(0,1,0), balise=Balise()):
        """

        :param balise:
        """
        RobotMotorise.__init__(self, pave, rg, rd, direction)
        self.balise=balise

