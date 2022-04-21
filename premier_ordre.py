from typing import Any, Callable, Iterable, Optional, Union
import propositionnelle


class Index:
    """
    Représente un indice.
    """
    nom: str
    valeur: Union[None, int]

    def __init__(self, nom: str) -> None:
        self.nom = nom
        self.valeur = None

    def __add__(self, dec: Union["Index", int]):
        return IndexAdd(self, dec)

    def __ne__(self, autre: Union["Index", int]) -> "Expr":
        if type(autre) is int:
            autre = Index.const(str(autre), autre)
        return RelationIndexee(self.nom+'!='+autre.nom, [self, autre], lambda indices: indices[0] != indices[1])

    def const(nom, c) -> "Index":
        """
        Définit un index constant. 
        """
        ci = Index(nom)
        ci.valeur = c
        return ci


class IndexAdd(Index):
    """
    Permet de définir la somme de deux indices.
    """

    def __init__(self, gauche: Union[Index, int], droite: Union[Index, int]) -> None:
        if isinstance(gauche, int):
            gauche = Index.const(str(gauche), gauche)
        if isinstance(droite, int):
            droite = Index.const(str(droite), droite)
        self.nom = gauche.nom + "+" + droite.nom
        self.gauche = gauche
        self.droite = droite

    @property
    def valeur(self):
        return self.gauche.valeur + self.droite.valeur


class Expr:
    """
    Une expression du premier ordre (sans fonctions, uniquement des relations).
    """

    def build(self) -> propositionnelle.Expr:
        """
        Transforme l'expression du premier ordre en formule propositionnelle.
        """
        pass

    def et(self, droite: "Expr") -> "Expr":
        return Et(self, droite)

    def ou(self, droite: "Expr") -> "Expr":
        return Ou(self, droite)

    def implique(self, droite: "Expr") -> "Expr":
        return Implique(self, droite)

    def equiv(self, droite: "Expr") -> "Expr":
        return Equiv(self, droite)

    def fnc(self):
        return self.build().forme_normale().conjonc()


class VariableIndexable:
    """
    Une variable indexable a un nom, le nombre d'indices qui peuvent l'indexer, et vals est
    un dictionnaire qui a un tuple d'indices associe la valeur si elle est connue de la variable.
    """

    def __init__(self, nom, nb_indices: int, vals: dict[any, Optional[bool]]):
        self.nom = nom
        self.nb_indices = nb_indices
        self.vals = vals

    def _(self, *indices: list[Index]) -> "VariableIndexee":
        """
        Permet de dire avec quels indices est associée la variable.
        """
        assert(len(indices) == self.nb_indices)
        return VariableIndexee(self.nom, indices, self.vals)


class VariableIndexee(Expr):
    def __init__(self, nom, indices: list[Index], vals):
        """
        Une variable indexée par les indices. Exemple a les coefficient d'une matrice
        est indexée par i et j.
        """
        self.nom = nom
        self.indices = indices
        self.vals = vals

    def build(self) -> propositionnelle.Expr:
        # On vérifie que tous les indiçages sont bien définis
        if any(map(lambda index: index.valeur is None, self.indices)):
            print("Error in var index")  # TODO: Improve error message
            raise {}
        val = self.vals[tuple(map(lambda index: index.valeur, self.indices))]
        if val is not None:
            if val:
                return propositionnelle.Top()
            else:
                return propositionnelle.Bottom()
        else:
            # On transforme la variable x indicée par (i=1,j=2) en x_1_2
            r = self.nom
            for index in self.indices:
                i = index.valeur
                r += "_" + str(i)
            return propositionnelle.Variable(r)


class RelationIndexee(Expr):
    def __init__(self, nom, indices: list[Index], relation):
        """
        Une variable indexée par les indices. Exemple a les coefficient d'une matrice
        est indexée par i et j.
        """
        self.nom = nom
        self.indices = indices
        self.relation = relation

    def build(self) -> propositionnelle.Expr:
        # On vérifie que tous les indices sont bien définis
        if any(map(lambda index: index.valeur is None, self.indices)):
            print("Error in var index")  # TODO: Improve error message
            raise {}
        val = self.relation(
            tuple(map(lambda index: index.valeur, self.indices)))
        if val:
            return propositionnelle.Top()
        else:
            return propositionnelle.Bottom()


