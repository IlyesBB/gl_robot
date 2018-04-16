import unittest
from gl_lib.sim.robot.strategy.deplacement import DeplacementCercle
from gl_lib.sim.robot import RobotMotorise
from gl_lib.sim.simulation import Simulation
from gl_lib.sim.robot.display.d2.gui import AppAreneThread
from gl_lib.sim.geometry import Arene, Pave, Point

class TestDeplacementCarre(unittest.TestCase):
    def setUp(self):
        self.cote = 1
        self.strat = DeplacementCercle(RobotMotorise(Pave(1,1,1, Point(4,4,0))), 1)
# cf DeplacementCercle.py