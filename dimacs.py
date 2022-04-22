from typing import Literal, Union
import fnc
import os

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

    def __init__(self, clauses: fnc.Clause) -> None:
        self.clauses = clauses
        self.vtoi = {}
        self.itov = []
        c=0
        for t in self.clauses.termes:
            for l in t.litteraux:
                if self.vtoi.get(l.nom) is None:
                    c+=1
                    self.vtoi[l.nom]=c
                    self.itov.append(l.nom)
        self.input="p cnf " + str(c) + " " + str(len(self.clauses.termes)) + "\n"
        for t in self.clauses.termes:
            for l in t.litteraux:
                if l.signe == fnc.NEGATIF:
                    self.input+="-"
                self.input+=str(self.vtoi[l.nom])+" "
            self.input += "0\n"
    def resoudre(self) -> None:
        """
        Si elles sont satisfaisables l'attribut solution est un dictionnaire
        contenant la correspondance variable-valeur attribuée par le SAT-Solveur.
        """
        with open("input.dimacs","w") as satinput:
            satinput.write(self.input)
            os.system("minisat input.dimacs output.dimacs")
            with open("output.dimacs","r") as satouput:
                output = satouput.readlines()
                if output[0] == "SAT\n":
                    self.solution = {}
                    for xs in output[1].split():
                        x=int(xs)
                        if x > 0:
                            self.solution[self.itov[x-1]]=True
                        elif x < 0:
                            self.solution[self.itov[-x-1]]=False
                else:
                    self.solution = False
        return