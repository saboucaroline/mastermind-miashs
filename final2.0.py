import tkinter as tk
from tkinter import messagebox

nb_pions = 4 
nb_couleurs = 8
nb_chiffre = 8
nb_essais_max = 10

couleurs = [
    "#E74C3C",
    "#3498DB",  
    "#0C8840",  
    "#F39C12",  
    "#9B59B6",  
    "#36EBC6",
    "#EAC737",  
    "#5F3006",
]

noms = ["Rouge", "Bleu", "Vert", "Orange", "Violet", "Turquoise", "Jaune", "Marron"]

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

#copier coller de unjoueur

#fonctions bien placés

def calculer_bienplaces(essai, codesecret):
    compteur = 0
    for i in range (0,3):
        if essai[i] == codesecret[i]:
            compteur = compteur +1
        return compteur
    

 #code claude ia! correction

def calculer_malplaces(essai, codesecret):
    # Étape 1 : exclure les bien placés des deux listes
    essai_restant  = [essai[i]      for i in range(len(essai)) if essai[i] != codesecret[i]]
    secret_restant = [codesecret[i] for i in range(len(essai)) if essai[i] != codesecret[i]]
    #                 ^^^^^^^^^^^ attention ici c'était codesecret, pas essai !

    # Étape 2 : compter les mal placés
    compteur = 0 
    for chiffre in essai_restant:
        if chiffre in secret_restant:
            compteur += 1
            secret_restant.remove(chiffre)  # important : retirer pour ne pas compter deux fois

    return compteur
#fin code claude ia

#on commence le jeu 
tentative_max = 10
tour = 1

import random 

codesecret = []
for i in range(4):
    codesecret.append(random.randint(1, 10)) 

print ("voilà le code secret", codesecret) #a ne pas mettre sur l'interface, c'est juste pour vérifer pour l'instant


while tour != tentative_max :
    print("essai n°", tour, "sur",tentative_max)
    #le joueur entre sa combinaison ; soit askplayer
    essaie = []
    for i in range (4):
        askplayer = int(input("choississez un chiffre entre 1 à 10 "))
        essaie.append(askplayer)

    #on passe à la vérification de la liste du joueur
    bien_places = calculer_bienplaces(essaie, codesecret)
    mal_places = calculer_malplaces(essaie, codesecret)

    print("nombre de chiffre bien placés dans la liste! =", bien_places)
    print("et le nombre de chiffre mal placés.. =", mal_places)

    #le joueur a réussi à faire 4 bien placés) 
    if bien_places == 4:
        print("Félicitation! vous avez réussi avec ",tour,"tour(s)")
        #end 
    else :
        tour = tour + 1
        
#défaite  -> sorti de la boucle car joueur n'a pas trouvé le codesecret
print("Mince..vous avez perdu, le code secret était, ", codesecret) 