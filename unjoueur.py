
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
print("nombre de chiffre bien placé:" bien_places)


#code claude #understand puis changer
import random

MAX_TENTATIVES = 10
TAILLE_CODE    = 4
MIN_CHIFFRE    = 1
MAX_CHIFFRE    = 10

def generer_code_secret():
    
    code_secret = []
    for i in range(TAILLE_CODE):
        code_secret.append(random.randint(MIN_CHIFFRE, MAX_CHIFFRE))
    return code_secret

def saisir_essai(numero_tentative):
    # Demande 4 chiffres au joueur et retourne la liste EssaiJoueur
    print(f"--- Tentative numéro {numero_tentative} ---")
    essai_joueur = []
    for i in range(TAILLE_CODE):
        chiffre = int(input(f"  Position {i+1} (entre {MIN_CHIFFRE} et {MAX_CHIFFRE}) : "))
        essai_joueur.append(chiffre)
    return essai_joueur

def comparer(essai_joueur, code_secret):
    # Crée deux copies de travail pour ne pas modifier l'original
    secret_temp = list(code_secret)
    essai_temp  = list(essai_joueur)

    bien_places = 0
    mal_places  = 0

    # Étape 1 : chercher les bien placés
    for i in range(TAILLE_CODE):
        if essai_temp[i] == secret_temp[i]:
            bien_places = bien_places + 1
            secret_temp[i] = "UTILISÉ"   # marquer comme utilisé
            essai_temp[i]  = "OK"

    # Étape 2 : chercher les mal placés
    for i in range(TAILLE_CODE):
        if essai_temp[i] != "OK":            # chiffre pas encore bien placé
            if essai_temp[i] in secret_temp:  # existe ailleurs dans le secret ?
                mal_places = mal_places + 1
                secret_temp.remove(essai_temp[i])  # éviter de le compter 2 fois

    return bien_places, mal_places


def afficher_resultats(bien_places, mal_places):
    # Affiche les indicateurs après chaque essai
    if bien_places == TAILLE_CODE:
        print("BRAVO ! Vous avez trouvé le code !")
    else:
        print(f"  Bien placés  : {bien_places}")
        print(f"  Mal placés   : {mal_places}")
        if bien_places == 0 and mal_places == 0:
            print("  → TOUT EST FAUX")


def jouer():
    print("Bienvenue au Mastermind !")

    code_secret  = generer_code_secret()
    tentatives   = 1
    partie_gagnee = False

    # Boucle principale
    while tentatives <= MAX_TENTATIVES and partie_gagnee == False:

        essai_joueur          = saisir_essai(tentatives)
        bien_places, mal_places = comparer(essai_joueur, code_secret)
        afficher_resultats(bien_places, mal_places)

        if bien_places == TAILLE_CODE:
            partie_gagnee = True
        else:
            tentatives = tentatives + 1

    # Conclusion
    if partie_gagnee == False:
        print("DOMMAGE ! Vous avez perdu.")
        print(f"Le code secret était : {code_secret}")

jouer()

