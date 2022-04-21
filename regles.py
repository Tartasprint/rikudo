from collections import defaultdict
from typing import Iterable
import premier_ordre as por

N=36
d=set(range(N))
i = por.Index("i")
j = por.Index("j")
k = por.Index("k")
n = por.Index.const("n",N-1)

c = por.VariableIndexable("C", 2, defaultdict(lambda: None))
# Configuration de la carte
# 01
# 23
v = por.VariableIndexable("V", 2, {(i,j): abs(i-j) == N or abs(i-j)==1 for i in range(N) for j in range(N)})

#Dans chaque case, il y a un nombre
R1 = por.Pourtout([],
                  i,
                  lambda _: d,
                  por.Ilexiste([i],
                                j,
                                lambda _: d,
                                c._(i,j))
                  )
#Chaque nombre se trouve dans une case
R2 = por.Pourtout([],
                  j,
                  lambda _: d,
                  por.Ilexiste([j],
                                i,
                                lambda _: d,
                                c._(i,j))
                  )
def dom_k_diff_j(ctxt: Iterable[por.Index]) -> set[int]:
        ctxt = iter(ctxt)
        i = next(ctxt)
        j = next(ctxt)
        return d.difference([j.valeur])
def dom_k_diff_j(ctxt: Iterable[por.Index]) -> set[int]:
        ctxt = iter(ctxt)
        i = next(ctxt)
        j = next(ctxt)
        return d.difference([j.valeur])
# Chaque case ne contient qu'un seul nombre
R3 = por.Pourtout([],
                  i,
                  lambda _: d,
                  por.Pourtout([j],
                                j,
                                lambda _: d,
                                por.Pourtout([i,j],
                                            k,
                                            dom_k_diff_j,
                                            c._(i,j).implique(por.Non(c._(i,k)))
                                            )
                                )
                  )
#Chaque nombre n'apparait que dans une case
R4 = por.Pourtout([],
                  i,
                  lambda _: d,
                  por.Pourtout([j],
                                j,
                                lambda _: d,
                                por.Pourtout([i,j],
                                            k,
                                            dom_k_diff_j,
                                            c._(i,j).implique(por.Non(c._(k,j)))
                                            )
                                )
                  )
domaine_moins_un=lambda _: d.difference([N-1])
R5 = por.Pourtout([], i, lambda _: d,
        c._(i,n).ou(
            por.Ilexiste([i], j, lambda _: d,
                v._(i,j).et(
                        por.Ilexiste([i,j], k, domaine_moins_un,
                        c._(i,k).et(c._(j,k+1)))
                )
            )
        ))
R1FNC = R1.build().forme_normale().conjonc()
print(R1FNC.repr(),("1"*80+"\n")*10)
R2FNC = R2.build().forme_normale().conjonc()
print(R2FNC.repr(),("2"*80+"\n")*10)
R3FNC = R3.build().forme_normale().conjonc()
print(R3FNC.repr(),("3"*80+"\n")*10)
R4FNC = R4.build().forme_normale().conjonc()
print(R4FNC.repr(),("4"*80+"\n")*10)
print(domaine_moins_un(3))
R5FNC = R5.build().forme_normale()
print(R5FNC.repr())