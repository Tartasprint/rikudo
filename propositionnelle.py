import propositionnelle_simple as ps


class Expr:
    """
    Une formule propositionnelle.
    """

    def repr(self) -> str:
        """
        Permet de passer d'une expression à une représentation textuelle.
        """
        pass

    def et(self, droite: "Expr") -> "Expr":
        """
        Créer l'expression Et(a,b) en écrivant a.et(b).
        Si la valeur booléenne de a ou de b et connue, on optimise.
        """
        if isinstance(droite, Top):
            return self
        elif isinstance(droite, Bottom):
            return Bottom()
        else:
            return Et(self, droite)

    def ou(self, droite: "Expr") -> "Expr":
        """
        Créer l'expression Ou(a,b) en écrivant a.ou(b).
        Si la valeur booléenne de a ou de b et connue, on optimise.
        """
        if isinstance(droite, Top):
            return Top()
        elif isinstance(droite, Bottom):
            return self
        else:
            return Ou(self, droite)

    def equiv(self, droite: "Expr") -> "Expr":
        """
        Créer l'expression Equiv(a,b) en écrivant a.equiv(b)
        """
        if isinstance(droite, Top):
            return self
        elif isinstance(droite, Bottom):
            return Non(self)
        else:
            return Equiv(self, droite)

    def implique(self, droite: "Expr") -> "Expr":
        """
        Créer l'expression Implique(a,b) en écrivant a.implique(b)
        """
        if isinstance(droite, Top):
            return Top()
        elif isinstance(droite, Bottom):
            return Non(self)
        else:
            return Implique(self, droite)

    def simplif(self) -> ps.Expr:
        """
        Remplacer les équivalences et les implications dans l'expression par
        "(nonA ou B) et (A ou nonB)" et "nonA ou B" respectivement, enfin les et/ou binaires sont
        transformés en produits/sommes . L'expression devient alors une expression simple.
        """
        pass

    def forme_normale(self) -> ps.Expr:
        """
        Transforme la formule en forme normale, c'est à dire avec seulement
        des et, des ou et les négations uniquement sur des variables.
        """
        return self.simplif().deplacer_negation()


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

    def simplif(self) -> ps.Expr:
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

    def simplif(self) -> ps.Expr:
        return ps.Bottom()


class Variable(Expr):
    def __init__(self, nom: str) -> None:
        self.nom = nom

    def repr(self) -> str:
        return self.nom

    def simplif(self) -> ps.Expr:
        return ps.Variable(self.nom)


class Et(Expr):
    def __init__(self, gauche: Expr, droite: Expr) -> None:
        self.gauche = gauche
        self.droite = droite

    def repr(self) -> str:
        return "("+self.gauche.repr() + " et " + self.droite.repr()+")"

    def simplif(self) -> ps.Expr:
        r = ps.Produit([])
        gauche = self.gauche.simplif()
        droite = self.droite.simplif()
        if isinstance(gauche, ps.Produit):
            r.termes.extend(gauche.termes)
        elif isinstance(gauche,ps.Top):
            return droite
        elif isinstance(gauche,ps.Bottom):
            return ps.Bottom()
        else:
            r.termes.append(gauche)
        if isinstance(droite,ps.Produit):
            r.termes.extend(droite.termes)
        elif isinstance(droite,ps.Top):
            return gauche
        elif isinstance(gauche,ps.Bottom):
            return ps.Bottom()
        else:
            r.termes.append(droite)
        if len(r.termes) > 1:
            return r
        elif len(r.termes) == 1:
            return r.termes[0]
        else:
            return ps.Top()


class Produit(Expr):
    def __init__(self, termes: list[Expr]) -> None:
        self.termes = termes

    def repr(self) -> str:
        return "ET(" + ",".join(t.repr() for t in self.termes) + ")"

    def simplif(self) -> ps.Expr:
        r=ps.Produit([])
        for t in self.termes:
            ts=t.simplif()
            if isinstance(ts,ps.Produit):
                r.termes.extend(ts.termes)
            elif isinstance(ts,ps.Top):
                continue
            elif isinstance(ts,ps.Bottom):
                return ps.Bottom()
            else:
                r.termes.append(ts)
        if len(r.termes) > 1:
            return r
        elif len(r.termes) == 1:
            return r.termes[0]
        else:
            return ps.Top()

class Ou(Expr):
    def __init__(self, gauche: Expr, droite: Expr) -> None:
        self.gauche = gauche
        self.droite = droite

    def repr(self) -> str:
        return "("+self.gauche.repr() + " ou " + self.droite.repr()+")"

    def simplif(self) -> ps.Expr:
        r = ps.Somme([])
        gauche = self.gauche.simplif()
        droite = self.droite.simplif()
        if isinstance(gauche,ps.Somme):
            r.termes.extend(gauche.termes)
        elif isinstance(gauche,ps.Top):
            return ps.Bottom()
        elif isinstance(gauche,ps.Bottom):
            return droite
        else:
            r.termes.append(gauche)
        if isinstance(droite,ps.Somme):
            r.termes.extend(droite.termes)
        elif isinstance(droite,ps.Top):
            return ps.Top()
        elif isinstance(gauche,ps.Bottom):
            return gauche
        else:
            r.termes.append(droite)
        if len(r.termes) > 1:
            return r
        elif len(r.termes) == 1:
            return r.termes[0]
        else:
            return ps.Top() 
class Somme(Expr):
    def __init__(self, termes: list[Expr]) -> None:
        self.termes = termes

    def repr(self) -> str:
        return "OU(" + ",".join(t.repr() for t in self.termes) + ")"

    def simplif(self) -> ps.Expr:
        r=ps.Somme([])
        for t in self.termes:
            ts=t.simplif()
            if isinstance(ts,ps.Somme):
                r.termes.extend(ts.termes)
            elif isinstance(ts,ps.Top):
                return ps.Top()
            elif isinstance(ts,ps.Bottom):
                continue
            else:
                r.termes.append(ts)
        if len(r.termes) > 1:
            return r
        elif len(r.termes) == 1:
            return r.termes[0]
        else:
            return ps.Top() 

class Non(Expr):
    def __init__(self, expr: Expr) -> None:
        self.expr = expr

    def repr(self) -> str:
        return "non(" + self.expr.repr()+")"

    def simplif(self) -> ps.Expr:
        return ps.Non(self.expr.simplif())


class Equiv(Expr):
    def __init__(self, gauche: Expr, droite: Expr) -> None:
        self.gauche = gauche
        self.droite = droite

    def simplif(self) -> ps.Expr:
        g = self.gauche.simplif()
        d = self.droite.simplif()
        return ps.Produit([
            ps.Somme([
                ps.Non(g),
                d]),
            ps.Somme([
                g,
                ps.Non(d)
            ])])

    def repr(self) -> str:
        return "("+self.gauche.repr() + " <=> " + self.droite.repr()+")"


class Implique(Expr):
    def __init__(self, gauche: Expr, droite: Expr) -> None:
        self.gauche = gauche
        self.droite = droite

    def repr(self) -> str:
        return "("+self.gauche.repr() + " => " + self.droite.repr()+")"

    def simplif(self) -> ps.Expr:
        g = self.gauche.simplif()
        d = self.droite.simplif()
        return ps.Somme([
                ps.Non(g),
                d
            ])
