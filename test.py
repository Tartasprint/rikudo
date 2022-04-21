from typing import Iterable


def x_diff_y():
    import premier_ordre as por
    i=por.Index("i")
    j=por.Index("j")
    x=por.VariableIndexee("x",[i,j])
    d=set(range(6))
    def j_diff_i(ctxt: Iterable[por.Index]) -> set[int]:
        ctxt=iter(ctxt)
        i=next(ctxt)
        return d.difference([i.valeur])
    po=por.Pourtout([],i, lambda _: range(5),
        por.Pourtout([i], j, j_diff_i, x))
    prop=po.build()
    print(prop.repr())
def forme_normale():
    import propositionnelle as pr
    a=pr.Variable("a")
    b=pr.Variable("b")
    c=pr.Variable("c")
    d=pr.Variable("d")
    form = pr.Non(((a.implique(b)).et(c)).ou(a.et(d)))
    print(form.forme_normale().repr())
forme_normale()