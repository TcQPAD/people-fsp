#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import math

# gets the number of physical AND logical cores
# available on the current machine
from core.threads.main_background_thread import Main
from core.utils.display import Display

parser = argparse.ArgumentParser()
args = None
nbP = 4
main = None

'''
    Starts the project by outputting information about the processes only,
    without UI. 
'''


def noUI():
    Main(nbP, None, args).start()


'''
    Starts the project by outputting information about the processes and by
    outputting through a UI. 
'''


def yesUI():
    display = Display()
    Main(nbP, display.queue, args).start()
    display.startTk()


if __name__ == '__main__':

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

    if args.p:
        if args.p <= 512 * 128:
            nbP = math.pow(2, args.p)

        else:
            raise Exception("Too many people provided with -p. Max value is : " + str(512 * 128))

    if args.m:
        noUI()
        exit(0)
    elif args.showUi == "true":
        yesUI()
        exit(0)
    else:
        noUI()
        exit(0)
