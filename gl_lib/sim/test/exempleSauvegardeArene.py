from gl_lib.sim.geometry import *
from gl_lib.sim.geometry.point import *


a=Arene()
o1=Polygone3D()
o2=Polygone3D()
o3=Polygone3D()
o1.add_vertex(Point(1, 1, 1))
o1.add_vertex(Point(1, 1, 2))
o1.add_vertex(Point(1, 2, 1))
o1.add_vertex(Point(1, 2, 2))
o2.add_vertex(Point(2, 2, 2))
o2.add_vertex(Point(2, 2, 3))
o2.add_vertex(Point(2, 3, 2))
o2.add_vertex(Point(2, 3, 3))
o3.add_vertex(Point(3, 3, 3))
o3.add_vertex(Point(3, 3, 4))
o3.add_vertex(Point(3, 4, 3))
o3.add_vertex(Point(3, 3, 4))
a.add(o1)
a.add(o2)
a.add(o3)
a.sauvegardeArene()