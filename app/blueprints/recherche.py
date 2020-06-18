from flask import Blueprint, request

from app.blueprints.pokemon import pokemons

recherche_blueprint = Blueprint('recherche', __name__)


@recherche_blueprint.route('/resultat', methods=['GET'])
def resultat():
    result = request.args
    n = result['nom']
    return pokemons(n)
