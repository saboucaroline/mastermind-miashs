# Projet Mastermind - L1 MIASHS
# Groupe : MIASHS2
# Fichier : interface.py
# Rôle : interface graphique Tkinter uniquement
#
# Ce fichier appelle des fonctions définies par les autres membres du groupe :
#   - evaluer_essai(code, essai)       -> (bien_places, mal_places)
#   - generer_code_aleatoire()         -> liste d'indices de couleur
#   - sauvegarder_partie(donnees)      -> écrit dans un fichier
#   - charger_partie()                 -> retourne les données ou None

import tkinter as tk
from tkinter import messagebox

# On importe la logique faite par les autres membres du groupe
from logique import evaluer_essai, generer_code_aleatoire
from fichiers import sauvegarder_partie, charger_partie

# ─────────────────────────────────────────
# CONSTANTES VISUELLES
# ─────────────────────────────────────────

COULEURS = [
    "#E74C3C",  # Rouge
    "#3498DB",  # Bleu
    "#0C8840",  # Vert
    "#F39C12",  # Orange
    "#9B59B6",  # Violet
    "#36EBC6",  # Turquoise
    "#EAC737",  # Jaune
    "#5F3006",  # Marron
]

NOMS = ["Rouge", "Bleu", "Vert", "Orange", "Violet", "Turquoise", "Jaune", "Marron"]

BG     = "#0d0d1a"
BG2    = "#16213e"
BG3    = "#1e1e3a"
ACCENT = "#e94560"
TEXTE  = "#ffffff"
TEXTE2 = "#8888aa"

# ─────────────────────────────────────────
# ÉTAT GLOBAL DE L'INTERFACE
# ─────────────────────────────────────────

etat = {
    "fen"            : None,
    "mode"           : None,     # "1joueur" ou "2joueurs"
    "secret"         : [],
    "essais"         : [],       # [(essai, bp, mp), ...]
    "essai_courant"  : [],
    "partie_finie"   : False,
    # widgets mis à jour pendant la partie
    "labels_grille"  : [],
    "labels_feedback": [],
    "label_essai_num": None,
    "btn_valider"    : None,
    "labels_saisie"  : [],
    # paramètres modifiables (extension)
    "param_pions"    : 4,
    "param_couleurs" : 8,
    "param_essais"   : 10,
}

# ─────────────────────────────────────────
# UTILITAIRE
# ─────────────────────────────────────────

def vider_fenetre():
    """Supprime tous les widgets de la fenêtre."""
    for widget in etat["fen"].winfo_children():
        widget.destroy()

# ─────────────────────────────────────────
# VUE : MENU PRINCIPAL
# ─────────────────────────────────────────

def vue_menu():
    """Affiche le menu principal avec les différents modes."""
    vider_fenetre()
    etat["fen"].geometry("380x400")
    etat["fen"].configure(bg=BG)

    tk.Label(etat["fen"], text="MASTERMIND",
             font=("Courier New", 26, "bold"),
             bg=BG, fg=ACCENT).pack(pady=(40, 5))

    tk.Label(etat["fen"], text="L1 MIASHS — Groupe MIASHS2",
             font=("Courier New", 9),
             bg=BG, fg=TEXTE2).pack(pady=(0, 30))

    boutons = [
        ("1 Joueur",       lambda: demarrer_partie("1joueur")),
        ("2 Joueurs",      vue_choix_secret),
        ("Paramètres",     vue_parametres),
        ("Charger partie", action_charger),
    ]

    for texte, commande in boutons:
        tk.Button(etat["fen"], text=texte,
                  font=("Courier New", 11),
                  bg=BG2, fg=TEXTE,
                  relief="flat", cursor="hand2",
                  width=20,
                  command=commande).pack(pady=5)

# ─────────────────────────────────────────
# VUE : PARAMÈTRES
# ─────────────────────────────────────────

