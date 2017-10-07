#!/usr/bin/python
# -*- coding: utf-8 -*-

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--showUi", 
        type=str, 
        default="true",
        help="Valeur booléenne spécifiant si la partie graphique devrait être affichée ou non. \nValeur par défaut : faux." 
        )

    # récupère les arguments dans un objet (appelable comme un struct en C)
    args = parser.parse_args()


    if args.showUi :

        # create an object that inputs data randomly 
        if args.showUi == "true" :
            print("Starting project with UI!")
            exit(0)

        else :
            print("Starting project with no UI!")
            exit(0)

    else :
        # inputs the data by reading the given image
        print("Starting project with no UI!")
        exit(0)


'''
    Starts the project by outputting information about the processes only,
    without UI. 
'''
def noUI() :



    return

'''
    Starts the project by outputting information about the processes and by
    outputting through a UI. 
'''
def yesUI() : 

    return