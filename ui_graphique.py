# othello_game.py

import tkinter as tk
from tkinter import ttk, messagebox
from logique_jeu import LogiqueJeu
from ia import IA

# --- Constantes pour l'affichage ---
TAILLE_CASE = 70
COULEUR_PLATEAU = "#008000"  # Vert foncé
COULEUR_LIGNES = "#000000"   # Noir
COULEUR_POSSIBLE = "#A9A9A9" # Gris pour les coups possibles

class OthelloUI:
    def __init__(self, master):
        """Initialisation de l'interface graphique du jeu Othello."""
        self.master = master
        self.master.title("Othello")
        self.master.resizable(False, False)
        
        # --- Création du menu de configuration initial ---
        self.creer_menu_configuration()

    def creer_menu_configuration(self):
        """Affiche un écran de configuration pour démarrer une partie."""
        self.menu_frame = tk.Frame(self.master, padx=20, pady=20)
        self.menu_frame.pack()

        tk.Label(self.menu_frame, text="Configuration de la partie", font=("Arial", 16, "bold")).pack(pady=10)

        # Choix de la couleur
        tk.Label(self.menu_frame, text="Choisissez votre couleur :", font=("Arial", 12)).pack()
        self.couleur_var = tk.StringVar(value='N')
        ttk.Radiobutton(self.menu_frame, text="Noir (commence)", variable=self.couleur_var, value='N').pack()
        ttk.Radiobutton(self.menu_frame, text="Blanc", variable=self.couleur_var, value='B').pack(pady=(0, 15))
        
        # Choix de la difficulté
        tk.Label(self.menu_frame, text="Choisissez la difficulté de l'IA :", font=("Arial", 12)).pack()
        self.difficulte_var = tk.StringVar(value="Moyen")
        options_difficulte = ["Facile", "Moyen", "Difficile"]
        menu_deroulant = ttk.Combobox(self.menu_frame, textvariable=self.difficulte_var, values=options_difficulte, state="readonly")
        menu_deroulant.pack(pady=(0, 20))

        # Bouton pour lancer la partie
        ttk.Button(self.menu_frame, text="Lancer la partie", command=self.lancer_partie).pack()

    def lancer_partie(self):
        """Configure le jeu avec les options choisies et lance l'interface de jeu."""
        # Récupération des choix
        self.couleur_humain = self.couleur_var.get()
        self.couleur_ia = 'B' if self.couleur_humain == 'N' else 'N'
        
        niveaux = {'Facile': 2, 'Moyen': 4, 'Difficile': 6}
        profondeur = niveaux[self.difficulte_var.get()]
        
        # Initialisation de la logique de jeu et de l'IA
        self.jeu = LogiqueJeu()
        self.ia = IA(self.couleur_ia, profondeur)
        
        # Destruction du menu et création de l'interface de jeu
        self.menu_frame.destroy()
        self.creer_interface_jeu()

    def creer_interface_jeu(self):
        """Crée les widgets pour le plateau de jeu."""
        # Frame pour les informations (score, tour)
        info_frame = tk.Frame(self.master, pady=10)
        info_frame.pack(fill="x")

        self.tour_label = tk.Label(info_frame, text="", font=("Arial", 14))
        self.tour_label.pack()
        self.score_label = tk.Label(info_frame, text="", font=("Arial", 14))
        self.score_label.pack()

        # Canvas pour le plateau
        self.canvas = tk.Canvas(self.master, 
                                width=8 * TAILLE_CASE, 
                                height=8 * TAILLE_CASE, 
                                bg=COULEUR_PLATEAU)
        self.canvas.pack(padx=10, pady=10)
        self.canvas.bind("<Button-1>", self.clic_case)

        # Bouton pour recommencer
        bouton_frame = tk.Frame(self.master)
        bouton_frame.pack(pady=10)
        ttk.Button(bouton_frame, text="Nouvelle Partie", command=self.recommencer_partie).pack()
        
        # Lancement du jeu
        self.partie_active = True
        self.dessiner_plateau()
        self.mettre_a_jour_affichage()
        self.demarrer_flux_de_jeu()

    def recommencer_partie(self):
        """Réinitialise l'interface pour afficher le menu de configuration."""
        for widget in self.master.winfo_children():
            widget.destroy()
        self.creer_menu_configuration()

    def dessiner_plateau(self):
        """Dessine la grille et les repères visuels sur le canvas."""
        for i in range(9):
            self.canvas.create_line(i * TAILLE_CASE, 0, i * TAILLE_CASE, 8 * TAILLE_CASE, fill=COULEUR_LIGNES)
            self.canvas.create_line(0, i * TAILLE_CASE, 8 * TAILLE_CASE, i * TAILLE_CASE, fill=COULEUR_LIGNES)
        # Petits cercles de repère
        for r, c in [(2,2), (2,6), (6,2), (6,6)]:
            self.canvas.create_oval(c*TAILLE_CASE-2, r*TAILLE_CASE-2, c*TAILLE_CASE+2, r*TAILLE_CASE+2, fill=COULEUR_LIGNES, outline="")

    def mettre_a_jour_affichage(self):
        """Met à jour l'affichage complet : pions, scores, et statut."""
        self.canvas.delete("pions")
        for lig in range(8):
            for col in range(8):
                pion = self.jeu.grille.couleur_pion(lig, col)
                if pion != ' ':
                    self.dessiner_pion(lig, col, pion)

        if self.partie_active and self.jeu.joueur_courant == self.couleur_humain:
            for lig, col in self.jeu.coups_possibles():
                self.dessiner_coup_possible(lig, col)
        
        scores = self.jeu.calculer_score()
        self.score_label.config(text=f"Score : Noirs (N) {scores['N']} - Blancs (B) {scores['B']}")
        
        if self.partie_active:
            joueur = "Noirs" if self.jeu.joueur_courant == 'N' else "Blancs"
            self.tour_label.config(text=f"Au tour des {joueur}")
        
        self.master.update_idletasks()

    def dessiner_pion(self, lig, col, couleur):
        """Dessine un pion sur la case spécifiée."""
        x0, y0 = col * TAILLE_CASE + 5, lig * TAILLE_CASE + 5
        x1, y1 = (col + 1) * TAILLE_CASE - 5, (lig + 1) * TAILLE_CASE - 5
        fill_color = 'black' if couleur == 'N' else 'white'
        self.canvas.create_oval(x0, y0, x1, y1, fill=fill_color, outline="#1A1A1A", tags="pions")

    def dessiner_coup_possible(self, lig, col):
        """Indique visuellement qu'un coup est possible."""
        x, y = col * TAILLE_CASE + TAILLE_CASE / 2, lig * TAILLE_CASE + TAILLE_CASE / 2
        self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill=COULEUR_POSSIBLE, outline="", tags="pions")

    def clic_case(self, event):
        """Gère le clic de la souris par le joueur humain."""
        if not self.partie_active or self.jeu.joueur_courant != self.couleur_humain:
            return

        col, lig = event.x // TAILLE_CASE, event.y // TAILLE_CASE
        if (lig, col) in self.jeu.coups_possibles():
            self.jeu.jouer_coup(lig, col)
            self.mettre_a_jour_affichage()
            self.gerer_prochain_tour()

    def gerer_prochain_tour(self):
        """
        Méthode centrale qui détermine l'état du jeu après un coup.
        Elle gère la fin de partie, les tours passés, et le passage à l'IA.
        """
        # 1. Priorité absolue : vérifier si la partie est terminée.
        if self.jeu.partie_terminee():
            self.terminer_partie()
            return

        # 2. Vérifier si le joueur courant a des coups.
        if not self.jeu.coups_possibles():
            # Si le joueur courant ne peut pas jouer, on passe son tour.
            self.passer_tour()
            return # La méthode passer_tour s'occupera de la suite.

        # 3. Si le joueur courant est l'IA, on lance son tour.
        if self.jeu.joueur_courant == self.couleur_ia:
            self.master.after(500, self.tour_ia)

    def tour_ia(self):
        """Gère le tour de l'intelligence artificielle."""
        if not self.partie_active or self.jeu.joueur_courant != self.couleur_ia:
            return

        self.tour_label.config(text=f"L'IA ({self.couleur_ia}) réfléchit...")
        self.master.update_idletasks()

        # L'IA joue simplement son coup. Elle n'a plus besoin de vérifier quoi que ce soit.
        self.ia.jouer_coup(self.jeu)
        self.mettre_a_jour_affichage()
        
        # Utiliser la nouvelle méthode centrale pour décider de la suite
        self.gerer_prochain_tour()

    def passer_tour(self):
        """Annonce qu'un tour est passé, change le joueur, et vérifie la suite."""
        messagebox.showinfo("Tour passé", f"Le joueur {self.jeu.joueur_courant} ne peut pas jouer et passe son tour.")
        self.jeu.changer_joueur()
        self.mettre_a_jour_affichage()

        # Après avoir passé le tour, on ré-évalue la situation
        self.gerer_prochain_tour()
    
    def demarrer_flux_de_jeu(self):
        """
        Vérifie l'état initial du jeu et lance le premier tour, 
        qui peut être celui de l'IA si l'humain a choisi les Blancs.
        """
        self.gerer_prochain_tour()
        
    def terminer_partie(self):
        """Affiche le résultat final de la partie."""
        self.partie_active = False
        scores = self.jeu.calculer_score()
        
        if scores['N'] > scores['B']: gagnant = "Les Noirs (N) ont gagné !"
        elif scores['B'] > scores['N']: gagnant = "Les Blancs (B) ont gagné !"
        else: gagnant = "Match nul !"
        
        self.tour_label.config(text="Partie terminée !")
        messagebox.showinfo("Fin de partie", f"{gagnant}\nScore final : Noirs {scores['N']} - Blancs {scores['B']}")