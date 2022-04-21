from typing import Iterable
import premier_ordre as por

n=36
d=set(range(n))
i = por.Index("i")
j = por.Index("j")
k = por.Index("k")
N = por.Index("n")
N.valeur = n

c = por.VariableIndexable("C", 2)
v = por.VariableIndexable("V", 2)
cij = c.i([i,j])
cik = c.i([i,k])
ckj = c.i([k,j])
cin = c.i([i,n])
vij = v.i([i,j])
#Dans chaque case, il y a un nombre
R1 = por.Pourtout([],
                  i,
                  lambda _: d,
                  por.Ilexiste([i],
                                j,
                                lambda _: d,
                                cij)
                  )
#Chaque nombre se trouve dans une case
R2 = por.Pourtout([],
                  j,
                  lambda _: d,
                  por.Ilexiste([j],
                                i,
                                lambda _: d,
                                cij)
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
#Chaque case ne contient qu'un seul nombre
R3 = por.Pourtout([],
                  i,
                  lambda _: d,
                  por.Pourtout([j],
                                j,
                                lambda _: d,
                                por.Pourtout([i,j],
                                            k,
                                            dom_k_diff_j,
                                            cij.implique(por.Non(cik))
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
                                            cij.implique(por.Non(ckj))
                                            )
                                )
                  )
contexte=[i,j]
superexpr= c.i([i,k]).et(c.i([j,k+1]))
domaine_moins_un=lambda _: d.difference([n-1])
existe = por.Ilexiste(contexte, k, domaine_moins_un, superexpr)
R5 = por.Pourtout([], i, lambda _: d,
        c.i([i,N]).ou(
            por.Ilexiste([i], j, lambda _: d,
                v.i([i,j]).et(existe)
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
R5FNC = R5.build().forme_normale()
print(R5FNC.repr())