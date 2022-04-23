import unittest
import propositionnelle_simple as ps
import fnc

class TestStringMethods(unittest.TestCase):

    def test_dev_simple(self):
        f=ps.Somme([
            ps.Produit([
                ps.Variable('a'),
                ps.Variable('b'),
                ]),
            ps.Variable('c'),
            ])
        self.assertEqual(
            f.conjonc(), 
            fnc.Clause([
                fnc.Terme([
                    fnc.Litteral('a', True),
                    fnc.Litteral('c', True),
                    ]),
                fnc.Terme([
                    fnc.Litteral('b', True),
                    fnc.Litteral('c', True),
                ])
            ])
        )
    def test_double(self):
        f=ps.Somme([
            ps.Produit([
                ps.Variable('a'),
                ps.Variable('b'),
                ]),
            ps.Produit([
                ps.Variable('c'),
                ps.Variable('d'),
                ]),
            ])
        self.assertEqual(
            f.conjonc(), 
            fnc.Clause([
                fnc.Terme([
                    fnc.Litteral('a', True),
                    fnc.Litteral('c', True),
                    ]),
                fnc.Terme([
                    fnc.Litteral('b', True),
                    fnc.Litteral('c', True),
                ]),
                fnc.Terme([
                    fnc.Litteral('a', True),
                    fnc.Litteral('d', True),
                    ]),
                fnc.Terme([
                    fnc.Litteral('b', True),
                    fnc.Litteral('d', True),
                ])
            ])
        )


if __name__ == '__main__':
    unittest.main()