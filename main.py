#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
import warnings

import psutil as ps

from core.algo.first_scenario import FirstScenario
# gets the number of physical AND logical cores
# available on the current machine
from core.algo.second_scenario import SecondScenario
from core.map.map_first_scenario import MapFirstScenario
from core.map.map_second_scenario import MapSecondScenario
from core.utils.cpu_usage import CpuPercent
from core.utils.display import Display

nb__logical_cores = ps.cpu_count(True)

'''
    Starts the project by outputting information about the processes only,
    without UI. 
'''


def noUI():
    print("Starting project with no UI!")
    cpuPercent = None

    if args.m:
        cpuPercent = CpuPercent(0)

    map = MapFirstScenario(nbP, False) if args.t == 0 else MapSecondScenario()
    algorithm = FirstScenario(map, nbP, None, False) if args.t == 0 else SecondScenario(map, nbP, None, False)

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

            map = MapFirstScenario(nbP, True) if args.t == 0 else MapSecondScenario()
            algorithm = FirstScenario(map, nbP, None, True) if args.t == 0 else SecondScenario(map, nbP, None, False)

            cpuPercent.start()
            algorithm.startAlgo()
            cpuPercent.stopMeasure()

            print("Finished simulation number " + str(i))

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
    map = MapFirstScenario(nbP, True if args.m else False, display) if args.t == 0 else MapSecondScenario()
    algorithm = FirstScenario(map, nbP, display, True if args.m else False) if args.t == 0 else SecondScenario(map, nbP,
                                                                                                               display,
                                                                                                               True if args.m else False)
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

    parser.add_argument(
        "-t",
        type=int,
        default=0,
        help="Scenario à exécuter. 0 ou 1."
    )

    # data structure with the argument (dictionary) that will be easily
    # usable
    args = parser.parse_args()

    nbP = 4

    if args.p:
        if args.p <= 512 * 128:
            nbP = math.pow(2, args.p)

        else:
            raise Exception("Too many people provided with -p. Max value is : " + str(512 * 128))

        # more threads than CPU cores, raise a warning
        # because program may be slower than expected
        if nbP > nb__logical_cores:
            warnings.warn("Provided number of threads is > to number of available cores\n"
                          "It may slow the execution of the program instead of accelerating it !!!\n"
                          "Number of available cores: " + str(nb__logical_cores), UserWarning)

    if args.m:
        noUI()
        exit(0)
    elif args.showUi == "true":
        yesUI()
        exit(0)
    else:
        noUI()
        exit(0)
