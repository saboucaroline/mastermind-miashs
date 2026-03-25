print("hello")

import random 

secret = []
for i in range(4):
    secret.append(random.randint(1, 9)) # Chiffres de 1 à 9


essais_max = 10
tour = 1
gagne = False

while tour <= essais_max and not gagne:
    print(f"Tour {tour}")
    # Ici on demandera l'input du joueur
    # Ici on compare
    tour += 1