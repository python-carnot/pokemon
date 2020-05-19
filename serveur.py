from flask import Flask, render_template, request
import datetime
import csv

app = Flask(__name__, static_url_path='/static')

nombre_pokemons_colonne = 10

with open("pokemons.csv") as csvfile:
  pokedex = []
  for pokemon in csv.DictReader(csvfile):
    pokedex.append(pokemon)

# On crée un dictionnaire associant à chaque nom de pokemon
# son enregistrement dans le pokedex
annuaire_pokemon = {}
for pokemon in pokedex:
  nom = pokemon["name"]
  annuaire_pokemon[nom] = pokemon

@app.route('/recherche')
def recherche():
  return """
  <!DOCTYPE html>
  <html lang="fr">
    <head>
        <meta charset="utf-8" />
        <link rel="stylesheet" type="text/css" href="/style.css" />
        <title>Rechercher un pokemons</title>
    </head>
    <body>  
      <h1>Rechercher un pokemon</h1>
    </body>
  </html>
  """

@app.route('/')
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
    <body>
      <table id="pokedex">
  """)

  for i, pokemon in enumerate(pokedex):
    if i % nombre_pokemons_colonne == 0:
      # On est au début d'une ligne
      html.append("      <tr>")
    
    nom = pokemon["name"]
    chemin_image = pokemon["image"]

    html.append("""
          <td>
            <a href="pokemons/{}">
              <img src="/static/{}" alt="{}"/>
            </a>
          </td>
    """.format(nom, chemin_image, nom))

    if i % nombre_pokemons_colonne == nombre_pokemons_colonne - 1:
      # On est à la fin d'une ligne
      html.append("      </tr>")


  html.append("""        
      </table>
    </body>
  </html>
  """)

  # On renvoie toutes les portions de html, concaténées en une unique
  # chaîne de caratères:
  return "".join(html)

@app.route("/pokemons/<nom_pokemon>")
def pokemons(nom_pokemon):
  pokemon = annuaire_pokemon[nom_pokemon]

  html = []
  
  html.append("""
  <!DOCTYPE html>
  <html lang="fr">
    <head>
        <meta charset="utf-8" />
        <link rel="stylesheet" type="text/css" href="/style.css" />
        <title>Pokemon: {}</title>
    </head>
    <body>

  """.format(pokemon["name"]))

  html.append("    <h1>{}</h1>".format(pokemon["name"]))

  html.append("""
      <div id="image">
        <img src="/static/{}" alt="{}" />
      </div>
    """.format(pokemon["image"], pokemon["name"]))

  # On liste les attributs de ce pokemon
  html.append("""    <table id="pokemon">""")

  # pokemon est un dictionnaire, où chaque clé est un nom d'attibut
  for attribut, valeur in pokemon.items():
    html.append("""
          <tr>
            <td class="attribut-pokemon">{} :</td>
            <td class="valeur-pokemon">{}</td>
          </tr>
    """.format(attribut, valeur))

  html.append("    <table>")

  html.append("""        
    </body>
  </html>
  """)

  return "".join(html)

@app.route('/style.css')
def css():
  return app.send_static_file("style.css")

app.run(debug=True)

