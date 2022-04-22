from dimacs import Dimacs
import regles
import fnc

class Carte:
    def __init__(self,nom: str):
        with open(nom ,"r") as fichier:
            n=fichier.readline().strip().split()
            self.H = int(n[0])
            self.L = int(n[1])
            self.vals = {(i,j): None for i in range(self.L * self.H) for j in range(self.L * self.H)}
            for i in range(self.H):
                l=fichier.readline().strip().split()
                for j in range(self.L):
                    if l[j] != "?":
                        self.vals[i*self.L+j,int(l[j])]=True
        N = self.L * self.H
        def voisins(i: int, j: int):
            return (i//self.L == j//self.L and abs(i-j) == 1) or (i%self.L == j%self.L and abs(i//self.L-j//self.L) == 1)
        d = set(range(N))
        self.regles,self.regles_aux = regles.generer_regles(d,self.vals,voisins)
    def resoudre(self):
        RG = fnc.Top()
        for i,regle in enumerate(self.regles):
            print(i)
            RG.extend(regle.fnc())
        RG.extend(self.regles_aux)
        sat=Dimacs(RG)
        sat.resoudre()
        tab=[[-1 for _ in range(self.L)] for _ in range(self.H)]
        if sat.solution:
            for nom,val in sat.solution.items():
                if val:
                    print(nom)
                    v=nom.split("_")
                    i=int(v[1])
                    j=int(v[2])
                    tab[i//self.L][i%self.L]=j
        for i in range(self.H):
            for j in range(self.L):
                print('{:3d}'.format(tab[i][j]),end="")
            print()

carte= Carte("test.carte")
print(carte.vals)
carte.resoudre()
