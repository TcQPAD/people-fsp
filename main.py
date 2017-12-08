#!/usr/bin/python
# -*- coding: utf-8 -*-

from core.map import Map
from core.algo import Algorithm
from core.display import Display
from core.cpu_usage import CpuPercent

import psutil as ps
import warnings
import math

# gets the number of physical AND logical cores
# available on the current machine
nb__logical_cores = ps.cpu_count(True)

'''
    Starts the project by outputting information about the processes only,
    without UI. 
'''


def noUI():
    print("Starting project with no UI!")
    cpuPercent = CpuPercent()
    if args.m:
        cpuPercent.start()

    map = Map(True if args.m else False)
    algorithm = Algorithm(map, nbP, None, True if args.m else False)
    algorithm.startAlgo()
    if args.m:
        cpuPercent.stopMeasure()
        cpuPercent.produce_report()

    return


'''
    Starts the project by outputting information about the processes and by
    outputting through a UI. 
'''


def yesUI():
    print("Starting project with UI!")
    display = Display(512, 128)
    map = Map(True if args.m else False, display)
    algorithm = Algorithm(map, nbP, display, True if args.m else False)
    algorithm.startAlgo()
    return


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--showUi",
        type=str,
        default="true",
        help="Valeur booléenne spécifiant si la partie graphique devrait être affichée ou non. \nValeur par défaut : "
             "faux. "
    )

    parser.add_argument(
        "-p",
        type=int,
        default=4,
        help="Puissance de 2 pour le nombre de personnes à insérer dans la simulation. Valeur par défaut: 4 (donc 2^4 "
             "= 16 personnes). "
    )

    parser.add_argument(
        "-m",
        action = "store_true", # to tell that this option has no value
        help="Si donné comme argument du programme, affiche des statistiques du CPU sur la sortie standard à la fin de l'exécution"
             "du programme."
    )

    # récupère les arguments dans un objet (appelable comme un struct en C)
    args = parser.parse_args()

    nbP = 4

    if args.p:
        if args.p <= 512 * 128:
            nbP = args.p

        else:
            raise Exception("Too many people provided with -p. Max value is : " + str(512*128))

        # more threads than CPU cores, raise a warning
        # because program may be slower than expected
        if math.pow(2, args.p) > nb__logical_cores:
            warnings.warn("Provided number of threads is > to number of available cores\n"
                          "It may slow the execution of the program instead of accelerating it !!!\n"
                          "Number of available cores: " + str(nb__logical_cores), UserWarning)

    if args.showUi:

        # create an object that inputs data randomly 
        if args.showUi == "true":

            if args.m:
                noUI()
                exit(0)

            yesUI()
            exit(0)

        else:
            noUI()
            exit(0)

    else:
        noUI()
        exit(0)