class Pourtout(Expr):
    def __init__(self,
                 ctxt: list[Index],
                 index: Index,
                 dom: Callable[[Iterable[Index]], Iterable[int]],
                 expr: Expr) -> None:
        #  Le contexte de l'expression si (pourtout x, E) se trouve dans pourtout y (pourtout x E), le contexte est [y].
        self.ctxt = ctxt
        self.expr = expr  # L'expression contenue
        self.index = index  # L'indice lié par le pour tout. Dans l'exemple au-dessus c'est x
        self.dom = dom  # Le domaine que va parcourir l'indice.
        #                 C'est une fonction à partir de la liste du contexte retourne un itérateur sur le domaine à parcourir.

    def build(self) -> propositionnelle.Expr:
        expr: propositionnelle.Expr = propositionnelle.Top()
        for i in self.dom(self.ctxt):
            self.index.valeur = i
            e2 = self.expr.build()
            if isinstance(e2, propositionnelle.Bottom):
                return propositionnelle.Bottom()
            elif isinstance(e2, propositionnelle.Top):
                continue
            expr = expr.et(e2)
        return expr


class Ilexiste(Expr):
    def __init__(self,
                 ctxt: list[Index],
                 index: Index,
                 dom: Callable[[Iterable[Index]], Iterable[int]],
                 expr: Expr) -> None:
        # Voir Pourtout pour les explications
        self.ctxt = ctxt
        self.expr = expr
        self.index = index
        self.dom = dom

    def build(self) -> propositionnelle.Expr:
        expr: propositionnelle.Expr = propositionnelle.Bottom()
        for i in self.dom(self.ctxt):
            self.index.valeur = i
            e2 = self.expr.build()
            if isinstance(e2, propositionnelle.Bottom):
                continue
            elif isinstance(e2, propositionnelle.Top):
                return propositionnelle.Top()
            expr = expr.ou(e2)
        return expr


class Et(Expr):
    def __init__(self, gauche: Expr, droite: Expr):
        self.gauche = gauche
        self.droite = droite

    def build(self) -> propositionnelle.Expr:
        gauche = self.gauche.build()
        droite = self.droite.build()
        if isinstance(gauche, propositionnelle.Top) or isinstance(droite, propositionnelle.Bottom):
            return droite
        elif isinstance(gauche, propositionnelle.Bottom) or isinstance(droite, propositionnelle.Top):
            return gauche
        else:
            return propositionnelle.Et(gauche, droite)


class Ou(Expr):
    def __init__(self, gauche: Expr, droite: Expr):
        self.gauche = gauche
        self.droite = droite

    def build(self) -> propositionnelle.Expr:
        gauche = self.gauche.build()
        droite = self.droite.build()
        if isinstance(gauche, propositionnelle.Top) or isinstance(droite, propositionnelle.Bottom):
            return gauche
        elif isinstance(gauche, propositionnelle.Bottom) or isinstance(droite, propositionnelle.Top):
            return droite
        else:
            return propositionnelle.Ou(gauche, droite)


class Non(Expr):
    def __init__(self, expr: Expr):
        self.expr = expr

    def build(self) -> propositionnelle.Expr:
        expr = self.expr.build()
        if isinstance(expr, propositionnelle.Top):
            return propositionnelle.Bottom()
        elif isinstance(expr, propositionnelle.Bottom):
            return propositionnelle.Top()
        else:
            return propositionnelle.Non(expr)


class Equiv(Expr):
    def __init__(self, gauche: Expr, droite: Expr):
        self.gauche = gauche
        self.droite = droite

    def build(self) -> propositionnelle.Expr:
        return propositionnelle.Equiv(self.gauche.build(), self.droite.build())


class Implique(Expr):
    def __init__(self, gauche: Expr, droite: Expr):
        self.gauche = gauche
        self.droite = droite

    def build(self) -> propositionnelle.Expr:
        gauche = self.gauche.build()
        droite = self.droite.build()
        if isinstance(gauche, propositionnelle.Top):
            return droite
        elif isinstance(gauche, propositionnelle.Bottom) or isinstance(droite, propositionnelle.Top):
            return propositionnelle.Top()
        elif isinstance(droite, propositionnelle.Bottom):
            return propositionnelle.Non(gauche)
        else:
            return propositionnelle.Implique(gauche, droite)
