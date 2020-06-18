from flask import Flask, render_template, request

import app.matrice
import app.table
import app.constantes as cst

from app.blueprints import *

pokeapp = Flask(__name__, static_url_path='/static')
pokeapp.register_blueprint(index_blueprint)
pokeapp.register_blueprint(categories_blueprint)
pokeapp.register_blueprint(pokemon_blueprint)
pokeapp.register_blueprint(recherche_blueprint)
pokeapp.register_blueprint(types_blueprint)


@pokeapp.route('/style.css')
def css():
    return pokeapp.send_static_file("style.css")


@pokeapp.route('/font.ttf')
def font():
    return pokeapp.send_static_file("digital-7-mono.ttf")