def vue_parametres():
    """Permet de modifier les paramètres du jeu (extension)."""
    vider_fenetre()
    etat["fen"].geometry("380x300")
    etat["fen"].configure(bg=BG)

    tk.Label(etat["fen"], text="Paramètres",
             font=("Courier New", 16, "bold"),
             bg=BG, fg=ACCENT).pack(pady=(20, 15))

    frame = tk.Frame(etat["fen"], bg=BG)
    frame.pack()

    # (texte affiché, clé dans etat, min, max)
    params = [
        ("Nombre de pions",    "param_pions",    2, 6),
        ("Nombre de couleurs", "param_couleurs", 2, 8),
        ("Essais maximum",     "param_essais",   3, 20),
    ]

    spinboxes = {}
    for (label, cle, mini, maxi) in params:
        ligne = tk.Frame(frame, bg=BG)
        ligne.pack(pady=6)
        tk.Label(ligne, text=label,
                 font=("Courier New", 10),
                 bg=BG, fg=TEXTE,
                 width=22, anchor="w").pack(side=tk.LEFT)
        sb = tk.Spinbox(ligne, from_=mini, to=maxi,
                        width=4, font=("Courier New", 10))
        sb.delete(0, "end")
        sb.insert(0, str(etat[cle]))
        sb.pack(side=tk.LEFT)
        spinboxes[cle] = sb

    def appliquer():
        etat["param_pions"]    = int(spinboxes["param_pions"].get())
        etat["param_couleurs"] = int(spinboxes["param_couleurs"].get())
        etat["param_essais"]   = int(spinboxes["param_essais"].get())
        messagebox.showinfo("Paramètres", "Paramètres enregistrés !")
        vue_menu()

    tk.Button(etat["fen"], text="Appliquer",
              font=("Courier New", 10, "bold"),
              bg=ACCENT, fg=TEXTE,
              relief="flat", cursor="hand2",
              command=appliquer).pack(pady=12)

    tk.Button(etat["fen"], text="Retour",
              font=("Courier New", 10),
              bg=BG2, fg=TEXTE,
              relief="flat", cursor="hand2",
              command=vue_menu).pack()

# ─────────────────────────────────────────
# VUE : CHOIX DU CODE SECRET (2 joueurs)
# ─────────────────────────────────────────

def vue_choix_secret():
    """Le joueur 1 choisit le code secret en cliquant sur les couleurs."""
    vider_fenetre()
    etat["fen"].geometry("500x280")
    etat["fen"].configure(bg=BG)

    n_p = etat["param_pions"]
    n_c = etat["param_couleurs"]
    code_tmp = []   # code en cours de saisie, local à cette vue

    tk.Label(etat["fen"],
             text="Joueur 1 : choisissez le code secret",
             font=("Courier New", 13, "bold"),
             bg=BG, fg=ACCENT).pack(pady=(20, 5))

    tk.Label(etat["fen"],
             text="Cliquez sur les couleurs pour former le code :",
             font=("Courier New", 10),
             bg=BG, fg=TEXTE2).pack()

    # Aperçu des pions choisis
    frame_ap = tk.Frame(etat["fen"], bg=BG)
    frame_ap.pack(pady=12)
    apercu = []
    for _ in range(n_p):
        lbl = tk.Label(frame_ap, bg=BG3, width=5, height=2,
                       relief="ridge", bd=2)
        lbl.pack(side=tk.LEFT, padx=6)
        apercu.append(lbl)

    btn_valider = tk.Button(etat["fen"], text="Valider le code",
                            font=("Courier New", 10, "bold"),
                            bg=ACCENT, fg=TEXTE,
                            relief="flat", cursor="hand2",
                            state=tk.DISABLED)

    def ajouter_couleur(idx):
        if len(code_tmp) < n_p:
            code_tmp.append(idx)
            apercu[len(code_tmp) - 1].configure(bg=COULEURS[idx])
            if len(code_tmp) == n_p:
                btn_valider.configure(state=tk.NORMAL)

    def effacer():
        if code_tmp:
            code_tmp.pop()
            apercu[len(code_tmp)].configure(bg=BG3)
            btn_valider.configure(state=tk.DISABLED)

    def valider():
        etat["secret"] = code_tmp.copy()
        messagebox.showinfo("Code enregistré",
                            "Le code secret est masqué.\nPassez la main au Joueur 2 !")
        demarrer_partie("2joueurs")

    # Palette de couleurs
    frame_pal = tk.Frame(etat["fen"], bg=BG)
    frame_pal.pack(pady=5)
    for i in range(n_c):
        tk.Button(frame_pal, bg=COULEURS[i], width=4, height=2,
                  relief="flat", cursor="hand2",
                  command=lambda idx=i: ajouter_couleur(idx)
                  ).pack(side=tk.LEFT, padx=3)

    frame_btn = tk.Frame(etat["fen"], bg=BG)
    frame_btn.pack(pady=8)

    tk.Button(frame_btn, text="Effacer",
              font=("Courier New", 10), bg=BG2, fg=TEXTE,
              relief="flat", cursor="hand2",
              command=effacer).pack(side=tk.LEFT, padx=8)

    btn_valider["command"] = valider
    btn_valider.pack(side=tk.LEFT, padx=8)

    tk.Button(frame_btn, text="Menu",
              font=("Courier New", 10), bg=BG, fg=TEXTE2,
              relief="flat", cursor="hand2",
              command=vue_menu).pack(side=tk.LEFT, padx=8)

