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
            X, Y, Z = int((x + arene.width) * PIX_PAR_M), int((y + arene.length) * PIX_PAR_M), int((z + arene.height) * PIX_PAR_M)

            # selon x sortant

            self.batch.add(4, GL_QUADS, self.side, ('v3f', (x, y, z, x, y, Z, x, Y, Z, x, Y, z,)), tex_coords) # fond
            self.batch.add(4, GL_QUADS, self.side, ('v3f', (X, y, Z, X, y, z, X, Y, z, X, Y, Z,)), tex_coords) # face
            self.batch.add(4, GL_QUADS, self.side, ('v3f', (x, y, z, X, y, z, X, y, Z, x, y, Z,)), tex_coords) # droite
            self.batch.add(4, GL_QUADS, self.side, ('v3f', (x, Y, Z, X, Y, Z, X, Y, z, x, Y, z,)), tex_coords) # gauche
            self.batch.add(4, GL_QUADS, self.side, ('v3f', (X, y, z, x, y, z, x, Y, z, X, Y, z,)), tex_coords) # bas
            self.batch.add(4, GL_QUADS, self.side, ('v3f', (x, y, Z, X, y, Z, X, Y, Z, x, Y, Z,)), tex_coords) # haut

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
                self.visual_robot_target(i)
            except:
                pass
            try:
                self.visual_pave_color(i)
            except:
                pass
            try:
                self.visual_pave(i)
            except:
                pass

        return

    def draw(self):
        self.batch.draw()

    def visual_pave(self, pave):
        quads = Pave.quads(pave)
        t_quads = list()
        for i in range(len(quads)):
            tup = ()
            for j in range(len(quads[0])):
                tup += (quads[i][j] * PIX_PAR_M).to_tuple()
            t_quads[i] = tup

        self.side = self.get_tex('white.png')

        tex_coords = ('t2f', (0, 0, 0, 1, 1, 1, 1, 0))

        for i in range(len(pave.vertices)):
            self.batch.add(4, GL_QUADS, self.side, ('v3f', t_quads[i]), tex_coords)

    def visual_pave_color(self, pave):
        quads = Pave.quads(pave)
        t_quads = list()
        for i in range(len(quads)):
            tup = ()
            for j in range(len(quads[0])):
                tup += (quads[i][j]*PIX_PAR_M).to_tuple(type_coords=int)
            t_quads.append(tup)
        self.side = self.get_tex('white.png')



        tex_coords = ('t2f', (0, 0, 0, 1, 1, 1, 1, 0))
        for i in range(len(pave.vertices)):
            self.batch.add(4, GL_QUADS, self.side, ('v3f', t_quads[i]), tex_coords)

    def visual_robot_target(self, robot):
        # A CORRIGER: Ajouter ce qu'il faut pour afficher la balise au bon endroit
        quads = robot.forme.quads()
        t_quads = list()
        for i in range(len(quads)):
            tup = ()
            for j in range(len(quads[0])):
                tup += quads[i].sommet[j]
            t_quads[i] = tup

        self.side = self.get_tex('white.png')
        textures = self.get_text_balise(robot.balise.colors)

        tex_coords = ('t2f', (0, 0, 0, 1, 1, 1, 1, 0))

        n = 4
        # Côté du fond, dans le sens trigo en partant du point le plus bas
        for i in range(6):
            if i != n:
                self.batch.add(4, GL_QUADS, self.side, ('v3f', t_quads[i]), tex_coords)
            else:
                p0 = quads[i][0]
                y = (p0 - quads[i][3]).to_vect().norm()
                x = (p0 - quads[i][1]).to_vect().norm()
                h2 = y.get_mag() / 2
                l2 = x.get_mag() / 2
                l = [quads[i][0].clone(), quads[i][0] + x * l2, quads[i][0] + y * h2, quads[i][0] + y * h2 + x * l2]
                for j in range(len(textures)):
                    p0 = l[j]
                    quad = p0.to_tuple() + (p0 + x * l2).to_tuple() + (p0 + x * l2 + y * h2).to_tuple() + (
                            p0 + y * h2).to_tuple()
                    self.batch.add(4, GL_QUADS, textures[j], ('v3f', quad), tex_coords)

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

    a = AreneFermee(15, 15, 15)
    p1=Pave(1, 1, 0, centre=Point(14, 14, 14))
    p12=Pave(1, 1, 0, centre=Point(14, 14, 14))
    p12.move(Vecteur(0,0,-13))
    p2=PaveColored(1, 1, 0, centre=Point(0.5, 14, 14), color=(0,0,255,0))
    p22=PaveColored(1, 1, 0, centre=Point(0.5, 14, 14), color=(0,0,255,0))
    p22.move(Vecteur(0,0,-13))
    p3 = PaveColored(1, 1, 0, centre=Point(14, 14, 14), color=(0, 255, 0, 0))
    p32=PaveColored(1, 1, 0, centre=Point(14, 14, 14), color=(0, 255, 0, 0))
    p32.move(Vecteur(0,0,-13))
    a.add(p1)
    a.add(p12)
    a.add(p2)
    a.add(p22)
    a.add(p3)
    a.add(p32)
    r = RobotTarget(pave=Pave(1, 1, 0, centre=Point(0.5,0.5, 1)), direction=Vecteur(0, 1, 0).norm())
    r.set_wheels_rotation(3, 1)

    s = Simulation(StrategieVision(r, a))

    s.start()

