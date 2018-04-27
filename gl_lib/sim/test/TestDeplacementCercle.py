from asyncio import sleep
from unittest import TestCase
from gl_lib.sim import Simulation
from gl_lib.sim.display.d2.gui import AppAreneThread
from gl_lib.sim.robot import *
from gl_lib.sim.geometry import *
from gl_lib.sim.robot.strategy.deplacement import DeplacementCercle


class TestDroitAmeliore(TestCase):
    def setUp(self):
        r = RobotMotorise(forme=Pave(centre=Point(0, 0, 0), width=1, height=1, length=1))
        r.move(Vecteur(5,5,0))
        self.arene = AreneFermee(3,3,3)
        self.diametre_cercle = 1
        self.strat = DeplacementCercle(robot=r, angle_max=360, diametre=self.diametre_cercle)
        self.arene.add(r)


    def test_visualisation_2D(self):

        app = AppAreneThread(self.arene)
        sim = Simulation(strategies=[self.strat])

        min_x, min_y = sim.strategie.robot.centre.x, sim.strategie.robot.centre.y
        max_x, max_y = sim.strategie.robot.centre.x, sim.strategie.robot.centre.y
        dps_wheels = sim.strategie.robot.get_wheels_rotations(3)

        sim.start()
        app.start()
        while not sim.stop:
            sleep(1)
            if sim.strategie.robot.centre.x < min_x:
                min_x = sim.strategie.robot.centre.x
            if sim.strategie.robot.centre.x > max_x:
                max_x = sim.strategie.robot.centre.x
            if sim.strategie.robot.centre.y < min_y:
                min_y = sim.strategie.robot.centre.y
            if sim.strategie.robot.centre.y > max_y:
                max_y = sim.strategie.robot.centre.y
            pass
        app.stop()

        print(abs(min_x-max_x), abs(max_y-min_y))


