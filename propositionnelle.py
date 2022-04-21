from inspect import isclass
import propositionnelle_simple as ps


class Expr:
    """
    Une formule propositionnelle.
    """

    def repr(self) -> str:
        """
        Permet de passer d'un object expression à du texte
        """
        pass

    def et(self, droite: "Expr") -> "Expr":
        """
        Créer l'expression Et(a,b) en écrivant a.et(b)
        """
        return Et(self, droite)

    def ou(self, droite: "Expr") -> "Expr":
        """
        Créer l'expression Ou(a,b) en écrivant a.ou(b)
        """
        return Ou(self, droite)

    def equiv(self, droite: "Expr") -> "Expr":
        """
        Créer l'expression Equiv(a,b) en écrivant a.equiv(b)
        """
        return Equiv(self, droite)

    def implique(self, droite: "Expr") -> "Expr":
        """
        Créer l'expression Implique(a,b) en écrivant a.implique(b)
        """
        return Implique(self, droite)

    def equiv_elim(self) -> ps.Expr:
        """
        Remplacer les équivalences et les implications dans l'expression par
        "(nonA ou B) et (A ou nonB)" et "nonA ou B" respectivement. L'expression
        devient alors une expression simple.
        """
        pass

    def forme_normale(self) -> ps.Expr:
        """
        Transforme la formule en forme normale, c'est à dire avec seulement
        des et, des ou et les négations uniquement sur des variables.
        """
        return self.equiv_elim().deplacer_negation()


class Top(Expr):
    def __init__(self) -> None:
        super().__init__()

    def repr(self) -> str:
        return "TOP"

    def et(self, droite: Expr) -> Expr:
        return droite

    def ou(self, droite: Expr) -> Expr:
        return Top()

    def equiv(self, droite: Expr) -> Expr:
        return droite

    def implique(self, droite: Expr) -> Expr:
        return droite

    def equiv_elim(self) -> ps.Expr:
        return ps.Top()


class Bottom(Expr):
    def repr(self) -> str:
        return "BOT"

    def et(self, droite: Expr) -> Expr:
        return Bottom()

    def ou(self, droite: Expr) -> Expr:
        return droite

    def equiv(self, droite: Expr) -> Expr:
        return Non(droite)

    def implique(self, droite: Expr) -> Expr:
        return Top()

    def equiv_elim(self) -> ps.Expr:
        return ps.Bottom()


class Variable(Expr):
    def __init__(self, nom: str) -> None:
        self.nom = nom

    def repr(self) -> str:
        return self.nom

    def equiv_elim(self) -> ps.Expr:
        return ps.Variable(self.nom)


class Et(Expr):
    def __init__(self, gauche: Expr, droite: Expr) -> None:
        self.gauche = gauche
        self.droite = droite

    def repr(self) -> str:
        return "("+self.gauche.repr() + " et " + self.droite.repr()+")"

    def equiv_elim(self) -> ps.Expr:
        return self.gauche.equiv_elim().et(self.droite.equiv_elim())


class Ou(Expr):
    def __init__(self, gauche: Expr, droite: Expr) -> None:
        self.gauche = gauche
        self.droite = droite

    def repr(self) -> str:
        return "("+self.gauche.repr() + " ou " + self.droite.repr()+")"

    def equiv_elim(self) -> ps.Expr:
        return self.gauche.equiv_elim().ou(self.droite.equiv_elim())


class Non(Expr):
    def __init__(self, expr: Expr) -> None:
        self.expr = expr

    def repr(self) -> str:
        return "non(" + self.expr.repr()+")"

    def equiv_elim(self) -> ps.Expr:
        return ps.Non(self.expr.equiv_elim())


class Equiv(Expr):
    def __init__(self, gauche: Expr, droite: Expr) -> None:
        self.gauche = gauche
        self.droite = droite

    def equiv_elim(self) -> ps.Expr:
        g = self.gauche.equiv_elim()
        d = self.droite.equiv_elim()
        return (ps.Non(g).ou(d)).et(g.ou(ps.Non(d)))

    def repr(self) -> str:
        return "("+self.gauche.repr() + " <=> " + self.droite.repr()+")"


class Implique(Expr):
    def __init__(self, gauche: Expr, droite: Expr) -> None:
        self.gauche = gauche
        self.droite = droite

    def repr(self) -> str:
        return "("+self.gauche.repr() + " => " + self.droite.repr()+")"

    def equiv_elim(self) -> ps.Expr:
        g = self.gauche.equiv_elim()
        d = self.droite.equiv_elim()
        return ps.Non(g).ou(d)
