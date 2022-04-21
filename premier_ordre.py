from typing import Callable, Iterable, Optional, Union
import propositionnelle


class Index:
    """
    Représente un indice qui varie dans les .
    """
    nom: str
    valeur: Union[None, int]

    def __init__(self, nom: str) -> None:
        self.nom = nom
        self.valeur = None


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

    def fnc(self):
        pass


class VariableIndexee(Expr):
    def __init__(self, nom, indices: list[Index]):
        """
        Une variable indexée par les indices. Exemple a les coefficient d'une matrice
        est indexée par i et j.
        """
        self.nom = nom
        self.indices = indices

    def build(self) -> propositionnelle.Expr:
        # On transforme la variable x indicée par (i=1,j=2) en x_1_2
        r = self.nom
        for index in self.indices:
            i = index.valeur
            if i is None:
                print("Error in var index")  # TODO: Improve error message
                raise {}
            else:
                r += "_" + str(i)
        return propositionnelle.Variable(r)


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
        #                C'est une fonction qui reçoit la liste du contexte et qui retourne un itérateur sur le domaine à parcourir.

    def build(self) -> propositionnelle.Expr:
        expr: propositionnelle.Expr = propositionnelle.Top()
        for i in self.dom(self.ctxt):
            self.index.valeur = i
            expr = expr.et(self.expr.build())
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
            expr = expr.ou(self.expr.build())
        return expr


class Et(Expr):
    def __init__(self, gauche: Expr, droite: Expr):
        self.gauche = gauche
        self.droite = droite

    def build(self) -> propositionnelle.Expr:
        return propositionnelle.Et(self.gauche.build(), self.droite.build())


class Ou(Expr):
    def __init__(self, gauche: Expr, droite: Expr):
        self.gauche = gauche
        self.droite = droite

    def build(self) -> propositionnelle.Expr:
        return propositionnelle.Ou(self.gauche.build(), self.droite.build())


class Non(Expr):
    def __init__(self, expr: Expr):
        self.expr = expr

    def build(self) -> propositionnelle.Expr:
        return propositionnelle.Non(self.expr.build())


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
        return propositionnelle.Implique(self.gauche.build(), self.droite.build())
