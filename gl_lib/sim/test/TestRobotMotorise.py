import os
import unittest
from cmath import pi

from gl_lib.config import PAS_TEMPS
from gl_lib.sim.geometry import Pave, Point, Vecteur
from gl_lib.sim.robot import RobotMotorise, Tete


class TestRobotMotorise(unittest.TestCase):
    def setUp(self):
        self.r = RobotMotorise(pave=Pave(1, 1, 0, centre=Point(5, 5, 0)), direction=Vecteur(1, 0, 0))


    def test_mecanism(self):
        """
            Vérifie que le robot avance correctement
        """
        self.r.set_wheels_rotation(1, 30)
        self.r.set_wheels_rotation(2, 30)
        self.p0 = self.r.centre.clone()
        self.n = int(1 / PAS_TEMPS) * 2
        print("Testing distance travelled...")
        for i in range(1, self.n):
            self.r.update()

        t_tot = self.n * PAS_TEMPS
        print("Time passed: ", t_tot, " s")
        d_th = (self.p0 - self.r.centre).to_vect().get_mag()
        d_calc = self.r.get_wheels_angles(1) * self.r.rd.diametre * (pi / 180)
        print("Error distance: ", abs(d_th-d_calc), " m")
        print("Done")
        self.assertAlmostEqual(d_th, d_calc)

    def test_json(self):
        """
            Vérifie le format json du robot
        """
        print("Testing json format...")
        r = RobotMotorise()
        r.save("robotmotorise.json")
        r2 = RobotMotorise.load("robotmotorise.json")
        self.assertIsInstance(r2, RobotMotorise)
        print("Done")

    def test_tete(self):
        """
            Vérifie la liaison entre la tête et le robot
        """
        print("Testing movement dependencies...")
        self.assertEqual(self.r.centre, self.r.tete.centre)
        self.r.move(Vecteur(1,0,0))
        self.assertEqual(self.r.centre, self.r.tete.centre)

        self.assertEqual(self.r.centre, self.r.tete.centre)
        self.r.rotate_all_around(self.r.centre, pi/4)
        self.r.tete.dir_rel = Vecteur(1,0,0)
        self.r.update()
        self.assertEqual(self.r.direction, self.r.tete.direction)
        print("Done")
