
tentative_max = 10
tour = 1

#avoir une liste choisit par l'ordi
import random 

codesecret = []
for i in range(4):
    codesecret.append(random.randint(1, 10)) 
print ("voilà le code secret", codesecret) #a ne pas mettre sur l'interface évidemment, c'est juste pour vérifer pour l'instant


#le premier essaie du joueur
essaie = []
print ("vous allez choisir 4 chiffres entre 1 à 10, vous allez le mettre un par un")

for i in range(4):
    reponse = int(input("choisissez un chiffre"))
    essaie.append(reponse)


#on va vérifié mtn si les code secret == essaie du joueur
bien_places = 0

if essaie[0] == codesecret[0]:
    bien_places = bien_places + 1

if essaie[1] == codesecret[1]:
    bien_places = bien_places + 1

if essaie[2] == codesecret[2]:
    bien_places = bien_places + 1

if essaie[3] == codesecret[3]:
    bien_places = bien_places + 1

#on va voir si les résultats sont correct 

print("nombre de chiffre bien placé:" ,bien_places)
