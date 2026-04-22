import random 
COULEURS = ["V","B","J","O","M","R"]
TAILLE_COMBINAISON = 4
NBS_ESSAIS = 10 
def generer_combinaison_secrete():
    return random.choices(COULEURS,TAILLE_COMBINAISON)
def obtrnir_tentative_joueur():
    while True:
        tantative=input()