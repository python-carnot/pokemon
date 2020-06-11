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

  affiche_tous_les_types(html)

  ajoute_table_pokemons(html)

  html.append("""
    </body>
  </html>
  """)

  # On renvoie toutes les portions de html, concaténées en une unique
  # chaîne de caratères:
  return "".join(html)

def affiche_tous_les_types(html):
  html.append("""<div id="categories">
  """)
  html.append("""
  <table>
    <tr>
  """)

  for t in tous_les_types:
    html.append("""
      <td>
        <a href="/type/{}">{}</a>
      </td>
    """.format(t, t.title()))

  html.append("""
    </tr>
  </table>
  """)
  html.append("</div>")

def ajoute_table_pokemons(html, type1="", type2=""):
  html.append("""
      <table id="pokedex">
  """)

  type1 = type1.lower()
  type2 = type2.lower()

  if type2 == "none":
    type2 = ""

  if type1 == "":
    # On veut la liste *complète* des pokemons
    liste_pokemons = annuaire_pokemon.keys()
  else:
    # On veut tous les pokemons ayant les types indiqués
    liste_pokemons = combinaisons_types[(type1, type2)]

  i = 0
  for nom_pokemon in liste_pokemons:
    pokemon = annuaire_pokemon[nom_pokemon]
    if i % nombre_pokemons_colonne == 0:
      # On est au début d'une ligne
      html.append("      <tr>")
    
    nom = pokemon["name"]
    chemin_image = pokemon["image"]

    if pokemon["is_legendary"] == "0":
      html.append("""
            <td>
      """)
    else:
      html.append("""
            <td class="legendary">
      """)

    html.append("""
            <a href="/pokemons/{}">
              <img src="/static/{}" alt="{}"/>
            </a>
            <p>{}</p>
          </td>
    """.format(nom, chemin_image, nom, nom))

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
    <body>
  """)

  ajoute_table_pokemons(html, type1, type2)

  html.append("""
    </body>
  </html>
  """)

  return "".join(html)

@app.route("/type/<type_pokemon>")
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
      <h1>Pokemons ayant le type {}</h1>

  """.format(type_pokemon, type_pokemon))

  html.append("""
      <h2>Type {} uniquement</h2>
  """.format(type_pokemon))

  ajoute_table_pokemons(html, type_pokemon)

  for t in tous_les_types:
    if t != type_pokemon and t != "":
      html.append("""
          <h2>Type {} - {}</h2>
      """.format(type_pokemon, t))

      if len(combinaisons_types[(type_pokemon, t)]) > 0:
        ajoute_table_pokemons(html, type_pokemon, t)
      else:
        html.append("""
          <p>Aucun pokemon n'a cette combinaison de types.</p>
        """)


  html.append("""
    </body>
  </html>
  """)

  return "".join(html)


app.run(debug=True)