# ─────────────────────────────────────────
# DÉMARRAGE D'UNE PARTIE
# ─────────────────────────────────────────

def demarrer_partie(mode):
    """Initialise l'état de la partie et affiche le plateau."""
    etat["mode"]          = mode
    etat["essais"]        = []
    etat["essai_courant"] = []
    etat["partie_finie"]  = False

    if mode == "1joueur":
        # generer_code_aleatoire() est fournie par logique.py
        etat["secret"] = generer_code_aleatoire()
    # En mode 2joueurs, etat["secret"] est déjà rempli par vue_choix_secret

    vue_plateau()

# ─────────────────────────────────────────
# VUE : PLATEAU DE JEU
# ─────────────────────────────────────────

def vue_plateau():
    """Affiche la grille de jeu complète."""
    vider_fenetre()

    n_p = etat["param_pions"]
    n_e = etat["param_essais"]

    largeur = max(480, n_p * 55 + 160)
    hauteur = n_e * 44 + 220
    etat["fen"].geometry(f"{largeur}x{hauteur}")
    etat["fen"].configure(bg=BG)

    # Titre
    tk.Label(etat["fen"], text="MASTERMIND",
             font=("Courier New", 14, "bold"),
             bg=BG, fg=ACCENT).pack(pady=(10, 2))

    # Compteur d'essais
    nb_joues = len(etat["essais"])
    label_num = tk.Label(etat["fen"],
                         text=f"Essai {nb_joues + 1} / {n_e}",
                         font=("Courier New", 10),
                         bg=BG, fg=TEXTE2)
    label_num.pack()
    etat["label_essai_num"] = label_num

    # ── Grille des essais ──
    frame_grille = tk.Frame(etat["fen"], bg=BG)
    frame_grille.pack(pady=6)

    # En-tête colonnes
    frame_entete = tk.Frame(frame_grille, bg=BG)
    frame_entete.pack()
    tk.Label(frame_entete, text="Essais",
             font=("Courier New", 9), bg=BG, fg=TEXTE2,
             width=n_p * 6).pack(side=tk.LEFT)
    tk.Label(frame_entete, text="  BP  MP",
             font=("Courier New", 9), bg=BG, fg=TEXTE2).pack(side=tk.LEFT)

    etat["labels_grille"]   = []
    etat["labels_feedback"] = []

    for i in range(n_e):
        ligne = tk.Frame(frame_grille, bg=BG)
        ligne.pack(pady=1)

        pions_ligne = []
        for j in range(n_p):
            lbl = tk.Label(ligne, bg=BG3,
                           width=3, height=1,
                           relief="ridge", bd=2,
                           font=("Courier New", 12))
            lbl.pack(side=tk.LEFT, padx=3)
            pions_ligne.append(lbl)
        etat["labels_grille"].append(pions_ligne)

        lbl_fb = tk.Label(ligne, text="  —  ",
                          font=("Courier New", 10),
                          bg=BG, fg=TEXTE2, width=8)
        lbl_fb.pack(side=tk.LEFT, padx=5)
        etat["labels_feedback"].append(lbl_fb)

    # Remplir les essais déjà joués (si partie chargée)
    for i, (e, bp, mp) in enumerate(etat["essais"]):
        afficher_ligne(i, e, bp, mp)

    # ── Zone de saisie de l'essai courant ──
    tk.Label(etat["fen"], text="Votre essai :",
             font=("Courier New", 10),
             bg=BG, fg=TEXTE2).pack(pady=(8, 2))

    frame_saisie = tk.Frame(etat["fen"], bg=BG)
    frame_saisie.pack()
    etat["labels_saisie"] = []
    for _ in range(n_p):
        lbl = tk.Label(frame_saisie, bg=BG3,
                       width=4, height=2,
                       relief="ridge", bd=2)
        lbl.pack(side=tk.LEFT, padx=4)
        etat["labels_saisie"].append(lbl)

    # ── Palette de couleurs ──
    frame_pal = tk.Frame(etat["fen"], bg=BG)
    frame_pal.pack(pady=5)
    n_c = etat["param_couleurs"]
    for i in range(n_c):
        tk.Button(frame_pal, bg=COULEURS[i], width=3, height=1,
                  relief="flat", cursor="hand2",
                  command=lambda idx=i: ajouter_pion(idx)
                  ).pack(side=tk.LEFT, padx=3)

    # ── Boutons d'action ──
    frame_act = tk.Frame(etat["fen"], bg=BG)
    frame_act.pack(pady=5)

    btn_val = tk.Button(frame_act, text="Valider",
                        font=("Courier New", 10, "bold"),
                        bg=ACCENT, fg=TEXTE,
                        relief="flat", cursor="hand2",
                        state=tk.DISABLED,
                        command=valider_essai)
    btn_val.pack(side=tk.LEFT, padx=4)
    etat["btn_valider"] = btn_val

    tk.Button(frame_act, text="Effacer",
              font=("Courier New", 10), bg=BG2, fg=TEXTE,
              relief="flat", cursor="hand2",
              command=effacer_pion).pack(side=tk.LEFT, padx=4)

    tk.Button(frame_act, text="Annuler essai",
              font=("Courier New", 10), bg=BG2, fg=TEXTE,
              relief="flat", cursor="hand2",
              command=annuler_essai).pack(side=tk.LEFT, padx=4)

    tk.Button(frame_act, text="Aide",
              font=("Courier New", 10), bg=BG2, fg="#36EBC6",
              relief="flat", cursor="hand2",
              command=afficher_aide).pack(side=tk.LEFT, padx=4)

    frame_act2 = tk.Frame(etat["fen"], bg=BG)
    frame_act2.pack(pady=3)

    tk.Button(frame_act2, text="Sauvegarder",
              font=("Courier New", 9), bg=BG2, fg=TEXTE,
              relief="flat", cursor="hand2",
              command=action_sauvegarder).pack(side=tk.LEFT, padx=4)

    tk.Button(frame_act2, text="Menu",
              font=("Courier New", 9), bg=BG, fg=TEXTE2,
              relief="flat", cursor="hand2",
              command=vue_menu).pack(side=tk.LEFT, padx=4)


