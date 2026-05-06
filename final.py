import tkinter as tk
from tkinter import messagebox
import random
#esma
NB_PIONS = 4
NB_COULEURS = 6
NB_ESSAIS = 10

COULEURS = ["red", "blue", "green", "orange", "yellow", "purple"]
NOMS = ["Rouge", "Bleu", "Vert", "Orange", "Jaune", "Violet"]
#sadati
secret      = []
historique  = []
courant     = []
fini        = False
mode        = ""      

label_compteur  = None
canvas_grille   = None
canvas_saisie   = None
cercles_grille  = []
cercles_saisie  = []
labels_resultat = []
#caroline
def code_aleatoire():
    code = []
    for i in range(NB_PIONS):
        code.append(random.randint(0, NB_COULEURS - 1))
    return code
#esma
def evaluer(secret, essai):
    bien = 0
    mal = 0
    secret_reste = []
    essai_reste  = []

    for i in range(NB_PIONS):
        if essai[i] == secret[i]:
            bien += 1
        else:
            secret_reste.append(secret[i])
            essai_reste.append(essai[i])

    for couleur in essai_reste:
        if couleur in secret_reste:
            mal += 1
            secret_reste.remove(couleur)

    return bien, mal

def vider_fenetre():
    for widget in racine.winfo_children():
        widget.destroy()
#sadati
def vue_menu():
    vider_fenetre()
    racine.geometry("350x300")

    label_titre = tk.Label(racine, text="MASTERMIND", font=("helvetica", "24", "bold"), fg="red")
    label_titre.grid(row=0, column=0, columnspan=2, pady=20)

    label_sous = tk.Label(racine, text="Choisissez un mode de jeu", font=("helvetica", "11"))
    label_sous.grid(row=1, column=0, columnspan=2, pady=5)

    btn_1joueur = tk.Button(racine, text="1 Joueur", font=("helvetica", "13"), bg="red", fg="white", width=18, command=demarrer_1joueur)
    btn_1joueur.grid(row=2, column=0, columnspan=2, pady=8)

    btn_2joueurs = tk.Button(racine, text="2 Joueurs", font=("helvetica", "13"), bg="blue", fg="white", width=18, command=vue_choix_secret)
    btn_2joueurs.grid(row=3, column=0, columnspan=2, pady=8)

    frame_deco = tk.Frame(racine)
    frame_deco.grid(row=4, column=0, columnspan=2, pady=15)
    for i in range(NB_COULEURS):
        tk.Label(frame_deco, bg=COULEURS[i], width=3, height=1, relief="ridge").grid(row=0, column=i, padx=2)
#sylvana
def vue_choix_secret():
    global mode
    mode = "2joueurs"
    vider_fenetre()
    racine.geometry("420x280")

    tk.Label(racine, text="Joueur 1 : choisissez le code secret", font=("helvetica", "13", "bold"),fg="blue").grid(row=0, column=0, columnspan=NB_PIONS + 1, pady=15, padx=10)

    tk.Label(racine, text="Cliquez sur les couleurs pour former le code :", font=("helvetica", "10")).grid(row=1, column=0, columnspan=NB_PIONS + 1, pady=3)

    canvas_apercu = tk.Canvas(racine, width=NB_PIONS * 40 + 20,  height=50, bg="lightyellow", relief="ridge", bd=2)
    canvas_apercu.grid(row=2, column=0, columnspan=NB_PIONS, padx=10, pady=10)

    cercles_apercu = []
    for j in range(NB_PIONS):
        x = j * 40 + 30
        y = 25
        id_c = canvas_apercu.create_oval(x - 15, y - 15, x + 15, y + 15, fill="lightgray", outline="black", width=2)
        cercles_apercu.append(id_c)

    code_tmp = []

    btn_valider_secret = tk.Button(racine, text="Valider le code", font=("helvetica", "11", "bold"), bg="green", fg="white", state=tk.DISABLED, command=lambda: valider_secret(code_tmp))
    btn_valider_secret.grid(row=4, column=0, columnspan=NB_COULEURS, pady=8)

    def ajouter_couleur_secret(idx):
        if len(code_tmp) < NB_PIONS:
            code_tmp.append(idx)
            pos = len(code_tmp) - 1
            canvas_apercu.itemconfigure(cercles_apercu[pos], fill=COULEURS[idx])
            if len(code_tmp) == NB_PIONS:
                btn_valider_secret.config(state=tk.NORMAL)

    def effacer_couleur_secret():
        if len(code_tmp) > 0:
            code_tmp.pop()
            pos = len(code_tmp)
            canvas_apercu.itemconfigure(cercles_apercu[pos], fill="lightgray")
            btn_valider_secret.config(state=tk.DISABLED)

    frame_palette = tk.Frame(racine)
    frame_palette.grid(row=3, column=0, columnspan=NB_COULEURS, pady=5)

    for i in range(NB_COULEURS):
        tk.Button(frame_palette, bg=COULEURS[i], width=4, height=2, relief="raised", cursor="hand2", command=lambda idx=i: ajouter_couleur_secret(idx) ).grid(row=0, column=i, padx=3)

    tk.Button(racine, text="Effacer", font=("helvetica", "10"), command=effacer_couleur_secret).grid(row=4, column=NB_COULEURS, pady=8, padx=5)

    tk.Button(racine, text="Menu", font=("helvetica", "10"), command=vue_menu).grid(row=5, column=0, columnspan=NB_COULEURS + 1, pady=5)
