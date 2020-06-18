from flask import Flask, render_template, request
import datetime

import app.constantes as cst

pokeapp = Flask(__name__, static_url_path='/static')


def liste_des_options_de_types(html):
  for t in cst.tous_les_types:
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



@pokeapp.route('/')
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

  matrice_des_types(html)

  ajoute_table_pokemons(html)

  html.append("""
    </body>
  </html>
  """)

  # On renvoie toutes les portions de html, concaténées en une unique
  # chaîne de caratères:
  return "".join(html)

def calcule_couleur_dégradé(nombre, nombre_pokemon_maxi):
  valeur_couleur = 255 - int(128 * pow(nombre / nombre_pokemon_maxi, 0.33))
  valeur_couleur_hexa = hex(valeur_couleur)[2:]
  return "#{}{}{}".format(valeur_couleur_hexa, valeur_couleur_hexa, valeur_couleur_hexa)

def matrice_des_types(html):
  html.append("""
  <div id="matrice">
  """)

  html.append("""
    <table>
  """)

  html.append("""
      <tr>
  """)  
  
  html.append("""<th></th>""")
  for t in cst.tous_les_types:
    if len(t) > 0:
      html.append("""<th>{}</th>""".format(t.title()))

  html.append("""
      </tr>
  """)  

  for t1 in cst.tous_les_types:
    html.append("""<tr>""")
    if len(t1) > 0:
      html.append("""<th>{}</th>""".format(t1.title()))
    else:
      html.append("""<th>Empty</th>""")

    for t2 in cst.tous_les_types:
      if len(t2) > 0:
        if len(t1) > 0:
          nombre = len(cst.combinaisons_types[(t1, t2)])
        else:
          nombre = len(cst.combinaisons_types[(t2, "")])
        if nombre > 0:
          couleur = calcule_couleur_dégradé(nombre, cst.nombre_pokemon_maxi)
          # url = Universal Remote Location
          if len(t1) > 0:
            url = "/categories?type1={}&type2={}".format(t1, t2)
          else:
            url = "/type/{}".format(t2)
          html.append("""<td class="clickable" onclick="parent.location='{}'" style="background-color: {}">{}</td>""".format(url, couleur, nombre))
        else:
          html.append("""<td></td>""")

    html.append("""</tr>""")

  html.append("""
    </table>""")


  html.append("""
  </div>""")

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
    liste_pokemons = cst.annuaire_pokemons.keys()
  else:
    # On veut tous les pokemons ayant les types indiqués
    liste_pokemons = cst.combinaisons_types[(type1, type2)]

  i = 0
  for nom_pokemon in liste_pokemons:
    pokemon = cst.annuaire_pokemons[nom_pokemon]
    if i % cst.nombre_pokemons_colonne == 0:
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

    if i % cst.nombre_pokemons_colonne == cst.nombre_pokemons_colonne - 1:
      # On est à la fin d'une ligne
      html.append("      </tr>")
    
    i = i + 1


  html.append("""        
      </table>
  """)  

@pokeapp.route("/pokemons/<nom_pokemon>")
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

@pokeapp.route('/style.css')
def css():
  return pokeapp.send_static_file("style.css")

@pokeapp.route('/font.ttf')
def font():
  return pokeapp.send_static_file("digital-7-mono.ttf")

@pokeapp.route('/resultat', methods=['GET'])
def resultat():
  result = request.args
  n = result['nom']
  return pokemons(n)

@pokeapp.route('/categories', methods=['GET'])
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

  html.append("<h1>Pokemons de type {} - {}</h1>".format(type1, type2))

  ajoute_table_pokemons(html, type1, type2)

  html.append("""
    </body>
  </html>
  """)

  return "".join(html)

@pokeapp.route("/type/<type_pokemon>")
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

  for t in cst.tous_les_types:
    if t != type_pokemon and t != "":
      html.append("""
          <h2>Type {} - {}</h2>
      """.format(type_pokemon, t))

      if len(cst.combinaisons_types[(type_pokemon, t)]) > 0:
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



