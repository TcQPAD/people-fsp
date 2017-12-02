#!/usr/bin/python
# -*- coding: utf-8 -*-

from core.map import Map
from core.algo import Algorithm
from core.display import Display

'''
    Starts the project by outputting information about the processes only,
    without UI. 
'''
def noUI():
    map = Map()
    algorithm = Algorithm(map, nbP)
    algorithm.startAlgo()
    print("Starting project with no UI!")
    return

'''
    Starts the project by outputting information about the processes and by
    outputting through a UI. 
'''
def yesUI():
    display = Display(512, 128)
    map = Map(display)
    algorithm = Algorithm(map, nbP, display)
    algorithm.startAlgo()
    print("Starting project with UI!")
    return

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--showUi", 
        type=str, 
        default="true",
        help="Valeur booléenne spécifiant si la partie graphique devrait être affichée ou non. \nValeur par défaut : faux." 
        )

    parser.add_argument(
        "-p",
        type=int,
        default=4,
        help="Puissance de 2 pour le nombre de personnes à insérer dans la simulation. Valeur par défaut: 4 (donc 2^4 = 16 personnes)."
    )

    # récupère les arguments dans un objet (appelable comme un struct en C)
    args = parser.parse_args()

    nbP = 4

    if args.p:
        if args.p <= 512*128:
            nbP = args.p
        else:
            raise Exception("Too many people in args, using 4 persons instead")

    if args.showUi:

        # create an object that inputs data randomly 
        if args.showUi == "true" :
            yesUI()
            exit(0)

        else :
            noUI()
            exit(0)

    else :
        noUI()
        exit(0)
