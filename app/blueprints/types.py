from flask import Blueprint

import app.table
import app.constantes as cst

types_blueprint = Blueprint('types', __name__)


@types_blueprint.route("/type/<type_pokemon>")
def pokemons_par_type(type_pokemon):
    html = []

    html.append("""
<!DOCTYPE html>
<html lang="fr">
    <head>
        <meta charset="utf-8" />
        <link rel="stylesheet" type="text/css" href="/style.css" />
        <title>Pokemons ayant le type {}</title>
    </head>
    <body>
        <h1>
            Pokemons ayant le type {}
        </h1>""".format(type_pokemon, type_pokemon))

    html.append("""
        <h2>
            Type {} uniquement
        </h2>""".format(type_pokemon))

    app.table.ajoute_table_pokemons(html, type_pokemon)

    for t in cst.tous_les_types:
        if t != type_pokemon and t != "":
            html.append("""
        <h2>
            Type {} - {}
        </h2>""".format(type_pokemon, t))

            if len(cst.combinaisons_types[(type_pokemon, t)]) > 0:
                app.table.ajoute_table_pokemons(html, type_pokemon, t)
            else:
                html.append("""
        <p>Aucun pokemon n'a cette combinaison de types.</p>""")
    html.append("""
    </body>
</html>""")

    return "".join(html)
