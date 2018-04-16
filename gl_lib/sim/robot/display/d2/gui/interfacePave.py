from tkinter import *
from gl_lib.sim.geometry import Arene, Pave, Objet3D
from gl_lib.sim.robot.display.d2.view import *
from gl_lib.sim.geometry import Vecteur
from gl_lib.sim.robot import Robot
from math import *


def lancer_simulation():
    """
    Initialise les elements necessaires au lancement et appelle les fonctions de la simulation
    """
    arene = creer_arene()
    global vueArene
    global Canevas

    # creaction fenetre
    fenetre = Tk()
    fenetre.title("Interface d'display de l'arene")

    # creaction des boutons
    Button(fenetre, text='Quitter', command=fenetre.destroy).pack(side=LEFT, padx=5, pady=5)
    Button(fenetre, text='Effacer', command=effacer).pack(side=LEFT, padx=5, pady=5)

    # creation canvas/arene
    Canevas = Canvas(fenetre, width=480, height=320, bg='white')
    vueArene = Vue2DArene(arene)
    vueArene.afficher(Canevas)
    Canevas.bind('<Key>', clavier)
    Canevas.focus_set()

    Canevas.pack(padx=10, pady=10)
    fenetre.mainloop()


def clavier(event):
    """
    q, d : tourner
    z, s : avancer/reculer
    """
    effacer()
    pasRotation = pi / 100
    global pave
    global vueArene
    global Canevas
    touche = event.keysym
    if touche == 'z':
        pave.move(Vecteur(0, -1, 0))
    if touche == 's':
        pave.move(Vecteur(0, 1, 0))
    if touche == 'q':
        pave.rotate(-pasRotation)
    if touche == 'd':
        pave.rotate(pasRotation)
    vueArene.afficher(Canevas)


def creer_arene():
    """
    renvoi une arene avec quelques objets: ici juste un pave
    """
    arene = Arene()
    global pave
    pave = Pave(1, 1, 0)
    pave.move(Vecteur(2, 2, 0))  # Le robot doit avoir une position nulle au depart pour etre a (50,50)
    arene.add(pave)
    return arene


def effacer():
    """
    Efface la zone graphique
    """
    Canevas.delete(ALL)


lancer_simulation()
