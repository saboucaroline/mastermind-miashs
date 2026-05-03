"""#on va vérifié mtn si les code secret == essaie du joueur
bien_places = 0

if essaie[0] == codesecret[0]:
    bien_places = bien_places + 1

if essaie[1] == codesecret[1]:
    bien_places = bien_places + 1

if essaie[2] == codesecret[2]:
    bien_places = bien_places + 1

if essaie[3] == codesecret[3]:
    bien_places = bien_places + 1
finalement on fera peut-etre une fonction pour que ça soit + lisible !!!
#on va voir si les résultats sont correct """

#fonctions bien placés

def calculer_bienplaces(essai, codesecret):
    compteur = 0
    for i in range (0,3):
        if essai[i] == codesecret[i]:
            compteur = compteur +1
        return compteur
    
#fonctions mal placés
"""def calculer_malplaces(essai,codesecret):
    #on va exclure les biens places 
    essaie_restant = [essai[i] for i in range (len(essaie)): essaie[i] != codesecret[i]]
    secret_restant = [essai[i] for i in range (len(essaie)): essaie[i] != codesecret[i]]

    compteur = 0

    for chiffre in range(essaie_restant):
        if chiffre == secret_restant:
            compteur =+ 1

    return compteur"""

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

#avoir une liste choisit par l'ordi
import random 

codesecret = []
for i in range(4):
    codesecret.append(random.randint(1, 10)) 
print ("voilà le code secret", codesecret) #a ne pas mettre sur l'interface, c'est juste pour vérifer pour l'instant


#le premier essaie du joueur

print ("vous allez choisir 4 chiffres entre 1 à 10, vous allez le mettre un par un")


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
        tour = tour +1
        
        
#défaite  -> sorti de la boucle car joueur n'a pas trouvé le codesecret
print("Mince..vous avez perdu, le code secret était, ", codesecret) #a mettre quand tour= tentative_max 


