# fichiers.py - version temporaire pour tester l'interface
# Les vraies fonctions seront faites par les autres membres du groupe

import json

def sauvegarder_partie(donnees):
    """Sauvegarde la partie dans sauvegarde.json."""
    with open("sauvegarde.json", "w") as f:
        json.dump(donnees, f)

def charger_partie():
    """Charge la partie depuis sauvegarde.json. Retourne None si pas de fichier."""
    try:
        with open("sauvegarde.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return None
