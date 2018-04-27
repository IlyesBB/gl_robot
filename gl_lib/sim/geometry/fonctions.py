# -*- coding: utf-8 -*-
from math import atan, pi, acos, sqrt, cos, sin
import os
import subprocess


def atan2(y,x):
    """retourne atan y/x """
    if x>0:
        return atan(y/x)
    if x<0:
        if y>=0:
            return atan(y/x)+pi
        if y<0:
            return atan(y/x)-pi
    if x==0:
        if y>0:
            return pi/2
        if y<0:
            return -pi/2
    return 0
    
def signe(x:int or float):
    """
        Retourne le signe de x
    """
    if x > 0.0:
        return 1
    elif x < 0.0:
        return -1
    else:
        return 0

def positive_angle(angle:float or int):
    """
        Retourne l'équivalent de angle (en radians) en positif

    :param angle:

    """
    if signe(angle) < 0:
        return angle + (2*pi)
    else:
        return angle

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
    res = get_project_repository()
    print(res)