def afficher_ligne(ligne_idx, essai, bp, mp):
    """Met à jour visuellement une ligne de la grille avec l'essai et son résultat."""
    for j, c in enumerate(essai):
        etat["labels_grille"][ligne_idx][j].configure(bg=COULEURS[c])
    etat["labels_feedback"][ligne_idx].configure(
        text=f"  {bp}●  {mp}○",
        fg=TEXTE
    )

# ─────────────────────────────────────────
# ACTIONS SUR LE PLATEAU
# ─────────────────────────────────────────

def ajouter_pion(idx):
    """Ajoute un pion de couleur idx à l'essai en cours de saisie."""
    n_p = etat["param_pions"]
    if etat["partie_finie"]:
        return
    if len(etat["essai_courant"]) < n_p:
        etat["essai_courant"].append(idx)
        pos = len(etat["essai_courant"]) - 1
        etat["labels_saisie"][pos].configure(bg=COULEURS[idx])
        if len(etat["essai_courant"]) == n_p:
            etat["btn_valider"].configure(state=tk.NORMAL)


def effacer_pion():
    """Efface le dernier pion de la saisie en cours."""
    if etat["essai_courant"]:
        etat["essai_courant"].pop()
        pos = len(etat["essai_courant"])
        etat["labels_saisie"][pos].configure(bg=BG3)
        etat["btn_valider"].configure(state=tk.DISABLED)


