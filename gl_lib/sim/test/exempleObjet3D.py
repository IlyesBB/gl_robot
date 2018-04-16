from gl_lib.sim.geometry import Objet3D, Point

#Creation d'un carre de cote 1 et deplacement de celui-ci du vecteur v
v=Point(1,1,1)
o = Objet3D()


print(o)

#deplacement puis display
print("deplacement de {}".format(v))
o.move(v)
print(o)

