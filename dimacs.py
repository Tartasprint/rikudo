from typing import Literal, Union
import fnc
import os
from config import sat

class Dimacs:
    """
    Contient les informations pour communiquer avec le SAT-solveur.

    Attributs:
        vtoi    Tableau nom de variable vers entier
        itov    Tableau entier vers nom de variable
        clauses Le système que l'on veut résoudre
        input   L'entrée DIMACS donnée au SAT Solveur
        output  La sortie DIMACS du SAT Solveur
        solution La solution du SAT Solveur. False si insatisfaisable, sinon une table de
                    correspondance entre nom de variable et valeur obtenue par le SAT-Solveur.
    """

    itov: list[str]
    vtoi: dict[str,int]
    solution: Union[Literal[False],dict[str,bool]]
    input: str
    output: str
    def __init__(self, clauses: fnc.Clause, nvars: int) -> None:
        self.clauses = clauses
        self.vtoi = {}
        self.itov = []
        self.nvars = nvars
    def resoudre(self, nom) -> None:
        """
        Si elles sont satisfaisables l'attribut solution est un dictionnaire
        contenant la correspondance variable-valeur attribuée par le SAT-Solveur.
        """
        entree_fichier = nom+".input.dimacs"
        sortie_fichier = nom+".output.dimacs"
        with open(entree_fichier,"w") as entree_sat:
            # On écrit le fichier d'entrée pour le SAT solveur
            entree_sat.write("p cnf " + str(len(self.itov)) + " " + str(len(self.clauses.termes)) + "\n")
            for t in self.clauses.termes:
                for l in t.litteraux:
                    if l.signe == fnc.NEGATIF:
                        entree_sat.write("-")
                    i=self.vtoi.get(l.nom)
                    if i is None:
                        self.itov.append(l.nom)
                        i=len(self.itov)
                        self.vtoi[l.nom]=i
                    entree_sat.write(str(i))
                    entree_sat.write(" ")
                entree_sat.write("0\n")
        # On fait appel au SAT solveur
        os.system(sat(entree_fichier, sortie_fichier))
        with open(sortie_fichier,"r") as sortie:
            sortie_sat = sortie.readlines()
        if sortie_sat[0] == "SAT\n":                            # Satisfaisable
            self.solution = {}
            for xs in sortie_sat[1].split():
                x=int(xs)
                if x > 0:
                    self.solution[self.itov[x-1]]=True
                elif x < 0:
                    self.solution[self.itov[-x-1]]=False
        else:                                               # Insatisfaisable
            self.solution = False
        return