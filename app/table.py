import app.constantes as cst


def ajoute_table_pokemons(html, type1="", type2=""):
    html.append("""
    <table id="pokedex">""")

    type1 = type1.lower()
    type2 = type2.lower()

    if type2 == "none":
        type2 = ""

    if type1 == "":
        # On veut la liste *complète* des pokemons
        liste_pokemons = cst.annuaire_pokemons.keys()
    else:
        # On veut tous les pokemons ayant les types indiqués
        liste_pokemons = cst.combinaisons_types[(type1, type2)]

    i = 0
    for nom_pokemon in liste_pokemons:
        pokemon = cst.annuaire_pokemons[nom_pokemon]
        if i % cst.nombre_pokemons_colonne == 0:
            # On est au début d'une ligne
            html.append("""
        <tr>""")

        nom = pokemon["name"]
        chemin_image = pokemon["image"]

        if pokemon["is_legendary"] == "0":
            html.append("""
            <td>""")
        else:
            html.append("""
            <td class="legendary">""")

        html.append("""
                <a href="/pokemons/{}">
                    <img src="/static/{}" alt="{}"/>
                </a>
                <p>{}</p>
            </td>""".format(nom, chemin_image, nom, nom))

        if i % cst.nombre_pokemons_colonne == cst.nombre_pokemons_colonne - 1:
            # On est à la fin d'une ligne
            html.append("""
        </tr>""")

        i = i + 1

    html.append("""        
    </table>""")
