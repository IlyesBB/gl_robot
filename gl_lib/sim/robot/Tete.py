from gl_lib.sim.geometry import *
from math import pi

class Tete(Objet3D):
    """
    definit une tete, ses capteurs et ses primitives de rotation
    """
    # indices pour reperer les capteurs
    IR, ACC, CAM = 0, 1, 2

    def __init__(self, centre: Point=Point(0,0,0),dir_robot: Vecteur=Vecteur(0,-1,0), dir_rel:Vecteur=Vecteur(1,0,0)):
        """
        :param pave: Pave (forme du robot)
        :param direction: Vecteur norme
        :param vitesserot: float
        :param n_rotations: nombre de rotation relatives de self.vitesseRot par rapport au robot
        """
        Objet3D.__init__(self, centre)
        self.dir_robot = dir_robot
        self.dir_rel = dir_rel
        angle=self.dir_rel.get_angle()
        self.direction=self.dir_robot.clone().rotate(angle)
        self.lcapteurs = [None, None, None]

    def add_sensors(self, ir = None, acc = None, cam = None) -> int:
        """ permet d'ajouter n'importequel type de sensor
        Tant qu'il respecte les type des capteurs
        """
        cpt = 0
        if ir is not None:
            self.lcapteurs[Tete.IR] = ir
            cpt += 1
        if cam is not None:
            self.lcapteurs[Tete.CAM] = cam
            cpt += 1
        if acc is not None:
            self.lcapteurs[Tete.ACC] = acc
            cpt += 1
        return cpt

    def rotate(self, angle:float, axis=None):
        self.dir_rel.rotate(angle, axis)

    def turn_towards(self, vecteur: Vecteur):
        diff = self.direction.diff_angle(vecteur)
        if abs(diff) > self.vitesseRot:
            self.turn(diff)
            return False
        else:
            return True

    def turn_towards_rel(self, teta: float):
        diff = int(teta / self.vitesseRot) - self.n_rotations
        if abs(diff) > 0:
            self.turn(diff)
            return False
        else:
            return True

    def set_dir(self):
        angle=self.dir_rel.get_angle()

        self.direction = self.dir_robot.clone().rotate(angle)
        for i in range(len(self.lcapteurs)):
            if self.lcapteurs[i] is not None:
                self.lcapteurs[i].direction = self.direction

    def update(self):
        self.set_dir()
        for i in range(len(self.lcapteurs)):
            if self.lcapteurs[i] is not None:
                self.lcapteurs[i].update()

    def __eq__(self, other):
        if Objet3D.__eq__(self, other) is False:
            return False
        if self.dir_robot != other.dir_robot or self.direction != other.direction:
            return False
        if self.dir_rel != other.dir_rel:
            return False
        for i in range(len(self.lcapteurs)):
            if self.lcapteurs[i] != other.lcapteurs[i]:
                return False
        return True


    def __repr__(self):
        s = ""
        for i in range(len(self.lcapteurs)):
            s += str(self.lcapteurs[i]) + "\n"
        return s


if __name__ == '__main__':
    from gl_lib.sim.geometry import Arene
    from gl_lib.sim.robot import RobotMotorise

    # une tete est cree automatiquement dans le constructeur du robot
    r = RobotMotorise()
    print(r.direction, r.tete.direction, r.tete.lcapteurs[Tete.IR].direction)

    p = Pave(1, 1, 0)
    p.move(Vecteur(0, -2, 0))
    r.set_dir((p.centre - r.centre).to_vect().norm())
    print(r.direction, r.tete.direction, r.tete.lcapteurs[Tete.IR].direction)
    a = Arene()
    a.add(p)
    m = r.tete.lcapteurs[Tete.IR].creer_matrice(a)
    print(r.tete.lcapteurs[Tete.IR].get_mesure(a))

    for i in range(len(m)):
        print(m[i])

    r.move_forward(1)
    r.move_forward(1)
    for i in range(5):
        r.turn(1)

    m = r.tete.lcapteurs[Tete.IR].creer_matrice(a)
    print(r.tete.lcapteurs[Tete.IR].get_mesure(a))

    for i in range(len(m)):
        print(m[i])

    r = RobotMotorise()
    print(r.tete.add_sensors(acc=Accelerometre(tete=r.tete)), r.tete)
