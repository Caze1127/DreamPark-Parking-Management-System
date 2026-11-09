import tkinter as tk
from tkinter import messagebox 


class VueMessage:
    def __init__(self, fenetre_principale):
        
        self.fenetre = fenetre_principale

    def afficher_erreur(self, message):
        messagebox.showerror("Erreur: ", message, parent=self.fenetre)

    def afficher_information(self, message):
        messagebox.showinfo("Dream Park", message, parent= self.fenetre)    