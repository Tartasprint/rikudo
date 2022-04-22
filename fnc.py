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

class Terme:
    """
    Un terme d'une FNC, contient un ensemble de littéraux.
    """
    def __init__(self, litteraux: Iterable[Litteral]) -> None:
        self.litteraux = set(litteraux)
    def extend(self, other: "Terme") -> None:
        self.litteraux.update(other.litteraux)
class Clause:
    """
    Une clause FNC, est un ensemble de termes qui sont des ensembles de
    littéraux.
    """
    def __init__(self, termes: Iterable[Terme]) -> None:
        self.termes = set(termes)
    def extend(self, other: "Clause") -> None:
        self.termes.update(other.termes)
    def repr(self) -> str:
        r=""
        for t in self.termes:
            for l in t.litteraux:
                r+=(l.nom if l.signe else "-"+l.nom)+" "
            r+="\n"
        return r
        
                    

def Top():
    return Clause([])

def Bottom():
    return Clause([Terme([])])