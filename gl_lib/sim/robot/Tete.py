from gl_lib.sim.robot.sensor import *
from gl_lib.sim.geometry import Objet3D, Pave
from gl_lib.sim.geometry.point import *


class Tete(Objet3D):
    """
    definit une tete, ses capteurs et ses primitives de rotation
    """
    # indices pour reperer les capteurs
    IR, ACC, CAM = 0, 1, 2

    def __init__(self, centre: Point=Point(0,0,0), dir_robot: Vecteur=Vecteur(0,-1,0), vitesserot: float = 0.1, n_rotations: int = 0, robot=None):
        """
        :param pave: Pave (forme du robot)
        :param direction: Vecteur norme
        :param vitesserot: float
        :param n_rotations: nombre de rotation relatives de self.vitesseRot par rapport au robot
        """
        Objet3D.__init__(self)
        self.dirRobot = dir_robot
        self.centre = centre
        self.vitesseRot = vitesserot
        self.n_rotations = n_rotations
        self.direction = None
        self.lcapteurs = [None, None, None]

        self.set_dir(self.dirRobot)
        if robot is not None:
            self.dirRobot=robot.direction
            self.centre=robot.centre
            self.set_dir(self.dirRobot)

    def add_sensors(self, ir: CapteurIR = None, acc: Accelerometre = None, cam: Camera = None) -> int:
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

    def turn(self, sens: int):
        signe = 0
        if sens > 0:
            signe = 1
        elif sens < 0:
            signe = -1

        self.n_rotations += signe
        self.set_dir(self.dirRobot)

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

    def set_dir(self, vecteur: Vecteur):
        self.direction = vecteur.clone()
        self.direction.rotate(self.n_rotations * self.vitesseRot)
        for i in range(len(self.lcapteurs)):
            if self.lcapteurs[i] is not None:
                self.lcapteurs[i].direction = vecteur.clone()
                self.lcapteurs[i].direction.rotate(self.n_rotations * self.vitesseRot)

    def update(self):
        v=self.dirRobot.rotate(self.n_rotations*self.vitesseRot)
        self.set_dir(v)

        for i in range(len(self.lcapteurs)):
            self.lcapteurs[i].centre=self.centre
            self.lcapteurs[i].direction=v.clone()
            try:
                self.lcapteurs[i].update()
            except:
                pass

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
    p.move(Vecteur(2, -2, 0))
    r.set_dir((p.centre - r.centre).to_vect().norm())
    print(r.direction, r.tete.direction, r.tete.lcapteurs[Tete.IR].direction)
    a = Arene()
    a.add(p)
    m = r.tete.lcapteurs[Tete.IR].creer_matrice(a)
    print(r.tete.lcapteurs[Tete.IR].mesure(a))

    for i in range(len(m)):
        print(m[i])

    r.move_forward(1)
    r.move_forward(1)
    for i in range(5):
        r.turn(1)

    m = r.tete.lcapteurs[Tete.IR].creer_matrice(a)
    print(r.tete.lcapteurs[Tete.IR].mesure(a))

    for i in range(len(m)):
        print(m[i])

    r = RobotMotorise()
    print(r.tete.add_sensors(acc=Accelerometre(tete=r.tete)), r.tete)
