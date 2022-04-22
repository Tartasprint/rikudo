# Les fichiers
## Essais
`essay.py`: première esquisse

`test.py`: fichier pour tester les modules de logique.
## Logique
Fichiers pour écrire de la logique de façon assez générale:

* `premier_ordre.py`: Fonctions pour exprimer une formule du premier ordre et passer au propositionnel

* `propositionnelle.py`: Fonctions  pour exprimer une formule propositionnelle (avec <=> et =>)

* `propositionnelle_simple.py`: Fonctions pour exprimer une formule propositionnelle (sans <=> et =>) et passer en forme normale

* `fnc.py`: La forme normale conjonctive

* `dimacs.py`: Gère la communication avec un SAT solveur en communiquant avec des fichiers DIMACS.

## Projet
Fichiers qui concernent le projet:

* `regles.py`: Les règles décrites dans le rendu de projet (`Theorie.pdf`).



# Timings
FNC pour:

N=3: 0,08514s
N=4: 0,08417s
N=5: 0,15573s
N=6: 0,15191s
N=7: 3,28s
N=8: 19,48s
N=9: 98,94s
