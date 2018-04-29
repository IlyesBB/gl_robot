# -*- coding: utf-8 -*-
from gl_lib.sim.geometry import ApproximableAPave

class PaveTarget(ApproximableAPave):
    """
        Classe abstraite regroupant les objets approximable à des pavés ayant une cible sur une face
    """
    def get_target(self):
        """
            Retourne la balise avec lequel est ciblé l'objet

            À implémenter dans les classes filles
        """
        return

    def get_face(self):
        """
            Retourne la face sur laquelle est la balise

        :return: entier compris entre 0 et 5
        """
        return

