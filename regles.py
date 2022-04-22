from dimacs import Dimacs
import premier_ordre as por
import fnc


def generer_regles(domaine: set[int], nombre_depart, voisins):
    i = por.Index("i")
    j = por.Index("j")
    k = por.Index("k")
    N = len(domaine)
    n = por.Index.const("n", N-1)
    c = por.VariableIndexable("C", 2, nombre_depart)
    voisinage = {(i, j): voisins(i,j) for i in domaine for j in domaine}
    print(voisinage)
    v = por.VariableIndexable("V", 2, voisinage)
    # Dans chaque case, il y a un nombre
    R1 = por.Pourtout([],
                    i,
                    lambda _: domaine,
                    por.Ilexiste([i],
                                j,
                                lambda _: domaine,
                                c._(i, j))
                    )
    # Chaque nombre se trouve dans une case
    R2 = por.Pourtout([],
                    j,
                    lambda _: domaine,
                    por.Ilexiste([j],
                                i,
                                lambda _: domaine,
                                c._(i, j))
                    )

    # Chaque case ne contient qu'un seul nombre
    R3 = por.Pourtout([],
                    i,
                    lambda _: domaine,
                    por.Pourtout([j],
                                j,
                                lambda _: domaine,
                                por.Pourtout([i, j],
                                                k,
                                                lambda _: domaine,
                                                (k != j).implique(
                                                c._(i, j).implique(
                                                    por.Non(c._(i, k)))
                                                ))
                                )
                    )
    # Chaque nombre n'apparait que dans une case
    R4 = por.Pourtout([],
                    i,
                    lambda _: domaine,
                    por.Pourtout([j],
                                j,
                                lambda _: domaine,
                                por.Pourtout([i, j],
                                                k,
                                                lambda _: domaine,
                                                (k != i).implique(
                                                c._(i, j).implique(
                                                    por.Non(c._(k, j)))
                                                ))
                                )
                    )


    R5 = por.Pourtout([], i, lambda _: domaine,
                    c._(i, n).ou(
        por.Ilexiste([i], j, lambda _: domaine,
                    v._(i, j).et(
            por.Ilexiste([i, j], k, lambda _: domaine.difference([N-1]),
                        c._(i, k).et(c._(j, k+1)))
        )
        )
    ))
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
    return [R1,R2,R3,R4,R5],RC