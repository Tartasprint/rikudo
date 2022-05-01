from carte import Carte
import sys

arg=sys.argv
if len(arg) != 2:
    print("Il faut exactement un argument, le fichier de la carte à résoudre.")
    exit(1)
nom_carte = arg[1]
carte= Carte(nom_carte)
carte.resoudre()