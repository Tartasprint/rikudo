from inspect import isclass

from six import b


class Expr:
    def repr(self) -> str:
        pass

    def et(self, droite: "Expr") -> "Expr":
        return Et(self, droite)

    def ou(self, droite: "Expr") -> "Expr":
        return Ou(self, droite)

    def deplacer_negation(self) -> "Expr":
        pass

    def nier(self) -> "Expr":
        pass

    def conjonc(self) -> "Expr":
        pass

    def conjonc_aux(self) -> "Expr":
        return self.conjonc(), False


class Top(Expr):
    def __init__(self) -> None:
        super().__init__()

    def repr(self) -> str:
        return "TOP"

    def et(self, droite: Expr) -> Expr:
        return droite

    def ou(self, droite: Expr) -> Expr:
        return Top()

    def deplacer_negation(self) -> "Expr":
        return self

    def nier(self) -> "Expr":
        return Bottom()

    def conjonc(self) -> "Expr":
        return self


class Bottom(Expr):
    def repr(self) -> str:
        return "BOT"

    def et(self, droite: Expr) -> Expr:
        return Bottom()

    def ou(self, droite: Expr) -> Expr:
        return droite

    def deplacer_negation(self) -> "Expr":
        return self

    def nier(self) -> "Expr":
        return Top()

    def conjonc(self) -> "Expr":
        return self


class Variable(Expr):
    def __init__(self, nom: str) -> None:
        self.nom = nom

    def repr(self) -> str:
        return self.nom

    def deplacer_negation(self) -> "Expr":
        return self

    def nier(self) -> "Expr":
        return Non(self)

    def conjonc(self) -> "Expr":
        return self


class Et(Expr):
    def __init__(self, gauche: Expr, droite: Expr) -> None:
        self.gauche = gauche
        self.droite = droite

    def repr(self) -> str:
        return "("+self.gauche.repr() + " et " + self.droite.repr()+")"

    def deplacer_negation(self) -> "Expr":
        return self.gauche.deplacer_negation().et(self.droite.deplacer_negation())

    def nier(self) -> Expr:
        return self.gauche.nier().ou(self.droite.nier())

    def conjonc(self) -> "Expr":
        return self.gauche.conjonc().et(self.droite.conjonc())


class Ou(Expr):
    def __init__(self, gauche: Expr, droite: Expr) -> None:
        self.gauche = gauche
        self.droite = droite

    def repr(self) -> str:
        return "("+self.gauche.repr() + " ou " + self.droite.repr()+")"

    def deplacer_negation(self) -> "Expr":
        return self.gauche.deplacer_negation().ou(self.droite.deplacer_negation())

    def nier(self) -> Expr:
        return self.gauche.nier().et(self.droite.nier())

    def conjonc(self) -> "Expr":
        if isinstance(self.gauche, Et):
            # (A et B) ou C ==> (A ou C) et (B ou C)
            return (self.gauche.droite.ou(self.droite)).et(self.gauche.gauche.ou(self.droite)).conjonc()
        elif isinstance(self.droite, Et):
            # A ou (B et C) ==> (A ou B) et (A ou C)
            return (self.gauche.ou(self.droite.droite)).et(self.gauche.ou(self.droite.gauche)).conjonc()
        expr, change = self.conjonc_aux()
        while change:
            expr, change = expr.conjonc_aux()
        return expr
        # (a ou b) ou c =>

    def conjonc_aux(self) -> tuple[Expr, bool]:
        if isinstance(self.gauche, Et):
            # (A et B) ou C ==> (A ou C) et (B ou C)
            return (self.gauche.droite.ou(self.droite)).et(self.gauche.gauche.ou(self.droite)).conjonc(), True
        elif isinstance(self.droite, Et):
            # A ou (B et C) ==> (A ou B) et (A ou C)
            return (self.gauche.ou(self.droite.droite)).et(self.gauche.ou(self.droite.gauche)).conjonc(), True
        if isinstance(self.gauche, Ou):
            expr, change = self.gauche.conjonc_aux()
            while change:
                expr, change = expr.conjonc_aux()
            gauche = expr
        else:
            gauche = self.gauche
        if isinstance(self.droite, Ou):
            expr, change = self.droite.conjonc_aux()
            while change:
                expr, change = expr.conjonc_aux()
            droite = expr
        else:
            droite = self.droite
        if isinstance(gauche, Et):
            # (A et B) ou C ==> (A ou C) et (B ou C)
            return (gauche.droite.ou(droite)).et(gauche.gauche.ou(droite)).conjonc(), True
        elif isinstance(droite, Et):
            # A ou (B et C) ==> (A ou B) et (A ou C)
            return (gauche.ou(droite.droite)).et(gauche.ou(droite.gauche)).conjonc(), True
        return self.gauche.ou(self.droite), False


class Non(Expr):
    def __init__(self, expr: Expr) -> None:
        self.expr = expr

    def repr(self) -> str:
        return "non(" + self.expr.repr()+")"

    def nier(self) -> Expr:
        return self.expr

    def deplacer_negation(self) -> "Expr":
        if not isinstance(self.expr, Variable):  # On évite une boucle infinie
            return self.expr.nier().deplacer_negation()
        else:
            return self

    def conjonc(self) -> "Expr":
        return self
#
