from dimacs import Dimacs
import premier_ordre as por
import fnc


def generer_regles(domaine: set[int], grille_depart, voisins):
    """
    Génère les règles 1-5 suivant le domaine donné(`domaine`), les nombres que l'on sait
    ou non remplis (`grille_depart`), une fonction `voisins` qui décide si i et j sont voisins.
    """
    i = por.Index("i")
    j = por.Index("j")
    k = por.Index("k")
    N = len(domaine)
    n = por.Index.const("n", N-1)
    # Variable C_i_j représentant la proposition "Dans la case i il y a le nombre j"
    c = por.VariableIndexable("C", 2, grille_depart)
    voisinage = {(i, j): voisins(i,j) for i in domaine for j in domaine}
    # Variable V_i_j représentant la proposition "La case i est voisine de la case j"
    v = por.VariableIndexable("V", 2, voisinage)
    # Dans chaque case, il y a un nombre
    R1 = por.Pourtout(i, domaine,
                    por.Ilexiste(j, domaine,
                                c._(i, j))
                    )
    # Chaque nombre se trouve dans une case
    R2 = por.Pourtout(j,
                    domaine,
                    por.Ilexiste(i, domaine,
                                c._(i, j))
                    )

    # Chaque case ne contient qu'un seul nombre
    R3 = por.Pourtout(i, domaine,
                    por.Pourtout(j, domaine,
                                por.Pourtout(k,
                                                domaine,
                                                (k != j).implique(
                                                c._(i, j).implique(
                                                    por.Non(c._(i, k)))
                                                ))
                                )
                    )
    # Chaque nombre n'apparait que dans une case
    R4 = por.Pourtout(i,domaine,
                    por.Pourtout(j, domaine,
                                por.Pourtout(k, domaine,
                                                (k != i).implique(
                                                c._(i, j).implique(
                                                    por.Non(c._(k, j)))
                                                ))
                                )
                    )

    # Chaque case:
    #   soit contient le dernier nombre,
    #   soit a une voisine qui est sa suivante.
    # (L'exclusivité du soit étant exprimée dans les règle 3-4)
    R5 = por.Pourtout(i,domaine,
                    c._(i, n).ou(
        por.Ilexiste(j, domaine,
                    v._(i, j).et(
            por.Ilexiste(k, domaine.difference([N-1]),
                        c._(i, k).et(c._(j, k+1)))
        )
        )
    ))

    # On ajoute une règle RC pour que les cases préremplies apparaissent dans les résultats
    # du SAT-Solveur
    RC = fnc.Top()
    for idxs,val in c.vals.items():
        if val is not None:
            nom=c.nom
            for i in idxs:
                nom += "_" + str(i)
            t=fnc.Terme([
                fnc.Litteral(nom, val)
            ])
            RC.extend(fnc.Clause([t]))
    return [R1,R2,R3,R4,R5],RC