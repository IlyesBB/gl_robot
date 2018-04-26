# -*- coding: utf-8 -*-
import json
from collections import OrderedDict
from threading import Thread, Event
from gl_lib.config import PAS_TEMPS
from gl_lib.sim.geometry import Arene
from time import sleep

from gl_lib.sim.robot.strategy.deplacement import *
from gl_lib.sim.robot.strategy.vision import *
from gl_lib.sim.robot.strategy import *
from gl_lib.sim.robot.strategy.deplacement.balise import *

from gl_lib.utils import Serializable


class Simulation(Thread, Serializable):
    """
        Classe qui gère les stratégies et compte le temps, jusqu'à ce qu'elles aient toutes envoyé un signal de fin
    """
    INIT = {"strategies": None, "strategie": None, "acceleration_factor": 1.0, "tmax": None, "tic": None,
            "tic_display": None, "final_actions": None, "cpt": 0, "stop": True, }
    KEYS = ["cpt", "stop", "strategies", "strategie", "acceleration_factor", "tmax", "tic", "tic_display",
            "final_actions"]
    strat_hooks = ["DeplacementDroit", "DeplacementDroitAmeliore", "Tourner", "DeplacementCercle", "Strategie",
             "StrategieDeplacement", "StrategieVision", "DDroitAmelioreVision", "TournerVersBalise", "DroitVersBalise"]

    def __init__(self, **kwargs):
        """
        :param strategies: Liste de stratégies à exécuter
        :param strategie: Stratégie principale (fais partie  de strategies)
        :param acceleration_factor: Le temps s'écoule acceleration_factor fois plus vite
        :param tic: Affiche un petit message tous les tic secondes
        :param tic_display: Variables/objets affichés à chaque tic
        :param tmax: Temps de fin de la simulation en s
        """
        keys = kwargs.keys()
        for key in Simulation.INIT.keys():
            if not key in keys:
                kwargs[key] = Simulation.INIT[key]
        Thread.__init__(self)

        self.final_actions = kwargs["final_actions"]
        self.tic_display = kwargs["tic_display"]
        if len(kwargs["strategies"]) < 1:
            raise NameError("list of strategies not defined")
        self.strategies = kwargs["strategies"]
        self.strategie = kwargs["strategie"] if kwargs["strategie"] is not None else self.strategies[0]
        self.acceleration_factor = float(kwargs["acceleration_factor"])

        self.cpt = kwargs["cpt"] # Compte de temps en PAS_TEMPS sencondes
        self.stop = kwargs["stop"] # Indique si la simulation est à l'arrêt
        self.tic = int(kwargs["tic"] / PAS_TEMPS) if kwargs["tic"] is not None else None
        self.tmax = int(kwargs["tmax"] / PAS_TEMPS) if kwargs["tmax"] is not None else None

    def __dict__(self):
        """
            Discrétise la simulation
        """
        dct = OrderedDict()
        dct["__class__"] = Simulation.__name__
        keys = list(Simulation.KEYS)
        keys.remove("final_actions")
        keys.remove("strategies")
        for key in keys:
            try:
                dct[key] = self.__getattribute__(key).__dict__()
            except:
                dct[key] = self.__getattribute__(key)

        l = list()

        for st in self.strategies:
            l.append(st.__dict__())
        dct["strategies"] = list(l)

        l = list()
        if self.final_actions is not None and len(self.final_actions)>0:
            for m in self.final_actions:
                l.append({"__class__":type(m).__name__, "__self__":m.__self__.__dict__(), "__name__":m.__name__})
        dct["final_actions"] = l
        return dct

    def __repr__(self):
        """
            Affiche les attributs dans des dictionnaires
        """
        s = ""
        d = self.__dict__()
        for k in d.keys():
            if isinstance(d[k], list) and len(d[k])>0:
                s += k + " :\n"
                for i in range(len(d[k])):
                    s += "\t" + repr(d[k][i]) + "\n"
            else:
                s += k+" : "+repr(d[k])+"\n"
        return s

    def __str__(self):
        """
            Affiche les caractéristiques essentielles de la simulation
        """
        s = "{}; cpt: {}; stop: {}\n".format(self.__class__.__name__, self.cpt, self.stop)
        return s + str(self.strategie)

    @staticmethod
    def hook(dct):
        for strat in Simulation.strat_hooks:
            res = eval(strat+".hook")(dct)
            if res is not None:
                return res
        if dct["__class__"] == "method":
            return dct["__self__"].__getattribute__(dct["__name__"])
        if dct["__class__"] == Simulation.__name__:
            return Simulation(**dct)

    @staticmethod
    def load(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f, object_hook=Simulation.hook)


    def run(self):
        """Lance une boucle qui met à jour les stratégies tous les PAS_TEMPS (gl_lib.config)
        Peut être accéléré en ajustant acceleration_factor
        """
        self.stop = False
        dt = PAS_TEMPS / self.acceleration_factor
        print("Starting simulation...")
        while not self.stop:
            # La boucle s'arrête quand toutes méthodes stop() des stratégies on renvoyé True
            b = True
            for strategy in self.strategies:
                strategy.update()
                b = b and strategy.stop()

            if self.tic is not None:
                # Affiche le temps passé et les objest dans tic_display
                if self.cpt % self.tic == 0:
                    print(self.cpt * PAS_TEMPS, " seconds passed")
                    if self.tic_display is not None and len(self.tic_display) > 0:
                        for s in self.tic_display:
                            print(s)
            self.cpt += 1
            self.stop = b
            if self.tmax is not None:
                if self.cpt > self.tmax:
                    self.stop = True
                    break
            sleep(dt)

        # On sort de la simulation
        self.time_end = self.cpt * PAS_TEMPS
        print("End simalution ({} s)".format(self.time_end))
        if self.final_actions is not None and len(self.final_actions) > 0:
            print("Closing...")
            # Exécute les actions de fin
            for f in self.final_actions:
                f()


if __name__ == '__main__':
    from gl_lib.sim.robot import RobotMotorise

    strat = DeplacementCercle(robot=RobotMotorise())

    sim = Simulation(strategies=[strat], final_actions=[strat.update])

    sim.save("simulation.json")

    sim2 = Simulation.load("simulation.json")
    print(repr(sim2.clone()))
