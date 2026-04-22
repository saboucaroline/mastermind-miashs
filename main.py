# Projet Mastermind - L1 MIASHS
# Groupe : MIASHS2
import random 
print("Bienvenue dans le Mastermind !")
# Les fonctions seront ajoutées ici
print("Règles du jeu :  \n -Un joueur choisit son code secret de 4 couleurs parmis 8 \n -L'autre joueur doit deviner ce code en 10 essai maximum \n")

nb_pions = 4 
nb_couleurs = 8
nb_essais_max = 10

couleurs = []

def evaluer_essai(code, essai):
    bien_place = 0
    mal_place = 0 
    code_restant = []
    essai_restant = []

    for i in range (nb_pions):
        if essai[i] == code[i]:
            bien_place +=1
        else:
            code_restant.append(code[i])
            essai_restant.append[essai[i]]

    for couleur in essai_restant:
        if couleur in code_restant:
            mal_place +=1
            code_restant.remove(couleur)
    return (bien_place,mal_place)