#esma
def valider_secret(code_tmp):
    global secret
    secret = code_tmp.copy()
    messagebox.showinfo("Code enregistre", "Le code est cache !\nPassez la main au Joueur 2.")
    vue_plateau()
#caroline
def demarrer_1joueur():
    global secret, mode
    mode   = "1joueur"
    secret = code_aleatoire()
    vue_plateau()
#sadati et sylvana
def vue_plateau():
    global historique, courant, fini
    global canvas_grille, canvas_saisie
    global cercles_grille, cercles_saisie
    global labels_resultat, label_compteur

    historique = []
    courant    = []
    fini       = False

    vider_fenetre()
    racine.geometry("500x620")

    RAYON      = 15
    ESPACEMENT = 40

    if mode == "1joueur":
        texte_titre = "MASTERMIND - 1 Joueur"
    else:
        texte_titre = "MASTERMIND - 2 Joueurs"

    tk.Label(racine, text=texte_titre,  font=("helvetica", "16", "bold"),  fg="red").grid(row=0, column=0, columnspan=3, pady=8)

    label_compteur = tk.Label(racine, text="Essai 1 / " + str(NB_ESSAIS), font=("helvetica", "11"))
    label_compteur.grid(row=1, column=0, columnspan=3, pady=3)

    canvas_grille = tk.Canvas(racine, width=NB_PIONS * ESPACEMENT + 20, height=NB_ESSAIS * ESPACEMENT + 10, bg="white", relief="ridge", bd=2)
    canvas_grille.grid(row=2, column=0, padx=10, pady=5)

    cercles_grille = []
    for i in range(NB_ESSAIS):
        ligne = []
        for j in range(NB_PIONS):
            x = j * ESPACEMENT + ESPACEMENT // 2 + 10
            y = i * ESPACEMENT + ESPACEMENT // 2 + 5
            id_cercle = canvas_grille.create_oval( x - RAYON, y - RAYON, x + RAYON, y + RAYON, fill="lightgray", outline="black", width=1 )
            ligne.append(id_cercle)
        cercles_grille.append(ligne)

    frame_resultats = tk.Frame(racine)
    frame_resultats.grid(row=2, column=1, padx=5, pady=5, sticky="n")

    labels_resultat = []
    for i in range(NB_ESSAIS):
        lbl = tk.Label(frame_resultats, text="  -  ", font=("helvetica", "10"),  width=6)
        lbl.grid(row=i, column=0, pady=3)
        labels_resultat.append(lbl)

    frame_palette = tk.Frame(racine, relief="ridge", bd=2)
    frame_palette.grid(row=2, column=2, padx=10, pady=5, sticky="n")

    tk.Label(frame_palette, text="Couleurs", font=("helvetica", "10", "bold")).grid(row=0, column=0, columnspan=2, pady=5)

    for i in range(NB_COULEURS):
        tk.Button(frame_palette, bg=COULEURS[i], width=4, height=2, relief="raised", cursor="hand2", command=lambda idx=i: cliquer_couleur(idx) ).grid(row=i // 2 + 1, column=i % 2, padx=4, pady=3)

    tk.Label(racine, text="Votre essai :", font=("helvetica", "11")).grid(row=3, column=0, pady=(10, 2))

    canvas_saisie = tk.Canvas(racine,  width=NB_PIONS * ESPACEMENT + 20, height=ESPACEMENT + 10, bg="lightyellow", relief="ridge", bd=2)
    canvas_saisie.grid(row=4, column=0, padx=10, pady=5)

    cercles_saisie = []
    for j in range(NB_PIONS):
        x = j * ESPACEMENT + ESPACEMENT // 2 + 10
        y = ESPACEMENT // 2 + 5
        id_cercle = canvas_saisie.create_oval(x - RAYON, y - RAYON, x + RAYON, y + RAYON, fill="lightgray", outline="black", width=2)
        cercles_saisie.append(id_cercle)

    frame_boutons = tk.Frame(racine)
    frame_boutons.grid(row=5, column=0, columnspan=3, pady=8)

    tk.Button(frame_boutons, text="Valider", font=("helvetica", "11", "bold"), bg="red", fg="white", command=cliquer_valider).grid(row=0, column=0, padx=5)

    tk.Button(frame_boutons, text="Effacer", font=("helvetica", "11"), command=cliquer_effacer).grid(row=0, column=1, padx=5)

    tk.Button(frame_boutons, text="Annuler essai", font=("helvetica", "11"), command=cliquer_annuler).grid(row=0, column=2, padx=5)

    tk.Button(frame_boutons, text="Rejouer", font=("helvetica", "11"), command=vue_plateau).grid(row=0, column=3, padx=5)

    tk.Button(frame_boutons, text="Menu", font=("helvetica", "11"), command=vue_menu).grid(row=0, column=4, padx=5)
#caroline
def cliquer_couleur(idx):
    global courant
    if fini:
        return
    if len(courant) < NB_PIONS:
        courant.append(idx)
        pos = len(courant) - 1
        canvas_saisie.itemconfigure(cercles_saisie[pos], fill=COULEURS[idx])
#esma
def cliquer_effacer():
    global courant
    if len(courant) > 0:
        courant.pop()
        pos = len(courant)
        canvas_saisie.itemconfigure(cercles_saisie[pos], fill="lightgray")
#esma
def cliquer_valider():
    global courant, fini

    if fini:
        return

    if len(courant) < NB_PIONS:
        messagebox.showwarning("Attention", "Il faut choisir 4 couleurs !")
        return

    bp, mp = evaluer(secret, courant)
    ligne  = len(historique)
    historique.append((courant.copy(), bp, mp))

    for j in range(NB_PIONS):
        canvas_grille.itemconfigure(cercles_grille[ligne][j], fill=COULEURS[courant[j]])

    labels_resultat[ligne].config(text=str(bp) + "B  " + str(mp) + "M")

    courant = []
    for j in range(NB_PIONS):
        canvas_saisie.itemconfigure(cercles_saisie[j], fill="lightgray")

    label_compteur.config(text="Essai " + str(len(historique) + 1) + " / " + str(NB_ESSAIS))

    if bp == NB_PIONS:
        fini = True
        messagebox.showinfo("Gagne !", "Bravo ! Code trouve en " + str(len(historique)) + " essai(s) !")

    elif len(historique) >= NB_ESSAIS:
        fini = True
        noms = ""
        for c in secret:
            noms = noms + NOMS[c] + " "
        messagebox.showinfo("Perdu !", "Le code etait : " + noms)
#caroline
def cliquer_annuler():
    global historique, courant, fini

    if len(historique) == 0:
        messagebox.showinfo("Info", "Aucun essai a annuler !")
        return

    historique.pop()
    ligne = len(historique)

    for j in range(NB_PIONS):
        canvas_grille.itemconfigure(cercles_grille[ligne][j], fill="lightgray")

    labels_resultat[ligne].config(text="  -  ")

    courant = []
    for j in range(NB_PIONS):
        canvas_saisie.itemconfigure(cercles_saisie[j], fill="lightgray")

    label_compteur.config(text="Essai " + str(len(historique) + 1) + " / " + str(NB_ESSAIS))
    fini = False

racine = tk.Tk()
racine.title("Mastermind")
vue_menu()
racine.mainloop()

# Ce travail a été réalisé par l'ensemble des membres du groupe, nous avons travaillé chacune de notre coté. Ce fichier est le fichier final où l'on a regrouper les efforts de chacunes, ce fichier a été réalisé sur un seul ordinateur car finalisé et perfectionner quand nous nous sommes réunies.
# sources : cours, document officiel python, reference tkinter en francais (joins dans le cours)