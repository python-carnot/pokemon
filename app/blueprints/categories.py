from flask import Blueprint, request

import app.table

categories_blueprint = Blueprint('categories', __name__)


@categories_blueprint.route('/categories', methods=['GET'])
def affichage_par_categories():
    result = request.args
    type1 = result['type1']
    type2 = result['type2']

    html = []

    html.append("""
<!DOCTYPE html>
<html lang="fr">
    <head>
        <meta charset="utf-8" />
        <link rel="stylesheet" type="text/css" href="/style.css" />
        <title>Pokemons d'une certaine catégories</title>
    </head>
    <body>""")

    html.append("<h1>Pokemons de type {} - {}</h1>".format(type1, type2))

    app.table.ajoute_table_pokemons(html, type1, type2)

    html.append("""
    </body>
</html>""")

    return "".join(html)
