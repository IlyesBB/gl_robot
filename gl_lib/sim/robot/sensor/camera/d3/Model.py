from pyglet.gl import *
from pyglet.window import key
import math
from gl_lib.config import PIX_PAR_M
from gl_lib.sim.geometry import *


class Model:

    def get_tex(self, file):
        tex = pyglet.image.load(file).texture
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        return pyglet.graphics.TextureGroup(tex)

    def __init__(self, arene):
        self.side = self.get_tex('white.png')

        self.batch = pyglet.graphics.Batch()

        if isinstance(arene, AreneFermee):
            tex_coords = ('t2f', (0, 0, 0, 1, 1, 1, 1, 0))

            x, y, z = 0, 0, 0
            X, Y, Z = int((x + arene.width) * PIX_PAR_M), int((y + arene.length) * PIX_PAR_M), int(
                (z + arene.height) * PIX_PAR_M)

            # selon x sortant

            self.batch.add(4, GL_QUADS, self.side, ('v3f', (x, y, z, x, y, Z, x, Y, Z, x, Y, z,)), tex_coords)  # fond
            self.batch.add(4, GL_QUADS, self.side, ('v3f', (X, y, Z, X, y, z, X, Y, z, X, Y, Z,)), tex_coords)  # face
            self.batch.add(4, GL_QUADS, self.side, ('v3f', (x, y, z, X, y, z, X, y, Z, x, y, Z,)), tex_coords)  # droite
            self.batch.add(4, GL_QUADS, self.side, ('v3f', (x, Y, Z, X, Y, Z, X, Y, z, x, Y, z,)), tex_coords)  # gauche
            self.batch.add(4, GL_QUADS, self.side, ('v3f', (X, y, z, x, y, z, x, Y, z, X, Y, z,)), tex_coords)  # bas
            self.batch.add(4, GL_QUADS, self.side, ('v3f', (x, y, Z, X, y, Z, X, Y, Z, x, Y, Z,)), tex_coords)  # haut

        self.visual_arene(arene)

    def get_text_color(self, color):
        couleur = color
        if (couleur[0], couleur[1], couleur[2]) == (255, 255, 255):
            return self.get_tex('white.png')
        elif (couleur[0], couleur[1]) == (255, 255):
            return self.get_tex('yellow.png')
        elif couleur[0] == 255:
            return self.get_tex('red.png')
        elif couleur[1] == 255:
            return self.get_tex('green.png')
        elif couleur[2] == 255:
            return self.get_tex('blue.png')

    def visual_arene(self, arene):
        for i in arene.objets3D:

            try:
                self.visual_pave(i)
            except:

                try:
                    self.visual_robot_target(i)
                except:
                    pass
        return

    def draw(self):
        self.batch.draw()

    def visual_pave(self, pave, texture=None):
        if texture is None:
            self.side = self.get_tex('red.png')
        else:
            self.side = texture
        p = pave.clone()

        tex_coords = ('t2f', (0, 0, 0, 1, 1, 1, 1, 0))
        for i in range(len(p.vertices)):
            p.vertices[i] = (p.vertices[i] * PIX_PAR_M).clone(type_coords=int)

        l_ln = [[0, 1, 2, 3], [0, 3, 7, 4], [1, 5, 6, 2], [4, 5, 6, 7], [0, 4, 5, 1], [3, 2, 6, 7]]
        for l in range(len(l_ln)):
            self.batch.add(4, GL_QUADS, self.side,
                           ('v3f', (p.vertices[l_ln[l][0]].x, p.vertices[l_ln[l][0]].y, p.vertices[l_ln[l][0]].z,
                                    p.vertices[l_ln[l][1]].x, p.vertices[l_ln[l][1]].y, p.vertices[l_ln[l][1]].z,
                                    p.vertices[l_ln[l][2]].x, p.vertices[l_ln[l][2]].y, p.vertices[l_ln[l][2]].z,
                                    p.vertices[l_ln[l][3]].x, p.vertices[l_ln[l][3]].y, p.vertices[l_ln[l][3]].z,)),
                           tex_coords)

    def visual_pave_color(self, pave):
        self.side = self.get_text_color(pave.color)
        self.visual_pave(texture=self.side)

    def visual_robot_target(self, robot):

        l_ln = [[0, 1, 2, 3], [0, 3, 7, 4], [1, 5, 6, 2], [4, 5, 6, 7], [0, 4, 5, 1], [3, 2, 6, 7]]

        face = 4
        p = robot.forme.clone()
        tex_coords = ('t2f', (0, 0, 0, 1, 1, 1, 1, 0))

        for i in range(len(p.vertices)):
            p.vertices[i] = (p.vertices[i] * PIX_PAR_M).clone(type_coords=int)

        for l in range(len(l_ln)):
            if l == face:
                self.batch.add(4, GL_QUADS, self.get_tex('balise.png'),
                               ('v3f', (p.vertices[l_ln[l][0]].x, p.vertices[l_ln[l][0]].y, p.vertices[l_ln[l][0]].z,
                                        p.vertices[l_ln[l][1]].x, p.vertices[l_ln[l][1]].y, p.vertices[l_ln[l][1]].z,
                                        p.vertices[l_ln[l][2]].x, p.vertices[l_ln[l][2]].y, p.vertices[l_ln[l][2]].z,
                                        p.vertices[l_ln[l][3]].x, p.vertices[l_ln[l][3]].y, p.vertices[l_ln[l][3]].z,)),
                               tex_coords)
            else:
                self.batch.add(4, GL_QUADS, self.side,
                               ('v3f', (p.vertices[l_ln[l][0]].x, p.vertices[l_ln[l][0]].y, p.vertices[l_ln[l][0]].z,
                                        p.vertices[l_ln[l][1]].x, p.vertices[l_ln[l][1]].y, p.vertices[l_ln[l][1]].z,
                                        p.vertices[l_ln[l][2]].x, p.vertices[l_ln[l][2]].y, p.vertices[l_ln[l][2]].z,
                                        p.vertices[l_ln[l][3]].x, p.vertices[l_ln[l][3]].y, p.vertices[l_ln[l][3]].z,)),
                               tex_coords)

    def get_text_balise(self, colors):
        """

        :param color:
        :return:
        """
        textures = list()
        for couleur in colors:
            textures.append(self.get_text_color(couleur))
        return textures


