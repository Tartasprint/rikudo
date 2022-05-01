from typing import Iterable

POSITIF=True
NEGATIF=False

class Litteral:
    """
    Un littéral d'une FNC.

    Attributs:
        nom: Nom du littéral
        signe: Positif si True Négatif sinon
    """
    nom: str
    signe: bool
    def __init__(self, nom: str, signe: bool) -> None:
        self.nom = nom
        self.signe = signe
    
    def __eq__(self, autre: object) -> bool:
        return self.nom == autre.nom and self.signe == autre.signe
    def __hash__(self) -> int:
        return hash((self.nom,self.signe))

class Terme:
    """
    Un terme d'une FNC, contient un ensemble de littéraux.
    """
    def __init__(self, litteraux: Iterable[Litteral]) -> None:
        self.litteraux = frozenset(litteraux)
    def extend_update(self, other: "Terme") -> None:
        self.litteraux.update(other.litteraux)
    def extend(self, other: "Terme") -> None:
        return Terme(self.litteraux.union(other.litteraux))
    def __eq__(self, autre: "Terme") -> bool:
        return self.litteraux == autre.litteraux
    def __hash__(self) -> int:
        return hash(self.litteraux)
class Clause:
    """
    Une clause FNC, est un ensemble de termes qui sont des ensembles de
    littéraux.
    """
    def __init__(self, termes: Iterable[Terme]) -> None:
        self.termes = frozenset(termes)
    def extend(self, other: "Clause") -> None:
        self.termes = self.termes.union(other.termes)
    def repr(self) -> str:
        if len(self.termes) == 0:
            return "Top"
        elif self == Bottom():
            return "Bot"
        else:
            r=""
            for t in self.termes:
                for l in t.litteraux:
                    r+=(l.nom if l.signe else "-"+l.nom)+" "
                r+="\n"
            return r
    def __repr__(self) -> str:
        r="["
        for t in self.termes:
            r+='('
            for l in t.litteraux:
                r+=(l.nom if l.signe else "-"+l.nom)+" "
            r+=")"
        return r + "]"
    def __eq__(self, autre: "Clause") -> bool:
        return self.termes == autre.termes
    def __hash__(self) -> int:
        return hash(self.termes)
        
                    

def Top():
    return Clause([])

def Bottom():
    return Clause([Terme([])])