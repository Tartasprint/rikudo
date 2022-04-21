from inspect import isclass


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


class Variable(Expr):
    def __init__(self, nom: str) -> None:
        self.nom = nom

    def repr(self) -> str:
        return self.nom

    def deplacer_negation(self) -> "Expr":
        return self

    def nier(self) -> "Expr":
        return Non(self)


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


class Non(Expr):
    def __init__(self, expr: Expr) -> None:
        self.expr = expr

    def repr(self) -> str:
        return "non(" + self.expr.repr()+")"

    def nier(self) -> Expr:
        return self.expr.nier()

    def deplacer_negation(self) -> "Expr":
        if not isinstance(self.expr, Variable):  # On évite une boucle infinie
            return self.expr.nier().deplacer_negation()
        else:
            return self
