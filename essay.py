from typing import Dict, Iterable, List

class Index:
    def __init__(self, nom: str) -> None:
        self.nom = nom

class Expr:
    def repr(self) -> str:
        pass
    def et(self,gauche) -> "Expr":
        return Et(self,gauche)
    def ou(self,gauche) -> "Expr":
        return Ou(self,gauche)
    def build(self,ctxt: dict[Index,int]) -> "Expr":
        pass


class Variable(Expr):
    def __init__(self, nom: str):
        self.nom = nom

    def repr(self) -> str:
        return self.nom
    def build(self, ctxt: dict[Index, int]) -> "Expr":
        return self





class VariableIndexee:
    def __init__(self, nom: str, indices: List[Index]):
        self.nom = nom
        self.indices = indices

    def build(self, ctxt: dict[Index,int]) -> Variable:
        r = self.nom
        for index in self.indices:
            i=ctxt.get(index)
            if i is None:
                print("Error in var index") # TODO: Improve error message
                raise {}
            else:
                r+="_" + str(ctxt[index])
        return Variable(r)

class Pourtout:
    def __init__(self, ctxt: List[Index],index: Index, expr: Expr) -> None:
        self.ctxt = ctxt
        self.expr = expr
        self.index = index
    def build(self, ctxt: dict[Index,int], dom: Iterable[int]) -> Expr:
        if not any(True for _ in dom): # Dom est vide
            pass
        else:
            dom=iter(dom)
            first = next(dom)
            ctxt[self.index] = first
            expr = self.expr.build(ctxt)
            for i in dom:
                ctxt[self.index] = i
                expr = expr.et(self.expr.build(ctxt))
            return expr
class Ilexiste:
    def __init__(self, ctxt: List[Index],index: Index, expr: Expr) -> None:
        self.ctxt = ctxt
        self.expr = expr
        self.index = index
    def build(self, ctxt: dict[Index,int], dom: Iterable[int]) -> Expr:
        if not any(True for _ in dom): # Dom est vide
            pass
        else:
            first = next(dom)
            ctxt[self.index] = first
            expr = self.expr.build(ctxt)
            for i in dom:
                ctxt[self.index] = i
                expr = expr.ou(self.expr.build(ctxt))
            return expr


class Non(Expr):
    def __init__(self, inner: Expr, right: Variable) -> None:
        self.inner = inner

    def repr(self) -> str:
        return "-" + self.inner.repr()
    def build(self, ctxt: dict[Index, int]) -> "Expr":
        return Non(self.inner.build())
class Et(Expr):
    def __init__(self, left: Expr, right: Variable) -> None:
        self.left = left
        self.right = right
    def repr(self) -> str:
        return self.left.repr() + " et " + self.right.repr()
    def build(self, ctxt: dict[Index, int]) -> "Expr":
        return Et(self.left.build(),self.right.build())

class Ou(Expr):
    def __init__(self, left: Expr, right: Variable) -> None:
        self.left = left
        self.right = right
    def repr(self) -> str:
        return self.left.repr() + " ou " + self.right.repr()
    def build(self, ctxt: dict[Index, int]) -> "Expr":
        return Ou(self.left.build(),self.right.build())

indice = Index("i")
x=VariableIndexee("x",[indice])
fo=Pourtout([],indice,x)
prop=fo.build({},[1,2,3])
print(prop.repr())