from collections import defaultdict
from typing import Iterable
import premier_ordre as por
import fnc
import os

H=3
L=3
N = H*L
d = set(range(N))
i = por.Index("i")
j = por.Index("j")
k = por.Index("k")
n = por.Index.const("n", N-1)

first_numbers={(i,j): None for i in d for j in d}
first_numbers[0,0]=True
#
##first_numbers[8,8]=True
c = por.VariableIndexable("C", 2, first_numbers)
## Configuration de la carte
## 0 5 6
## 1 4 7
## 2 3 8

def voisins(i: int, j: int):
    return (i//H == j//H and abs(i-j) == 1) or (i%L == j%L and abs(i//H-j//H) == 1)
voisinage = {(i, j): voisins(i,j) for i in range(N) for j in range(N)}
print(voisinage)
v = por.VariableIndexable("V", 2, voisinage)

# Dans chaque case, il y a un nombre
R1 = por.Pourtout([],
                  i,
                  lambda _: d,
                  por.Ilexiste([i],
                               j,
                               lambda _: d,
                               c._(i, j))
                  )
# Chaque nombre se trouve dans une case
R2 = por.Pourtout([],
                  j,
                  lambda _: d,
                  por.Ilexiste([j],
                               i,
                               lambda _: d,
                               c._(i, j))
                  )

# Chaque case ne contient qu'un seul nombre
R3 = por.Pourtout([],
                  i,
                  lambda _: d,
                  por.Pourtout([j],
                               j,
                               lambda _: d,
                               por.Pourtout([i, j],
                                            k,
                                            lambda _: d,
                                            (k != j).implique(
                                            c._(i, j).implique(
                                                por.Non(c._(i, k)))
                                            ))
                               )
                  )
# Chaque nombre n'apparait que dans une case
R4 = por.Pourtout([],
                  i,
                  lambda _: d,
                  por.Pourtout([j],
                               j,
                               lambda _: d,
                               por.Pourtout([i, j],
                                            k,
                                            lambda _: d,
                                            (k != i).implique(
                                            c._(i, j).implique(
                                                por.Non(c._(k, j)))
                                            ))
                               )
                  )


def domaine_moins_un(_): return d.difference([N-1])


R5 = por.Pourtout([], i, lambda _: d,
                  c._(i, n).ou(
    por.Ilexiste([i], j, lambda _: d,
                 v._(i, j).et(
        por.Ilexiste([i, j], k, domaine_moins_un,
                     c._(i, k).et(c._(j, k+1)))
    )
    )
))

#print(R5.build().repr())


def tout():
    R1FNC = R1.fnc()
    R2FNC = R2.fnc()
    R3FNC = R3.fnc()
    R4FNC = R4.fnc()
    R5FNC = R5.fnc()

    RG = fnc.Top()
    RG.extend(R1FNC)
    RG.extend(R2FNC)
    RG.extend(R3FNC)
    RG.extend(R4FNC)
    RG.extend(R5FNC)

    RC = fnc.Top()
    for idxs,val in c.vals.items():
        if val is not None:
            print(idxs)
            nom=c.nom
            for i in idxs:
                nom += "_" + str(i)
            t=fnc.Terme([
                fnc.Litteral(nom, val)
            ])
            RC.extend(fnc.Clause([t]))
    RG.extend(RC)
    sat=RG.dimacs()
    sat.resoudre()
    
tout()

#print("1"*15+"\n",R5.build().repr())
#print("2"*15+"\n",R5.build().simplif().repr())
#print("3"*15+"\n",R5.build().simplif().deplacer_negation().repr())
#print("4"*15+"\n",R5.build().simplif().deplacer_negation().conjonc().repr())