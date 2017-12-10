#!/usr/bin/python
# -*- coding: utf-8 -*-

from core.map import Map
from core.algo import Algorithm
from core.display import Display
from core.cpu_usage import CpuPercent
from core.algo_scenario_1 import AlgorithmScenarioOne

import psutil as ps
import warnings
import math

# gets the number of physical AND logical cores
# available on the current machine
nb__logical_cores = ps.cpu_count(True)

"""
    Overrides the default warnings.showwarning()
    function from the warnings package
    We need to override it because warning.warn() prints 
    the Python code of the warning to the user
    
    Here, we only return the msg of the warning and NOT the Python code
    
    see: https://stackoverflow.com/questions/2187269/python-print-only-the-message-on-warnings
"""


def custom_formatwarning(msg, *a):
    # ignore everything except the message
    return str(msg) + '\n'


'''
    Starts the project by outputting information about the processes only,
    without UI. 
'''


def noUI():
    print("Starting project with no UI!")
    cpuPercent = None

    if args.m:
        cpuPercent = CpuPercent(0)

    map = Map(False)
    algorithm = AlgorithmScenarioOne(map, nbP, None, False)

    if args.m:
        # finished setting up for simulation
        # start measurements
        cpuPercent.start()

    algorithm.startAlgo()

    if args.m:
        cpuPercent.stopMeasure()
        i = 1
        while i < 5:
            # here, we could have used a ThreadPool along
            # with an executor service to re-use this measurement thread
            # instead of re-creating one after each simulation.
            # however, the doc says that for the moment, due to the GLI,
            # multiprocessing API spawns subprocesses instead of threads, which
            # is less effective and heavier for the machine
            # see: https://docs.python.org/2/library/multiprocessing.html
            cpuPercent = CpuPercent(i)

            map = Map(True)
            algorithm = AlgorithmScenarioOne(map, nbP, None, True)

            cpuPercent.start()
            algorithm.startAlgo()
            cpuPercent.stopMeasure()

            print("Finished simulation number " + str(i + 1))

            i += 1

        # need to join cpuPercent to let it finish writing in the file
        # the results of the last 5th simulation, or there will be a concurrency
        # problem for the res.json file
        cpuPercent.join()
        # returns the measurements for the 5 simulations
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
    algorithm = AlgorithmScenarioOne(map, nbP, display, True if args.m else False)
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
        action="store_true",  # to tell that this option has no value
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
            raise Exception("Too many people provided with -p. Max value is : " + str(512 * 128))

        # more threads than CPU cores, raise a warning
        # because program may be slower than expected
        if math.pow(2, args.p) > nb__logical_cores:
            warnings.formatwarning = custom_formatwarning
            warn_msg = "\nProvided number of threads is > to number of available cores\nIt may slow the execution of the program instead of accelerating it !!!\nNumber of available cores: " + str(
                nb__logical_cores) + "\n"
            warnings.warn(warn_msg, UserWarning)

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
