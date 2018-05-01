# -*- coding: utf-8 -*-
import os
import sys
from math import sqrt
RES_M = 2
PAS_IR=(1/RES_M)*sqrt(2)
DT_SCREENSHOT = 0.1
PAS_TEMPS=0.2
PIX_PAR_M_2D=50
PIX_PAR_M=5
PIX_PAR_M_3D=5

# Prendre une trop grande précision peut amener des erreurs dans la recherche de la balise
RATIO_SEARCH_SCREENSHOT = 10
SEARCH_LUM_PRECISION = 100
FORMAT_SCREENSHOT = ".png"
FILENAME_SCREENSHOT = "screenshot"
# A précéder du nom du répertoire du projet
REPNAME_SCREENSHOTS = "/sim/robot/sensor/camera/pictures/"
REPNAME_TEXTURES = "/sim/robot/sensor/camera/d3/"


def get_project_repository():
    """
        Cherche le répertoire du projet dans l'ordinateur

        ATTENTION: Peut ne pas fonctionner pour plusieurs raisons (plusieurs répertoires avec le nom du projet,
        notamment)
    """
    os.chdir("/home/")
    #p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    stream = os.popen("find -name 'gl_lib' | grep -v 'local' | grep -v 'venv' | grep -vi 'lien'")
    s = str(stream.read()).replace(".", "/home")
    l = s.split('\n')
    stream.close()
    return l[0]

if __name__=='__main__':
    sys.stdout.write(get_project_repository())