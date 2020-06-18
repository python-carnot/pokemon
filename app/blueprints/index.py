from flask import Blueprint

import app.matrice
import app.table

index_blueprint = Blueprint('index', __name__)


@index_blueprint.route('/')
def index():
    # Créer dynamiquement une chaîne de caractère peut se faire selon
    # deux méthodes:
    # - on crée des bouts de chaînes que l'on concatène à l'aide
    #   de l'opérateur +: "pascal" + " " + "grossé" donne "pascal grossé"
    #   MAIS: cela est très coûteux, une nouvelle chaîne est créée en
    #   mémoire et intégralement recopiée à chaque utilisation de +.
    # - On stocke tous les bouts de chaînes dans un tableau, que l'on
    #   concatène en une seule opération à la fin grâce à join. C'est
    #   de très loin la meilleure méthode.

    html = []

    html.append("""
<!DOCTYPE html>
<html lang="fr">
    <head>
        <meta charset="utf-8" />
        <link rel="stylesheet" type="text/css" href="/style.css" />
        <title>Tous les pokemons</title>
    </head>
    <body>""")

    formulaire_de_recherche(html)

    app.matrice.matrice_des_types(html)

    app.table.ajoute_table_pokemons(html)

    html.append("""
    </body>
</html>""")

    # On renvoie toutes les portions de html, concaténées en une unique
    # chaîne de caratères:
    return "".join(html)


def formulaire_de_recherche(html):
    html.append("""
    <div id="recherche">
      <form action="resultat" method="get">
          <label>Nom du pokemon: </label><input type="text" name="nom" />
          <input type="submit" value="Aller voir ce pokemon" />
      </form>
    </div>
  """)
