from gl_lib.sim.robot import RobotMotorise

class RobotTarget(RobotMotorise):
    """
    Robot destiné à avoir une balise sur le dos
    """
    def __init__(self, pave,rg,rd, direction, balise):
        """

        :param balise:
        """
        RobotMotorise.__init__(self, pave, rg, rd, direction)
        self.balise=balise

