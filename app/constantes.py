import csv

"""
Nombre de pokemons à afficher par colonne dans une table html
"""
nombre_pokemons_colonne = 10

"""
Liste de tous les types de pokemons
"""
tous_les_types = []

with open("pokemons.csv") as csvfile:
    pokedex = []
    for pokemon in csv.DictReader(csvfile):
        pokedex.append(pokemon)
        t1 = pokemon["type1"].lower()
        t2 = pokemon["type2"].lower()

        # On nettoie les pokémons qui ont 2x le même type
        if t1 == t2:
            t2 = ""
            pokemon["type2"] = ""

        if len(t1) > 0 and t1 not in tous_les_types:
            tous_les_types.append(t1)
        if len(t2) > 0 and t2 not in tous_les_types:
            tous_les_types.append(t2)
tous_les_types.sort()
tous_les_types.append('')

"""
Dictionnaire associant à chaque clé du type (type1, type2) la liste des noms de
pokemons correspondants. type2 peut être ''.
"""
combinaisons_types = {}

for i in range(len(tous_les_types) - 1):
    for j in range(i, len(tous_les_types)):
        t1 = tous_les_types[i]
        t2 = tous_les_types[j]
        combinaisons_types[(t1, t2)] = []
        combinaisons_types[(t2, t1)] = []
for p in pokedex:
    t1 = p["type1"]
    t2 = p["type2"]

    if (t1, t2) in combinaisons_types:
        combinaisons_types[(t1, t2)].append(p["name"].lower())

    if len(t2) > 0 and (t2, t1) in combinaisons_types:
        combinaisons_types[(t2, t1)].append(p["name"].lower())

"""
Nombre maximal de pokemon dans une catégorie donnée.
"""
nombre_pokemon_maxi = 0

for liste in combinaisons_types.values():
    if len(liste) > nombre_pokemon_maxi:
        nombre_pokemon_maxi = len(liste)

"""
Dictionnaire associant à chaque nom de pokemon son enregistrement.
"""
annuaire_pokemons = {}
for pokemon in pokedex:
    nom = pokemon["name"]
    annuaire_pokemons[nom.lower()] = pokemon
