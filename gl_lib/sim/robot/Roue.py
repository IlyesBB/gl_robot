from gl_lib.sim.geometry import Objet3D, Point


class Roue(Objet3D):
    """
    Definie les informations de base pour une roue
    """

    def __init__(self,diametre:float or int=0.3, centre:Point=Point(0,0,0)):
        """

        :param diametre:
        """
        Objet3D.__init__(self, centre)
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

    def get_angle(self):
        return self.angle

    def clone(self):
        return Roue(self.diametre, self.centre.clone())

    def __eq__(self, other):
        if Objet3D.__eq__(self, other) is False:
            return False
        if self.diametre != other.diametre:
            return False
        return True

    def __repr__(self):
        return "Roue de diametre " + str(self.diametre) + " tournant a " + str(self.vitesseRot) + " dps"



if __name__ == '__main__':
    r = Roue(10)
    print(r)
