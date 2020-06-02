from flask import Flask, render_template, request
import datetime
import csv

app = Flask(__name__, static_url_path='/static')

nombre_pokemons_colonne = 10

tous_les_types = []

with open("pokemons.csv") as csvfile:
  pokedex = []
  for pokemon in csv.DictReader(csvfile):
    pokedex.append(pokemon)
    t1 = pokemon["type1"].lower()
    t2 = pokemon["type2"].lower()
    if len(t1) > 0 and t1 not in tous_les_types:
      tous_les_types.append(t1)
    if len(t2) > 0 and t2 not in tous_les_types:
      tous_les_types.append(t2)

# On crée un dictionnaire associant à chaque nom de pokemon
# son enregistrement dans le pokedex
annuaire_pokemon = {}
for pokemon in pokedex:
  nom = pokemon["name"]
  annuaire_pokemon[nom.lower()] = pokemon

def liste_des_options_de_types(html):
  for t in tous_les_types:
    html.append('<option value="{}">{}</option>'.format(t, t.title()))

def formulaire_de_recherche(html):
  html.append("""
    <div id="recherche">
      <form action="resultat" method="get">
          <label>Nom du pokemon: </label><input type="text" name="nom" />
          <input type="submit" value="Aller voir ce pokemon" />
      </form>
      <form action="categories" method="get">
          <label>Type 1: </label>
          <select id="type1" name="type1">
  """)

  liste_des_options_de_types(html)

  html.append("""
          </select>
          <label>Type 2: </label>
          <select id="type2" name="type2">
            <option value="none">No second type</option>
  """)
  

  liste_des_options_de_types(html)

  html.append("""
          </select>
          <input type="submit" value="Chercher tous les pokemons de ce type" />
      </form>
    </div>
  """)



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
  """)

  formulaire_de_recherche(html)

  ajoute_table_pokemons(html)

  html.append("""
    </body>
  </html>
  """)

  # On renvoie toutes les portions de html, concaténées en une unique
  # chaîne de caratères:
  return "".join(html)

def ajoute_table_pokemons(html, type1="", type2=""):
  html.append("""
      <table id="pokedex">
  """)

  type1 = type1.lower()
  type2 = type2.lower()

  if type2 == "none":
    type2 = ""

  i = 0
  for pokemon in pokedex:
    if ((type1 == "" and type2 == "") or 
        (type1 == pokemon["type1"].lower() and type2 == pokemon["type2"].lower()) or
        (type1 == pokemon["type2"].lower() and type2 == pokemon["type1"].lower())):
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
      
      i = i + 1


  html.append("""        
      </table>
  """)  

@app.route("/pokemons/<nom_pokemon>")
def pokemons(nom_pokemon):
  pokemon = annuaire_pokemon[nom_pokemon.lower()]

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

@app.route('/resultat', methods=['GET'])
def resultat():
  result = request.args
  n = result['nom']
  return pokemons(n)

@app.route('/categories', methods=['GET'])
def categories():
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
    <body>
  """)

  ajoute_table_pokemons(html, type1, type2)

  html.append("""
    </body>
  </html>
  """)

  return "".join(html)


app.run(debug=True)

