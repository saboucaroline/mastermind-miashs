# logique.py - version temporaire pour tester l'interface
# Les vraies fonctions seront faites par les autres membres du groupe

import random

nb_pions    = 4
nb_couleurs = 8

def evaluer_essai(code, essai):
    """Compare un essai au code secret, retourne (bien_places, mal_places)."""
    bien_place    = 0
    mal_place     = 0
    code_restant  = []
    essai_restant = []

    for i in range(len(code)):
        if essai[i] == code[i]:
            bien_place += 1
        else:
            code_restant.append(code[i])
            essai_restant.append(essai[i])

    for couleur in essai_restant:
        if couleur in code_restant:
            mal_place += 1
            code_restant.remove(couleur)

    return (bien_place, mal_place)


def generer_code_aleatoire():
    """Génère un code secret aléatoire."""
    return [random.randint(0, nb_couleurs - 1) for _ in range(nb_pions)]


def trouver_suggestion(essais, n_pions, n_couleurs):
    """Retourne un code compatible avec les essais déjà joués."""
    def tous_les_codes(n, c):
        if n == 0:
            return [[]]
        sous = tous_les_codes(n - 1, c)
        result = []
        for couleur in range(c):
            for s in sous:
                result.append([couleur] + s)
        return result

    for candidat in tous_les_codes(n_pions, n_couleurs):
        compatible = True
        for (e, bp, mp) in essais:
            b, m = evaluer_essai(candidat, e)
            if b != bp or m != mp:
                compatible = False
                break
        if compatible:
            return candidat
    return None
