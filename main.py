# Projet Mastermind - L1 MIASHS
# Groupe : MIASHS2
import tkinter as tk 
from tkinter import messagebox 
import json
from itertools import product 
print("Bienvenue dans le Mastermind !")
# Les fonctions seront ajoutées ici
print("Règles du jeu :  \n -Un joueur choisit son code secret de 4 couleurs parmis 8 \n -L'autre joueur doit deviner ce code en 10 essai maximum \n -A chaque essai, on reçoit : \n  *le nombre de pions BIEN PLACE (bonne couleur, bonne place) \n  *Le nombre de pions MAL PLACES (bonne couleur, mauvaise place)")

nb_pions = 4 
nb_couleurs = 8
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

def vue_choix_secret(self):
        self.vider()
        self.fen.geometry("460x300")
        self.mode = "2joueurs"
        self._code_tmp = []
 
        tk.Label(self.fen, text="Joueur 1 : choisissez le code secret",
                 font=("Courier New", 13, "bold"),
                 bg="#0d0d1a", fg="#e94560").pack(pady=(20, 5))
 
        tk.Label(self.fen, text="Cliquez sur les couleurs pour former le code :",
                 font=("Courier New", 10),
                 bg="#0d0d1a", fg="#8888aa").pack()
 
 
        frame_ap = tk.Frame(self.fen, bg="#0d0d1a")
        frame_ap.pack(pady=12)
        self._ap = []
        for _ in range(nb_pions):
            lbl = tk.Label(frame_ap, bg="#1e1e3a", width=5, height=2,
                           relief="ridge", bd=2)
            lbl.pack(side=tk.LEFT, padx=6)
            self._ap.append(lbl)
 
        frame_pal = tk.Frame(self.fen, bg="#0d0d1a")
        frame_pal.pack(pady=5)
        for i, c in enumerate(couleurs):
            tk.Button(frame_pal, bg=c, width=4, height=2,
                      relief="flat", cursor="hand2",
                      command=lambda idx=i: self._ajouter_secret(idx)
                      ).pack(side=tk.LEFT, padx=4)
 
        frame_btn = tk.Frame(self.fen, bg="#0d0d1a")
        frame_btn.pack(pady=8)
 
        tk.Button(frame_btn, text="Effacer",
                  font=("Courier New", 10), bg="#16213e", fg="#a8dadc",
                  relief="flat", cursor="hand2",
                  command=self._effacer_secret).pack(side=tk.LEFT, padx=8)
 
        self._btn_valider_secret = tk.Button(
            frame_btn, text="Valider le code",
            font=("Courier New", 10, "bold"), bg="#e94560", fg="white",
            relief="flat", cursor="hand2", state=tk.DISABLED,
            command=self._valider_secret)
        self._btn_valider_secret.pack(side=tk.LEFT, padx=8)
 
        tk.Button(frame_btn, text="Menu",
                  font=("Courier New", 10), bg="#0d0d1a", fg="#555577",
                  relief="flat", cursor="hand2",
                  command=self.vue_menu).pack(side=tk.LEFT, padx=8)
 
def _ajouter_secret(self, idx):
        if len(self._code_tmp) < nb_pions:
            self._code_tmp.append(idx)
            pos = len(self._code_tmp) - 1
            self._ap[pos].configure(bg=couleurs[idx])
            if len(self._code_tmp) == nb_pions:
                self._btn_valider_secret.configure(state=tk.NORMAL)
 
def _effacer_secret(self):
        if self._code_tmp:
            self._code_tmp.pop()
            pos = len(self._code_tmp)
            self._ap[pos].configure(bg="#1e1e3a")
            self._btn_valider_secret.configure(state=tk.DISABLED)
 
def _valider_secret(self):
        self.secret = self._code_tmp.copy()
        messagebox.showinfo("Code enregistre",
                            "Le code secret est masque.\nPassez la main au Joueur 2 !")
        self._init_partie()
        self.vue_plateau()
 