from tkinter import Label
from tkinter import Frame
from tkinter import PhotoImage
from tkinter import Button
from tkinter import Toplevel
from tkinter import Message
from PIL import ImageTk, Image
from Game import Grille


class Main(Frame):
    def __init__(self):
        Frame.__init__(self)
        self.master.geometry("400x500")
        self.master.title("Puissance 4")

        self.master.resizable(height=False, width=False)

        # Image de Fond de la fênetre principal
        self.img_fond = ImageTk.PhotoImage(Image.open("images/home.png"))
        self.lab_fond = Label(image=self.img_fond)
        self.lab_fond.place(x=0, y=0)

        # icone
        self.master.iconphoto(False, PhotoImage(file='images/icon.png'))

        # Bouton Quitter
        self.img_quiter = ImageTk.PhotoImage(Image.open("images/close.png"))
        self.btn_quitter = Button(
            image=self.img_quiter, borderwidth=0, width=40, height=40, command=self.master.destroy, background="#ff3962")
        self.btn_quitter.place(x=175, y=420)

        # Bouton Jouer
        self.img_jouer = ImageTk.PhotoImage(Image.open("images/start.png"))
        self.btn_jouer = Button(
            image=self.img_jouer, borderwidth=0, width=40, height=40, command=self.create, background="#ff3962")
        self.btn_jouer.place(x=175, y=375)

        # Bouton principe du jeu
        self.img_principe = ImageTk.PhotoImage(
            Image.open("images/principle.png"))
        self.btn_principe = Button(
            image=self.img_principe, borderwidth=0, width=15, height=15, command=self.principe, background="#ff3962")
        self.btn_principe.place(x=360, y=20)

        # Bouton à propos
        self.img_a_propos = ImageTk.PhotoImage(
            Image.open("images/about.png"))
        self.btn_a_propos = Button(
            image=self.img_a_propos, borderwidth=0, width=15, height=15, command=self.aPropos, background="#ff3962")
        self.btn_a_propos.place(x=360, y=40)

    def create(self):
        self.app = Grille(Toplevel(self.master))

    def principe(self):
        msg = Toplevel(self)
        msg.geometry("400x300")
        msg.title("Principe du jeu")
        msg.iconphoto(False, PhotoImage(file='images/icon.png'))
        Message(msg, width=400, font="Arial",
                text="Deux joueurs s'affrontent, chaque joueur dispose de 21 pions d'une couleur (noir ou blanc).\n"
                "Tour à tour, les deux joueurs placent un pion dans la colonne de leur choix, "
                "le pion coulisse alors jusqu'à la position la plus basse possible dans ladite "
                "colonne et c'est ensuite à l'adversaire de jouer.\n"
                "Le vainqueur est le joueur qui réalise le premier un alignement (horizontal, "
                "vertical ou diagonal) consécutif d'au moins quatre pions de sa couleur.\n"
                "Si, alors que toutes les cases de la grille de jeu sont remplies et aucun des "
                "deux joueurs n'a réalisé un tel alignement, la partie est déclarée nulle.")\
            .pack(padx=10, pady=10)

    def aPropos(self):
        msg = Toplevel(self)
        msg.geometry("400x100")
        msg.title("A propos")
        msg.iconphoto(False, PhotoImage(file='images/icon.png'))
        Message(msg, width=200, font="Arial", aspect=100, justify='center',
                text="Jeu Puissance 4\n\nManar hedhli, Décembre 2021.")\
            .pack(padx=10, pady=10)


if __name__ == '__main__':
    Main().mainloop()
