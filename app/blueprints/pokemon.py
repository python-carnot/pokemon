from flask import Blueprint

import app.constantes as cst

pokemon_blueprint = Blueprint('pokemon', __name__)


@pokemon_blueprint.route("/pokemons/<nom_pokemon>")
def pokemons(nom_pokemon):
    pokemon = cst.annuaire_pokemons[nom_pokemon.lower()]

    html = []

    html.append("""
<!DOCTYPE html>
<html lang="fr">
    <head>
        <meta charset="utf-8" />
        <link rel="stylesheet" type="text/css" href="/style.css" />
        <title>Pokemon: {}</title>
    </head>
    <body>""".format(pokemon["name"]))

    html.append("""
        <h1>
            {}
        </h1>""".format(pokemon["name"]))

    html.append("""
        <div id="image">
            <img src="/static/{}" alt="{}" />
        </div>""".format(pokemon["image"], pokemon["name"]))

    # On liste les attributs de ce pokemon
    html.append("""
        <table id="pokemon">""")

    # pokemon est un dictionnaire, où chaque clé est un nom d'attibut
    for attribut, valeur in pokemon.items():
        html.append("""
            <tr>
                <td class="attribut-pokemon">{} :</td>
                <td class="valeur-pokemon">{}</td>
            </tr>""".format(attribut, valeur))

    html.append("""
        <table>""")

    html.append("""        
    </body>
</html>""")

    return "".join(html)
