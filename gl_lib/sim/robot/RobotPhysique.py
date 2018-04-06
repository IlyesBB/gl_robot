from gl_lib.sim.robot import Robot
from gl_lib.sim.robot.sensor import Camera, CapteurIR, Accelerometre
from gl_lib.sim.robot import Tete
from gl_lib.sim.geometry import Objet3D, Pave, Arene
from gl_lib.sim.geometry.point import Vecteur, Point


class RobotPhysique(Robot):
    def __init__(self, pave: Objet3D = Pave(0, 0, 0), rg: Objet3D = Objet3D(), rd: Objet3D = Objet3D(),
                 direction: Vecteur = Vecteur(0, -1, 0)):
        """
        :param pave: forme du robot, a priori Pave
        :param rg: roue droite
        :param rd: roue gauche
        :param direction: direction du robot
        """
        Robot.__init__(self, pave, rg, rd, direction)
        self.tete = Tete(robot=self)
        self.tete.add_sensors(acc=Accelerometre(tete=self.tete), ir=CapteurIR(tete=self.tete, portee=3),
                              cam=Camera(tete=self.tete))

    def move(self, vecteur: Vecteur):
        """
        deplace le robot et sa tete
        :param vecteur: Vecteur
        """
        Robot.move(self,vecteur)

    def turn(self, sens):
        Robot.turn(self,sens)
        self.tete.turn(sens)

    def move_forward(self, sens: int or float):
        """ tourne le robot """
        if sens < 0:
            self.move(-self.vitesse * self.direction)
        elif sens > 0:
            self.move(self.vitesse * self.direction)

    def set_dir(self, vecteur: Vecteur):
        """
        change la direction du robot et de la tete
        """
        self.direction = vecteur.clone()
        self.tete.set_dir(vecteur)

    def update(self):
        self.tete.set_dir(self.direction)


if __name__ == '__main__':
    from math import pi

    p = Pave(5, 5, 0)
    p.move(Vecteur(5, 5, 0) * 1)
    r = RobotPhysique(Pave(5, 5, 0, centre=Point(0, 0, 0)))
    a = Arene([p])

    r.tete.add_sensors(ir=CapteurIR(tete=r.tete, portee=10))
    r.set_dir(Vecteur(1, 0, 0))

    m = r.tete.lcapteurs[Tete.IR].creer_matrice(a)
    for i in range(0, len(m)):
        print(m[i])
    print()

    n = 10
    rotation = 2 * pi / n
    for i in range(n + 1):
        p.rotate_all_around(r.centre, rotation)
        print(p)
        v = (p.centre - r.centre).to_vect().norm()
        r.set_dir(v)
        m = r.tete.lcapteurs[Tete.IR].creer_matrice(a)

        for i in range(0, len(m)):
            print(m[i])
        print()

    print(r.centre, r.forme.centre, r.tete.centre, r.tete.lcapteurs[Tete.IR].centre)
    r.move(Vecteur(3, 3, 0))
    print(r.centre, r.forme.centre, r.tete.centre, r.tete.lcapteurs[Tete.IR].centre)
    for i in range(100):
        r.turn(1)
    print(r.centre, r.forme.centre, r.tete.centre, r.tete.lcapteurs[Tete.IR].centre)
