from gl_lib.sim.geometry import Objet3D


class Roue(Objet3D):
    """
    Definie les informations de base pour une roue
    """

    def __init__(self, diametre=0.015):
        """

        :param diametre:
        """
        self.diametre = diametre
        self.vitesseRot = 0
        self.angle = 0

    def turn(self, sens):
        """
        :param sens:
        :return:
        """
        if sens < 0:
            self.angle += self.vitesseRot

        elif sens > 0:
            self.angle -= self.vitesseRot

    def set_dps(self, dps):
        self.vitesseRot=dps

    def get_angle(self):
        return self.angle

    def __repr__(self):
        return "Roue de diametre " + str(self.diametre) + " tournant a " + str(self.vitesseRot) + " dps"


if __name__ == '__main__':
    r = Roue(10)
    print(r)
