import fnc

class Expr:
    def repr(self) -> str:
        pass

    def deplacer_negation(self) -> "Expr":
        pass

    def nier(self) -> "Expr":
        pass

    def conjonc(self) -> fnc.Clause:
        pass


class Top(Expr):
    def __init__(self) -> None:
        super().__init__()

    def repr(self) -> str:
        return "TOP"

    def deplacer_negation(self) -> "Expr":
        return self

    def nier(self) -> "Expr":
        return Bottom()

    def conjonc(self) -> fnc.Clause:
        return fnc.Top()


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

    def conjonc(self) -> fnc.Clause:
        return fnc.Bottom()


class Variable(Expr):
    def __init__(self, nom: str) -> None:
        self.nom = nom

    def repr(self) -> str:
        return self.nom

    def deplacer_negation(self) -> "Expr":
        return self

    def nier(self) -> "Expr":
        return Non(self)

    def conjonc(self) -> fnc.Clause:
        return fnc.Clause([fnc.Terme([fnc.Litteral(self.nom,fnc.POSITIF)])])

class Produit(Expr):
    def __init__(self, termes: list[Expr]) -> None:
        self.termes = termes
    def repr(self) -> str:
        return "Et(" + ",".join(t.repr() for t in self.termes) + ")"
    def deplacer_negation(self) -> "Expr":
        return Produit([t.deplacer_negation() for t in self.termes])

    def nier(self) -> Expr:
        return Somme([t.nier() for t in self.termes])

    def conjonc(self) -> fnc.Clause:
        l=fnc.Top()
        for t in self.termes:
            l.extend(t.conjonc())
        return l


class Somme(Expr):
    def __init__(self, termes: list[Expr]) -> None:
        self.termes = termes
    def repr(self) -> str:
        return "Ou(" + ",".join(t.repr() for t in self.termes) + ")"
    def deplacer_negation(self) -> "Expr":
        return Somme([t.deplacer_negation() for t in self.termes])

    def nier(self) -> Expr:
        return Produit([t.nier() for t in self.termes])

    def conjonc(self) -> fnc.Clause:
        l=fnc.Bottom() # Clause[Terme[]]
        for t in self.termes:
            tc =t.conjonc()
            for t_terme in tc.termes:
                for l_terme in l.termes:
                    l_terme.extend(t_terme)
        return l

class Non(Expr):
    def __init__(self, expr: Expr) -> None:
        self.expr = expr

    def repr(self) -> str:
        return "non(" + self.expr.repr()+")"

    def nier(self) -> Expr:
        return self.expr

    def deplacer_negation(self) -> Expr:
        if not isinstance(self.expr, Variable):  # On évite une boucle infinie
            return self.expr.nier().deplacer_negation()
        else:
            return self

    def conjonc(self) -> fnc.Clause:
        assert(isinstance(self.expr, Variable))
        return fnc.Clause([fnc.Terme([fnc.Litteral(self.expr.nom,fnc.NEGATIF)])])