if __name__ == '__main__':
    from gl_lib.sim.robot import RobotMotorise, RobotTarget, Tete
    from gl_lib.sim.robot.sensor import *
    from gl_lib.sim.geometry.point import *
    from gl_lib.sim.geometry import *
    from gl_lib.sim.simulation import Simulation
    from gl_lib.sim.robot.strategy.vision import StrategieDeplacementVision, StrategieVision
    from gl_lib.sim.robot.strategy.deplacement import StrategieDeplacement
    from gl_lib.sim.robot.strategy.deplacement.balise import TournerVersBaliseVision, DroitVersBaliseVision
    from math import pi

    a = AreneFermee(30, 30, 30)
    p1 = Pave(1, 1, 1)
    w, l, h = a.width , a.length , a.height
    p_w2, p_l2, p_h2 = p1.width / 2, p1.length / 2, p1.height / 2
    l = [Vecteur(w - p_w2, p_l2, p_h2),
         Vecteur(w - p_w2, p_l2, -p_h2 + h),
         Vecteur(p_w2, l - p_l2, p_h2),
         Vecteur(p_w2, l - p_l2, -p_h2 + h),
         Vecteur(w - p_w2, l - p_l2, p_h2),
         Vecteur(w - p_w2, l - p_l2, -p_h2 + h)]


    for v in l:
        p=p1.clone()
        a.add(p.move(v).clone())
    v=Vecteur(1,1,0).norm()*10
    r = RobotTarget(pave=Pave(1, 1, 1, centre=Point(0.5, 0.5, 1).move(v)), direction=Vecteur(1, 0, 0).rotate(pi / 4).norm())
    r2 = RobotTarget(pave=Pave(1, 1, 1, centre=Point(5, 5, 1).move(v)), direction=Vecteur(1, 0, 0).rotate(pi / 4).norm())
    r.set_wheels_rotation(3, 0)
    r2.set_wheels_rotation(0,0)

    a.add(r2)
    s2 = Simulation(StrategieDeplacement(r2))
    s = Simulation(DroitVersBaliseVision(r, a))

    s2.start()
    s.start()
