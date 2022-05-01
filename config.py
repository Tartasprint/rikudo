# Modifier cette ligne pour changer la commande du sat solveur.
sat=lambda input,output: f"minisat \"{input}\" \"{output}\""
# Afficher les formes normales conjonctives correspondant à chaque règle.
afficher_fnc=False