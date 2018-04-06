from gl_lib.sim.robot import *
from gl_lib.sim.geometry import *
from gl_lib.sim.geometry.point import *
from gl_lib.config import PAS_TEMPS
from gl_lib.sim.simulation import Simulation
from math import pi


class RobotMotorise(RobotPhysique):
    """
    Robot dont on commande les moteurs des roues
    """
    PAS_MAX = 0.01

    def __init__(self, pave=Pave(1, 1, 1, centre=Point(2, 2, 0)), rg=Roue(), rd=Roue(),
                 direction: Vecteur = Vecteur(0, -1, 0)):
        """
        :param pave: forme du robot, a priori Pave
        :param rg: roue droite
        :param rd: roue gauche
        :param direction: direction du robot
        """
        RobotPhysique.__init__(self, pave, rg, rd, direction)

        self.angles_roues = (0, 0)
        self.dist_wheels = (self.rd.centre - self.rg.centre).to_vect().get_mag()

        self.set_wheels_rotation(3, 0)

    # ports: 1 pour roue gauche, 2 pour roue droite
    # sommer pour modifier les deux

    def set_wheels_rotation(self, port, dps):
        """
        :param port:
        :param dps:
        :return:
        """
        if port == 1:
            self.rd.vitesseRot = dps
        elif port == 2:
            self.rg.vitesseRot = dps
        elif port == 3:
            self.rd.vitesseRot = dps
            self.rg.vitesseRot = dps

    def get_wheels_rotations(self, port):
        """
        :param port:
        :return:
        """
        if port == 1:
            return self.rd.vitesseRot
        elif port == 2:
            return self.rg.vitesseRot
        elif port == 3:
            return self.rd.vitesseRot, self.rg.vitesseRot

    def get_wheels_angles(self, port):
        if port == 1:
            return self.rg.angle
        elif port == 2:
            return self.rd.angle
        elif port == 3:
            return self.rd.angle, self.rg.angle

    def get_wheels_speed(self, port):
        if port == 1:
            return self.rg.vitesseRot
        elif port == 2:
            return self.rd.vitesseRot
        elif port == 3:
            return self.rd.vitesseRot, self.rg.vitesseRot

    def reset_wheels_angles(self):
        self.rg.angle = 0
        self.rd.angle = 0

    def update(self):
        self.update_pos()
        self.tete.update()

    def update_pos(self):
        """
        Met à jour la position du robot en fonction de l'avancement des roues
        :return:
        """
        pas = min(RobotMotorise.PAS_MAX, PAS_TEMPS)
        n = int(PAS_TEMPS / RobotMotorise.PAS_MAX)
        angle_g = self.rg.vitesseRot * pas
        angle_d = self.rd.vitesseRot * pas

        d_rot = abs(self.rg.vitesseRot - self.rd.vitesseRot) * pas
        p_rot = self.rg.vitesseRot*self.rd.vitesseRot
        if d_rot == 0.0:
            v = self.direction * ((n + 1) * angle_d * self.rd.diametre * (pi / 180))
            self.move(v)
        else:

            diffs = (angle_d * (pi / 180) * (self.rd.diametre / self.dist_wheels),
                     angle_g * (pi / 180) * (self.rg.diametre / self.dist_wheels))
            for i in range(n + 1):
                v = (self.rg.centre - self.rd.centre).to_vect().norm()

                self.rotate_around(self.rg.centre, diffs[1])
                self.rotate_around(self.rd.centre, -diffs[0])

                self.forme.rotate_all_around(self.centre, diffs[0] - diffs[1])
                self.direction.rotate(-diffs[0] + diffs[1])

        self.rg.angle += (n + 1) * angle_g
        self.rd.angle += (n + 1) * angle_d


if __name__ == '__main__':
    r = RobotMotorise(pave=Pave(1, 1, 0, centre=Point(5, 5, 0)), direction=Vecteur(1, 0, 0))
    r.set_wheels_rotation(1, 0)
    r.set_wheels_rotation(2, 30)
    p0 = r.centre.clone()
    n = int(1 / PAS_TEMPS) * 2

    for i in range(1, n):
        r.update()

    t_tot = n * PAS_TEMPS
    print("temps de la simulation: ", t_tot, " s")
    print("vitesse mesurée :", r.tete.lcapteurs[Tete.ACC].get_mesure(1))

    print(r.get_wheels_angles(3), " rads")
    print((r.get_wheels_angles(3)[0] / t_tot, r.get_wheels_angles(3)[1] / t_tot), " rads.s^-1")
    print("distance parcourue théorique: ", (p0 - r.centre).to_vect().get_mag())
    print("distance parcourue calculée: ", r.get_wheels_angles(1) * r.rd.diametre * (pi / 180))

    from gl_lib.sim.robot.strategy.deplacement import StrategieDeplacement
    from gl_lib.sim.display.d2.gui import AppSimulationThread

    s = Simulation(StrategieDeplacement(r))

    newGUIThread = AppSimulationThread(s)
    s.start()
    newGUIThread.start()
