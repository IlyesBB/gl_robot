from gl_lib.config import PAS_TEMPS
from gl_lib.sim.robot import RobotMotorise
from gl_lib.sim.robot.strategy.deplacement import StrategieDeplacement, Tourner
from math import pi, cos, sin
from gl_lib.sim.geometry import fonctions

class DeplacementCercle(Tourner):
    """Dirige le robot pour dessiner un cercle, approximé par un polygone dont tout les points sont sur ce cercle

    Le robot commence à dessiner le cercle dans le sens de sa direction
    On se
    """
    def __init__(self, robot:RobotMotorise, angle_max:float or int = 360, diametre:int or float = None,
                 vitesse: int or float = 30):
        """

        :param robot: Robot à déplacer
        :param angle_max: Angle duquel se déplacer sur le cercle
        :param diametre: Diamètre du cercle en mètres
        :param vitesse: Vitesse en degrés par seconde
        """
        Tourner.__init__(self, robot,angle_max)
        self.diametre = abs(diametre)
        self.sens = fonctions.signe(diametre)
        self.init_movement(angle_max,self.diametre,vitesse)

    def init_movement(self, angle_max,diametre_cercle=1, dps_moy=30):
        if angle_max is None:
            return
        self.angle_max = abs(angle_max)
        self.rot_angle = 0
        self.turning = True
        diametre = diametre_cercle
        vitesse = abs(dps_moy)*self.robot.rd.diametre*(1/2.0)
        sens = fonctions.signe(angle_max)
        vg = 2*vitesse/self.robot.rd.diametre
        vd = (1-(self.robot.rd.diametre/(2*diametre))) * 2 * vitesse / self.robot.rd.diametre

        if sens < 0:
            aux = vg
            vg = vd
            vd = aux

        self.robot.set_wheels_rotation(1,vd)
        self.robot.set_wheels_rotation(2,vg)

    def update(self):
        if self.turning is True:
            self.robot.update()
            dps_wheels = self.robot.get_wheels_rotations(3)
            vitesse_rot = abs(dps_wheels[0]-dps_wheels[1])*(pi/180)
            self.rot_angle += vitesse_rot * PAS_TEMPS * (self.robot.rd.diametre / self.robot.dist_wheels)

            v=self.robot.direction
            try:
                # Peut générer des erreurs si la vitesse est nulle
                if self.rot_angle>(self.angle_max*pi/180):
                    print("Done turning ", self.sens*self.angle_max, "degrees")
                    Tourner.abort(self)
                    self.robot.set_wheels_rotation(3,0)
            except:
                pass

if __name__ == '__main__':
    from gl_lib.sim.simulation import Simulation
    from gl_lib.sim.robot.display.d2.gui import AppAreneThread
    from gl_lib.sim.robot import *
    from gl_lib.sim.robot.sensor import Accelerometre
    from gl_lib.sim.geometry import *

    a = AreneFermee(10,10,10)
    r = RobotMotorise(Pave(centre=Point(3, 6, 0), width=1, height=1, length=1))
    sim = Simulation(DeplacementCercle(r, -90, 0.5), 4)
    a.add(r)
    app = AppAreneThread(a)
    sim.start()
    app.start()
    min_x, min_y = sim.strategie.robot.centre.x, sim.strategie.robot.centre.y
    max_x, max_y = sim.strategie.robot.centre.x, sim.strategie.robot.centre.y
    dps_wheels = sim.strategie.robot.get_wheels_rotations(3)
    while not sim.stop:
        if sim.strategie.robot.centre.x < min_x:
            min_x = sim.strategie.robot.centre.x
        if sim.strategie.robot.centre.x > max_x:
            max_x = sim.strategie.robot.centre.x
        if sim.strategie.robot.centre.y < min_y:
            min_y = sim.strategie.robot.centre.y
        if sim.strategie.robot.centre.y > max_y:
            max_y = sim.strategie.robot.centre.y
    d_rot = abs(dps_wheels[0]-dps_wheels[1])*PAS_TEMPS*(pi/180)
    max_rot = max(dps_wheels[0], dps_wheels[1])*PAS_TEMPS*(pi/180)
    d_dist = max_rot*(sim.strategie.robot.rd.diametre/2)
    print(dps_wheels)
    n=(2*pi)/d_rot
    gr_diametre = n*d_dist/(2*pi)
    print((max_x - min_x)/2, gr_diametre)
    print(dps_wheels)
    app.stop()


