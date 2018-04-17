from PIL import Image
from pyglet.gl import *
from gl_lib.sim.robot import RobotTarget, Robot
from gl_lib.sim.robot.sensor.camera import Balise
from gl_lib.config import PIX_PAR_M, REPNAME_TEXTURES
from gl_lib.sim.geometry import *
from gl_lib.sim.geometry import fonctions
import os

class Model:

    def get_tex(self, file):
        tex = pyglet.image.load(file).texture
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        return pyglet.graphics.TextureGroup(tex)

    def __init__(self, arene):
        os.chdir(fonctions.get_project_repository() + REPNAME_TEXTURES)
        self.batch = pyglet.graphics.Batch()
        self.batch_bg = pyglet.graphics.Batch()
        self.l_textures = list()
        self.graphic_objects = list()
        self.updatable_g_objs = list()
        l = ['white.png', 'red.png', 'green.png', 'blue.png', 'yellow.png', 'balise.png', 'grey.png']
        for file in l:
            self.l_textures.append(self.get_tex(file))

        if isinstance(arene, AreneFermee):
            X, Y, Z = arene.width * PIX_PAR_M, arene.length * PIX_PAR_M, arene.height * PIX_PAR_M
            p = Pave(X,Y,Z)
            p.move(p.vertices[4].to_vect()*-1)
            #im = Image.open('grey.png')
            #im.thumbnail((p.width*im.shape[0], p.length), Image.ANTIALIAS)
            #im.save(outfile, "JPEG")
            self.visual_pave(p, self.l_textures[6], self.batch_bg)
        self.visual_arene(arene)

    def get_text_color(self, color):
        if color is None:
            return self.l_textures[0]
        i = fonctions.signe(color[0]) + fonctions.signe(color[1]) + fonctions.signe(color[2])
        return self.l_textures[i]

    def visual_arene(self, arene:Arene):
        for i in range(len(arene.objets3D)):
            t=type(arene.objets3D[i])
            if issubclass(t, Pave):
                self.visual_pave(arene.objets3D[i])
            elif issubclass(t, RobotTarget):
                self.visual_robot_target(arene.objets3D[i])
            elif issubclass(t, Robot):
                #self.visual_pave(i.forme)
                pass
    def draw(self):
        for i in range(len(self.updatable_g_objs)):
            quads_lvertices = Model.get_vertices(self,self.updatable_g_objs[i][1])
            for j in range(6):
                self.updatable_g_objs[i][0][j].vertices=list(quads_lvertices[j])

        self.batch_bg.draw()
        self.batch.draw()

    def visual_pave(self, pave, texture=None, batch=None):
        if texture is None:
            self.side = self.l_textures[0]
        else:
            self.side = texture
        p = pave.clone()
        if batch is None:
            cur_batch = self.batch
        else:
            cur_batch = self.batch_bg

        tex_coords = ('t2f/static', (0, 0, 1, 0, 1, 1, 0, 1))
        for i in range(len(p.vertices)):
            p.vertices[i] = (p.vertices[i] * PIX_PAR_M).clone()

        l_ln = [[0, 1, 2, 3], [0, 3, 7, 4], [1, 5, 6, 2], [4, 5, 6, 7], [0, 4, 5, 1], [3, 2, 6, 7]]
        l_objs = list()
        for l in range(len(l_ln)):
            obj=cur_batch.add(4, GL_QUADS, self.side,
                           ('v3f/static', (p.vertices[l_ln[l][0]].x, p.vertices[l_ln[l][0]].y, p.vertices[l_ln[l][0]].z,
                                    p.vertices[l_ln[l][1]].x, p.vertices[l_ln[l][1]].y, p.vertices[l_ln[l][1]].z,
                                    p.vertices[l_ln[l][2]].x, p.vertices[l_ln[l][2]].y, p.vertices[l_ln[l][2]].z,
                                    p.vertices[l_ln[l][3]].x, p.vertices[l_ln[l][3]].y, p.vertices[l_ln[l][3]].z,)),
                           tex_coords)
            l_objs.append(obj)
        p=pave
        self.graphic_objects.append((l_objs, p))

    def visual_pave_color(self, pave):
        self.side = self.get_text_color(pave.color)
        self.visual_pave(pave, self.side)

    def visual_robot_target(self, robot):
        l_ln = [[0, 1, 2, 3], [0, 3, 7, 4], [1, 5, 6, 2], [4, 5, 6, 7], [0, 4, 5, 1], [3, 2, 6, 7]]
        face = 1
        p = robot.forme.clone()
        tex_coords = ('t2f/static', (1, 1, 0, 1, 0, 0, 1, 0))
        self.side = self.l_textures[0]

        for i in range(len(p.vertices)):
            p.vertices[i] = (p.vertices[i] * PIX_PAR_M).clone()
        l_objs = list()
        for l in range(len(l_ln)):
            if l == face:
                obj=self.batch.add(4, GL_QUADS, self.l_textures[5],
                               ('v3f/dynamic', (p.vertices[l_ln[l][0]].x, p.vertices[l_ln[l][0]].y, p.vertices[l_ln[l][0]].z,
                                        p.vertices[l_ln[l][1]].x, p.vertices[l_ln[l][1]].y, p.vertices[l_ln[l][1]].z,
                                        p.vertices[l_ln[l][2]].x, p.vertices[l_ln[l][2]].y, p.vertices[l_ln[l][2]].z,
                                        p.vertices[l_ln[l][3]].x, p.vertices[l_ln[l][3]].y, p.vertices[l_ln[l][3]].z,)),
                               tex_coords)
                l_objs.append(obj)
            else:
                obj=self.batch.add(4, GL_QUADS, self.side,
                               ('v3f/dynamic', (p.vertices[l_ln[l][0]].x, p.vertices[l_ln[l][0]].y, p.vertices[l_ln[l][0]].z,
                                        p.vertices[l_ln[l][1]].x, p.vertices[l_ln[l][1]].y, p.vertices[l_ln[l][1]].z,
                                        p.vertices[l_ln[l][2]].x, p.vertices[l_ln[l][2]].y, p.vertices[l_ln[l][2]].z,
                                        p.vertices[l_ln[l][3]].x, p.vertices[l_ln[l][3]].y, p.vertices[l_ln[l][3]].z,)),
                               tex_coords)
                l_objs.append(obj)
        p=robot.forme
        self.updatable_g_objs.append((l_objs, p, robot.lock_update_pos))

    def get_text_balise(self, colors):
        """
        :param color:
        :return:
        """
        textures = list()
        for couleur in colors:
            textures.append(self.get_text_color(couleur))
        return textures

    def get_vertices(self, pave):
        l_ln = [[0, 1, 2, 3], [0, 3, 7, 4], [1, 5, 6, 2], [4, 5, 6, 7], [0, 4, 5, 1], [3, 2, 6, 7]]
        lvertices = list()
        p=pave.clone()
        for i in range(len(p.vertices)):
            p.vertices[i] = (p.vertices[i] * PIX_PAR_M).clone()
        for l in range(len(l_ln)):
            vertices = (p.vertices[l_ln[l][0]].x, p.vertices[l_ln[l][0]].y, p.vertices[l_ln[l][0]].z,
                                        p.vertices[l_ln[l][1]].x, p.vertices[l_ln[l][1]].y, p.vertices[l_ln[l][1]].z,
                                        p.vertices[l_ln[l][2]].x, p.vertices[l_ln[l][2]].y, p.vertices[l_ln[l][2]].z,
                                        p.vertices[l_ln[l][3]].x, p.vertices[l_ln[l][3]].y, p.vertices[l_ln[l][3]].z,)
            lvertices.append(vertices)
        return lvertices

if __name__ == '__main__':
    from gl_lib.sim import Simulation
    from gl_lib.sim.robot.strategy.deplacement.balise import DroitVersBaliseVision
    from gl_lib.sim.robot.sensor.camera import Balise
    import os
    from math import pi

    a = AreneFermee(15,15,15)
    p1 = Pave(1, 1, 1)
    w, l, h = a.width , a.length , a.height
    p_w2, p_l2, p_h2 = p1.width / 2, p1.length / 2, p1.height / 2


    v=Vecteur(1,1,0).norm()*-1
    r = RobotTarget(direction=v.clone(), balise = Balise())
    r2 = RobotTarget(pave=Pave(1, 1, 1, (v*5).to_point()), direction=v.clone())
    r.set_wheels_rotation(3, 0)
    r2.set_wheels_rotation(0,0)
    print(os.getcwd())
    #a.add(r2)
    s = Simulation(DroitVersBaliseVision(r, a))

    s.start()
