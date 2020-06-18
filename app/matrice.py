import app.constantes as cst


def calcule_couleur_dégradé(nombre, nombre_pokemon_maxi):
    valeur_couleur = 255 - int(128 * pow(nombre / nombre_pokemon_maxi, 0.33))
    valeur_couleur_hexa = hex(valeur_couleur)[2:]
    return "#{}{}{}".format(valeur_couleur_hexa, valeur_couleur_hexa, valeur_couleur_hexa)


def matrice_des_types(html):
    html.append("""
    <div id="matrice">""")

    html.append("""
        <table>""")

    html.append("""
            <tr>""")

    html.append("""
                <th></th>""")
    for t in cst.tous_les_types:
        if len(t) > 0:
            html.append("""
                <th>{}</th>""".format(t.title()))

    html.append("""
            </tr>""")

    for t1 in cst.tous_les_types:
        html.append("""
            <tr>""")
        if len(t1) > 0:
            html.append("""
                <th>{}</th>""".format(t1.title()))
        else:
            html.append("""
                <th>Empty</th>""")

        for t2 in cst.tous_les_types:
            if len(t2) > 0:
                if len(t1) > 0:
                    nombre = len(cst.combinaisons_types[(t1, t2)])
                else:
                    nombre = len(cst.combinaisons_types[(t2, "")])
                if nombre > 0:
                    couleur = calcule_couleur_dégradé(
                        nombre, cst.nombre_pokemon_maxi)
                    # url = Universal Remote Location
                    if len(t1) > 0:
                        url = "/categories?type1={}&type2={}".format(t1, t2)
                    else:
                        url = "/type/{}".format(t2)
                    html.append(
                        """
                <td class="clickable" onclick="parent.location='{}'" style="background-color: {}">{}</td>""".format(url, couleur, nombre))
                else:
                    html.append("""
                <td></td>""")

        html.append("""
            </tr>""")

    html.append("""
        </table>""")
    html.append("""
    </div>""")
