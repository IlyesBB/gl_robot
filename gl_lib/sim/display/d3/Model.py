from pyglet.gl import *
from pyglet.window import key
import math
from gl_lib.sim.geometry import *


class Model:

    def get_tex(self, file):
        tex = pyglet.image.load(file).texture
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        return pyglet.graphics.TextureGroup(tex)

    def __init__(self, arene):

        if arene is None:
            Pave1 = Pave(10, 8, 30)

            Pave2 = Pave(15, 6, 25)

            Pave3 = Pave(7, 7, 7)
            arene = Arene()
            arene.add(Pave1)
            arene.add(Pave2)
            arene.add(Pave3)

        self.side = self.get_tex('white.png')

        self.batch = pyglet.graphics.Batch()

        if isinstance(arene, AreneFermee):
            tex_coords = ('t2f', (0, 0, 0, 1, 1, 1, 1, 0))

            x, y, z = 0, 0, 0
            X, Y, Z = x + arene.width, y + arene.length, z + arene.height

            self.batch.add(4, GL_QUADS, self.side, ('v3f', (x, y, z, x, y, Z, x, Y, Z, x, Y, z,)), tex_coords)
            self.batch.add(4, GL_QUADS, self.side, ('v3f', (X, y, Z, X, y, z, X, Y, z, X, Y, Z,)), tex_coords)
            self.batch.add(4, GL_QUADS, self.side, ('v3f', (x, y, z, X, y, z, X, y, Z, x, y, Z,)), tex_coords)
            self.batch.add(4, GL_QUADS, self.side, ('v3f', (x, Y, Z, X, Y, Z, X, Y, z, x, Y, z,)), tex_coords)
            self.batch.add(4, GL_QUADS, self.side, ('v3f', (X, y, z, x, y, z, x, Y, z, X, Y, z,)), tex_coords)
            self.batch.add(4, GL_QUADS, self.side, ('v3f', (x, y, Z, X, y, Z, X, Y, Z, x, Y, Z,)), tex_coords)

        self.visualiser(arene)

    def visualiser(self, arene):
        for i in arene.objets3D:
            if isinstance(i, Pave):
                x, y, z = i.vertices[0].x, i.vertices[0].y, i.vertices[0].z
                X, Y, Z = i.length, i.width, i.length

                self.side = self.get_tex('Red.svg.png')

                tex_coords = ('t2f', (0, 0, 0, 1, 1, 1, 1, 0))

                self.batch.add(4, GL_QUADS, self.side, ('v3f', (x, y, z, x, y, Z, x, Y, Z, x, Y, z,)), tex_coords)
                self.batch.add(4, GL_QUADS, self.side, ('v3f', (X, y, Z, X, y, z, X, Y, z, X, Y, Z,)), tex_coords)
                self.batch.add(4, GL_QUADS, self.side, ('v3f', (x, y, z, X, y, z, X, y, Z, x, y, Z,)), tex_coords)
                self.batch.add(4, GL_QUADS, self.side, ('v3f', (x, Y, Z, X, Y, Z, X, Y, z, x, Y, z,)), tex_coords)
                self.batch.add(4, GL_QUADS, self.side, ('v3f', (X, y, z, x, y, z, x, Y, z, X, Y, z,)), tex_coords)
                self.batch.add(4, GL_QUADS, self.side, ('v3f', (x, y, Z, X, y, Z, X, Y, Z, x, Y, Z,)), tex_coords)

            elif isinstance(i, RobotTarget):
                # A CORRIGER: Ajouter ce qu'il faut pour afficher la balise au bon endroit
                x, y, z = i.forme.vertices[0].x, i.forme.vertices[0].y, i.forme.vertices[0].z
                X, Y, Z = i.forme.length, i.forme.width, i.height
                X2, Y2, Z2 = i.length/2, i.width/2, i.height/2

                self.side = self.get_tex('Red.svg.png')

                tex_coords = ('t2f', (0, 0, 0, 1, 1, 1, 1, 0))

#Côté du fond, dans le sens trigo en partant du point le plus bas
                self.batch.add(4, GL_QUADS, self.side, ('v3f', (x, y, z, X2, y, z, X2, Y2, z, x, Y2, z,)), tex_coords)

                self.batch.add(4, GL_QUADS, self.side, ('v3f', (x, Y2, z, X2, Y2, z, X2, Y, z, x, Y, z,)), tex_coords)

                self.batch.add(4, GL_QUADS, self.side, ('v3f', (X2, Y2, z, x, Y2, z, X, Y, z, x, Y, z,)), tex_coords)

                self.batch.add(4, GL_QUADS, self.side, ('v3f', (X2, y, z, X, y, z, X, Y2, z, X2, Y2, z,)), tex_coords)



                self.batch.add(4, GL_QUADS, self.side, ('v3f', (x, y, z, x, y, Z, x, Y, Z, x, Y, z,)), tex_coords)
                self.batch.add(4, GL_QUADS, self.side, ('v3f', (X, y, Z, X, y, z, X, Y, z, X, Y, Z,)), tex_coords)
                self.batch.add(4, GL_QUADS, self.side, ('v3f', (x, y, z, X, y, z, X, y, Z, x, y, Z,)), tex_coords)
                self.batch.add(4, GL_QUADS, self.side, ('v3f', (x, Y, Z, X, Y, Z, X, Y, z, x, Y, z,)), tex_coords)
                self.batch.add(4, GL_QUADS, self.side, ('v3f', (X, y, z, x, y, z, x, Y, z, X, Y, z,)), tex_coords)
                self.batch.add(4, GL_QUADS, self.side, ('v3f', (x, y, Z, X, y, Z, X, Y, Z, x, Y, Z,)), tex_coords)
                pass


        return

    def draw(self):
        self.batch.draw()