def valider_essai():
    """
    Valide l'essai courant :
    appelle evaluer_essai() (fournie par logique.py),
    met à jour la grille, vérifie victoire/défaite.
    """
    if etat["partie_finie"]:
        return

    essai     = etat["essai_courant"].copy()
    # evaluer_essai est importée de logique.py
    bp, mp    = evaluer_essai(etat["secret"], essai)
    ligne_idx = len(etat["essais"])

    etat["essais"].append((essai, bp, mp))
    afficher_ligne(ligne_idx, essai, bp, mp)

    # Réinitialiser la saisie
    etat["essai_courant"] = []
    for lbl in etat["labels_saisie"]:
        lbl.configure(bg=BG3)
    etat["btn_valider"].configure(state=tk.DISABLED)

    n_p      = etat["param_pions"]
    n_e      = etat["param_essais"]
    nb_joues = len(etat["essais"])

    if nb_joues < n_e:
        etat["label_essai_num"].configure(
            text=f"Essai {nb_joues + 1} / {n_e}")

    # Victoire ?
    if bp == n_p:
        etat["partie_finie"] = True
        code_str = "  ".join([NOMS[c] for c in etat["secret"]])
        messagebox.showinfo("Gagné !",
                            f"Bravo ! Code trouvé en {nb_joues} essai(s) !\nCode : {code_str}")
        return

    # Défaite ?
    if nb_joues >= n_e:
        etat["partie_finie"] = True
        code_str = "  ".join([NOMS[c] for c in etat["secret"]])
        messagebox.showinfo("Perdu !",
                            f"Plus d'essais !\nLe code était : {code_str}")


def annuler_essai():
    """Annule le dernier essai validé (fonction triche demandée par le sujet)."""
    if not etat["essais"]:
        messagebox.showinfo("Annuler", "Aucun essai à annuler.")
        return

    ligne_idx = len(etat["essais"]) - 1
    etat["essais"].pop()

    n_p = etat["param_pions"]
    for j in range(n_p):
        etat["labels_grille"][ligne_idx][j].configure(bg=BG3)
    etat["labels_feedback"][ligne_idx].configure(text="  —  ", fg=TEXTE2)

    nb_joues = len(etat["essais"])
    etat["label_essai_num"].configure(
        text=f"Essai {nb_joues + 1} / {etat['param_essais']}")
    etat["partie_finie"] = False
    etat["btn_valider"].configure(state=tk.DISABLED)


def afficher_aide():
    """
    Demande une suggestion à la logique et l'affiche.
    La fonction trouver_suggestion() doit être fournie par logique.py.
    """
    # Import local pour ne pas bloquer si logique.py n'est pas encore prête
    try:
        from logique import trouver_suggestion
        suggestion = trouver_suggestion(etat["essais"],
                                        etat["param_pions"],
                                        etat["param_couleurs"])
        if suggestion is None:
            messagebox.showinfo("Aide", "Aucun code compatible trouvé.")
        else:
            noms_sugg = "  ".join([NOMS[c] for c in suggestion])
            messagebox.showinfo("Aide",
                                f"Code compatible avec vos essais :\n{noms_sugg}")
    except ImportError:
        messagebox.showinfo("Aide", "Fonction d'aide non encore disponible.")


# ─────────────────────────────────────────
# ACTIONS SAUVEGARDE / CHARGEMENT
# ─────────────────────────────────────────

def action_sauvegarder():
    """Prépare les données et appelle sauvegarder_partie() de fichiers.py."""
    donnees = {
        "mode"          : etat["mode"],
        "secret"        : etat["secret"],
        "essais"        : etat["essais"],
        "param_pions"   : etat["param_pions"],
        "param_couleurs": etat["param_couleurs"],
        "param_essais"  : etat["param_essais"],
    }
    sauvegarder_partie(donnees)
    messagebox.showinfo("Sauvegarde", "Partie sauvegardée !")


def action_charger():
    """Appelle charger_partie() de fichiers.py et relance le plateau."""
    donnees = charger_partie()
    if donnees is None:
        messagebox.showerror("Erreur", "Aucune sauvegarde trouvée.")
        return
    etat["mode"]           = donnees["mode"]
    etat["secret"]         = donnees["secret"]
    etat["essais"]         = donnees["essais"]
    etat["param_pions"]    = donnees["param_pions"]
    etat["param_couleurs"] = donnees["param_couleurs"]
    etat["param_essais"]   = donnees["param_essais"]
    etat["partie_finie"]   = False
    etat["essai_courant"]  = []
    vue_plateau()

# ─────────────────────────────────────────
# LANCEMENT
# ─────────────────────────────────────────

def lancer_application():
    """Crée la fenêtre Tkinter et affiche le menu."""
    fen = tk.Tk()
    fen.title("Mastermind - L1 MIASHS")
    fen.resizable(False, False)
    etat["fen"] = fen
    vue_menu()
    fen.mainloop()


lancer_application()
