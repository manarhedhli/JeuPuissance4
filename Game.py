from tkinter import Label
from tkinter import Frame
from tkinter import Canvas
from tkinter import PhotoImage
from tkinter import Button
from tkinter import Toplevel
from PIL import ImageTk, Image

VD = 0
J1 = 1
J2 = 2
GRILLE = []


class Grille(Frame):
    def __init__(self, master):
        Frame.__init__(self)
        self.master = master
        self.master.geometry("400x500")
        self.master.iconphoto(False, PhotoImage(file='images/icon.png'))
        self.master.resizable(height=False, width=False)

        # Canvas
        self.can = Canvas(self.master, bg="#C0C0C0", width=400, height=500,
                          borderwidth=0, highlightthickness=1, highlightbackground="#C0C0C0")
        self.can.pack(side='top')

        # Bouton Quitter
        img_quiter = ImageTk.PhotoImage(Image.open("images/quit.png"))
        self.btn_quitter = Button(self.can, image=img_quiter, borderwidth=0,
                                  width=42, height=40, command=self.gerer_fermeture,  bg="#C0C0C0")
        self.btn_quitter.place(x=95, y=430)

        # Bouton Reinitialiser
        img_rejouer = ImageTk.PhotoImage(Image.open("images/restart.png"))
        self.btn_rejouer = Button(self.can, image=img_rejouer, borderwidth=0,
                                  width=42, height=40, command=self.gerer_reinitialiser,  bg="#C0C0C0")
        self.btn_rejouer.place(x=255, y=430)

        self.init_donnees()
        self.master.mainloop()

    # Initialiser les données

    def init_donnees(self):

        global GRILLE
        GRILLE = [
            [VD, VD, VD, VD, VD, VD, VD],
            [VD, VD, VD, VD, VD, VD, VD],
            [VD, VD, VD, VD, VD, VD, VD],
            [VD, VD, VD, VD, VD, VD, VD],
            [VD, VD, VD, VD, VD, VD, VD],
            [VD, VD, VD, VD, VD, VD, VD]
        ]
        self.tracer_grille()
        self.joueur_courant = J1
        self.can.itemconfigure(self.tour, fill="black")
        self.can.bind("<Button-1>", self.clic)

    # Tracer la grille
    def tracer_grille(self):
        self.can.create_rectangle(
            25, 25, 375, 325, fill='#808080', outline='white')
        x = 75
        for l in range(6):  # lignes horizontales
            self.can.create_line(25, x, 375, x, fill="white")
            x += 50
        x = 75
        for c in range(7):  # lignes verticales
            self.can.create_line(x, 25, x, 325, fill="white")
            x += 50

        self.can.create_rectangle(
            125, 345, 275, 395, fill='#808080', outline='white')
        self.info = self.can.create_text(160, 370, text="Joueur", font='Arial')
        self.tour = self.can.create_oval(230, 350, 270, 390, fill='grey')

    # Gérer les clic sur le Canvas
    def clic(self, event):
        x = event.x
        y = event.y
        if x < 375 and y < 325 and x > 25 and y > 25:  # Ne dériger que les clic sur la grille
            c = int((x-25)/50)
            l = int((y-25)/50)
            if (l >= 25 or l <= 325) and (c >= 25 or c <= 375):
                l = self.trouver_ligne(c)
                if l >= 0:
                    GRILLE[l][c] = self.joueur_courant
                    self.tracer_pion(l, c)
                    if self.chercher_4_pions():
                        self.gerer_victoire()
                    elif self.est_pleine():
                        self.gerer_partie_nulle()
                    else:
                        self.changer_joueur()

    def trouver_ligne(self, c):
        for l in range(5, -1, -1):
            if GRILLE[l][c] == VD:
                return l
        return -1

    def tracer_pion(self, l, c):
        if GRILLE[l][c] != VD:
            x1 = 25 + c * 50 + 5
            x2 = 25 + (c + 1) * 50 - 5
            y1 = 25 + l * 50 + 5
            y2 = 25 + (l + 1) * 50 - 5
            if GRILLE[l][c] == J1:
                self.can.create_oval(x1, y1, x2, y2, width=1, fill='black')
            if GRILLE[l][c] == J2:
                self.can.create_oval(x1, y1, x2, y2, width=1, fill='white')

    def est_pleine(self):
        for c in range(7):
            if GRILLE[0][c] == VD:
                return False
        return True

    def changer_joueur(self):
        if self.joueur_courant == J1:
            self.joueur_courant = J2
            self.can.itemconfigure(self.tour, fill="white")
        else:
            self.joueur_courant = J1
            self.can.itemconfigure(self.tour, fill="black")

    def chercher_4_pions(self):
        if self.quatre_pions_verticale():
            return True
        if self.quatre_pions_horizontale():
            return True
        if self.quatre_pions_diagonale_1():
            return True
        if self.quatre_pions_diagonale_2():
            return True
        return False

    def quatre_pions_verticale(self):  # |
        for l in range(5, 2, -1):
            for c in range(7):
                if GRILLE[l][c] == self.joueur_courant:
                    if GRILLE[l][c] == GRILLE[l-1][c] == GRILLE[l-2][c] == GRILLE[l-3][c]:
                        self.can.create_line(
                            50+50*c, 25+50*(l+1), 50+50*c, 25+50*(l-3), fill='grey', width=4)
                        return True
        return False

    def quatre_pions_horizontale(self):  # --
        for l in range(6):
            for c in range(4):
                if GRILLE[l][c] == self.joueur_courant:
                    if GRILLE[l][c] == GRILLE[l][c+1] == GRILLE[l][c+2] == GRILLE[l][c+3]:
                        self.can.create_line(
                            25+50*c, 50+50*l, 25+50*(c+4), 50+50*l, fill='grey', width=4)
                        return True
        return False

    def quatre_pions_diagonale_1(self):  # /
        for l in range(5, 2, -1):
            for c in range(4):
                if GRILLE[l][c] == self.joueur_courant:
                    if GRILLE[l][c] == GRILLE[l-1][c+1] == GRILLE[l-2][c+2] == GRILLE[l-3][c+3]:
                        self.can.create_line(
                            25+50*c, 25+50*(l+1), 25+50*(c+4), 25+50*(l-3), fill='grey', width=4)
                        return True
        return False

    def quatre_pions_diagonale_2(self):
        for l in range(5, 2, -1):
            for c in range(6, 2, -1):
                if GRILLE[l][c] == self.joueur_courant:
                    if GRILLE[l][c] == GRILLE[l-1][c-1] == GRILLE[l-2][c-2] == GRILLE[l-3][c-3]:
                        self.can.create_line(
                            25+50*(c+1), 25+50*(l+1), 25+50*(c-3), 25+50*(l-3), fill='grey', width=4)
                        return True
        return False

    # gérer l'action provenant de l'alerte de fermeture du jeu
    def choix_fermeture(self, option):
        msg_box.destroy()
        self.btn_quitter.configure(state='active')
        self.btn_rejouer.configure(state='active')
        if option == "Oui":
            self.master.destroy()
        else:
            self.can.bind("<Button-1>", self.clic)

    # Définir un alerte avant la fermeture du jeu
    def gerer_fermeture(self):

        self.btn_quitter.configure(state='disabled')
        self.btn_rejouer.configure(state='disabled')
        self.can.unbind("<Button 1>")

        # Variable globale pour assurer sa fermeture dans la méthode choix_fermeture (en cliquant sur le bouton Quitter)
        global msg_box
        msg_box = Toplevel(self.master)
        msg_box.iconphoto(False, PhotoImage(file='images/icon.png'))
        msg_box.title('Quitter')
        msg_box.geometry("250x150")

        label_info = Label(
            msg_box, text='Voulez-vous Quitter\n cette partie ?', font='Arial')
        label_info.pack(pady=5, padx=5)

        frame = Frame(msg_box)
        frame.pack(pady=5)

        global img_gagne
        img_gagne = ImageTk.PhotoImage(Image.open("images/question.png"))
        lab_img_gagne = Label(frame, image=img_gagne,
                              borderwidth=0, width=80, height=80)
        lab_img_gagne.grid(row=0, column=0)

        btn_oui = Button(frame, text="Quitter", borderwidth=0, width=8,
                         height=1, bg="grey", command=lambda: self.choix_fermeture("Oui"))
        btn_non = Button(frame, text="Annuler", borderwidth=0, width=8,
                         height=1, bg="grey", command=lambda: self.choix_fermeture("Non"))

        btn_oui.grid(row=0, column=1, padx=5)
        btn_non.grid(row=0, column=2, padx=5)

    def choix_reinitialiser(self, option):
        msg_box.destroy()
        self.btn_quitter.configure(state='active')
        self.btn_rejouer.configure(state='active')
        if option == "Oui":
            self.init_donnees()
        else:
            self.can.bind("<Button-1>", self.clic)

    # Définir un alerte avant la réinitialisation d'une partie
    def gerer_reinitialiser(self):
        self.btn_quitter.configure(state='disabled')
        self.btn_rejouer.configure(state='disabled')
        self.can.unbind("<Button 1>")

        global msg_box
        msg_box = Toplevel(self.master)
        msg_box.iconphoto(False, PhotoImage(file='images/icon.png'))
        msg_box.title('Réinitialiser')
        msg_box.geometry("250x150")

        label_info = Label(
            msg_box, text='Voulez-vous commencer une \nnouvelle partie ?', font='Arial')
        label_info.pack(pady=5, padx=5)

        frame = Frame(msg_box)
        frame.pack(pady=5)

        global img_gagne
        img_gagne = ImageTk.PhotoImage(Image.open("images/Question.png"))
        lab_img_gagne = Label(frame, image=img_gagne,
                              borderwidth=0, width=80, height=80)
        lab_img_gagne.grid(row=0, column=0)

        btn_oui = Button(frame, text="Rejouer", borderwidth=0, width=8, height=1,
                         bg="grey", command=lambda: self.choix_reinitialiser("Oui"))
        btn_non = Button(frame, text="Annuler", borderwidth=0, width=8, height=1,
                         bg="grey", command=lambda: self.choix_reinitialiser("Non"))

        btn_oui.grid(row=0, column=1, padx=5)
        btn_non.grid(row=0, column=2, padx=5)

    def rejouer(self, option):
        msg_box.destroy()
        self.btn_quitter.configure(state='active')
        self.btn_rejouer.configure(state='active')
        if option == "Rejouer":
            self.init_donnees()

    # Définir un alerte pour annoncer le gagnant
    def gerer_victoire(self):
        self.btn_quitter.configure(state='disabled')
        self.btn_rejouer.configure(state='disabled')
        if self.joueur_courant == J1:
            couleur = "noirs"
        else:
            couleur = "blans"
        self.can.unbind("<Button 1>")

        global msg_box
        msg_box = Toplevel(self.master)
        msg_box.iconphoto(False, PhotoImage(file='images/icon.png'))
        msg_box.title('Résultat')
        msg_box.geometry("250x150")

        label_info = Label(msg_box, text='Félicitations!\n Joueur avec pions {} a gagné !!'.format(
            couleur), font='Arial')
        label_info.pack(pady=5, padx=5)

        frame = Frame(msg_box)
        frame.pack(pady=5)

        global img_gagne
        img_gagne = ImageTk.PhotoImage(Image.open("images/winner.png"))
        lab_img_gagne = Label(frame, image=img_gagne,
                              borderwidth=0, width=80, height=80)
        lab_img_gagne.grid(row=0, column=0)
        btn_rej = Button(frame, text="Rejouer", borderwidth=0, width=10,
                         height=1, bg="grey", command=lambda: self.rejouer("Rejouer"))
        btn_rej.grid(row=0, column=2, padx=10)

    def gerer_partie_nulle(self):
        self.btn_quitter.configure(state='disabled')
        self.btn_rejouer.configure(state='disabled')
        self.can.unbind("<Button 1>")
        global msg_box
        msg_box = Toplevel(self.master)
        msg_box.iconphoto(False, PhotoImage(file='images/icon.png'))
        msg_box.title('Partie nulle')
        msg_box.geometry("250x120")
        label_info = Label(msg_box, text='Partie Nulle !', font='Arial')
        label_info.pack(pady=8, padx=5)
        frame = Frame(msg_box)
        frame.pack(pady=5)
        global img_perdu
        img_perdu = ImageTk.PhotoImage(Image.open("images/looser.png"))
        lab_img_perdu = Label(frame, image=img_perdu,
                              borderwidth=0, width=80, height=80)
        lab_img_perdu.grid(row=0, column=0)
        btn_rej = Button(frame, text="Rejouer", borderwidth=0, width=10,
                         height=1, bg="grey", command=lambda: self.rejouer("Rejouer"))
        btn_rej.grid(row=0, column=2, padx=10)
