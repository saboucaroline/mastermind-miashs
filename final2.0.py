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