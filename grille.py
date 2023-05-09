class Grille:
    def __init__(self):
        """Initialisation du plateau de jeu"""
        self.plateau = [[' ' for _ in range(8)] for _ in range(8)] # Initialiser une grille vide 8x8
        self.plateau[3][3] = 'B' # Positionner les pions de depart pour Othello
        self.plateau[3][4] = 'N'
        self.plateau[4][3] = 'N'
        self.plateau[4][4] = 'B'

    def __str__(self):
        """Affichage du plateau de jeu en mode texte"""
        sortie = "  0 1 2 3 4 5 6 7\n"
        for i, ligne in enumerate(self.plateau):
            sortie += f"{i} {' '.join(ligne)} {i}\n" # Concatener les elements de chaque ligne de la grille en une seule chaine de caracteres
        sortie += "  0 1 2 3 4 5 6 7"
        return sortie

    def placer_pion(self, lig, col, couleur):
        """Place un pion de la couleur donnee a la position specifiee"""
        if self.plateau[lig][col] == ' ': # Verifier si la case est vide
            self.plateau[lig][col] = couleur # Placer le pion
            return True # Indiquer que l'operation s'est bien deroulee
        return False # Indiquer que la case est deja occupee

    def est_dans_grille(self, lig, col):
        """Verifie si la case specifiee est dans la grille"""
        return 0 <= lig < 8 and 0 <= col < 8 # Verifier si la case est dans la grille

    def retourner_pion(self, lig, col):
        """Retourne le pion a la position specifiee"""
        if self.plateau[lig][col] == 'B': # Si le pion est noir
            self.plateau[lig][col] = 'N' # Le retourner en blanc
        elif self.plateau[lig][col] == 'N': # Si le pion est blanc
            self.plateau[lig][col] = 'B' # Le retourner en noir

    def couleur_pion(self, lig, col):
        """Retourne la couleur du pion a la position specifiee"""
        return self.plateau[lig][col] # Renvoyer la couleur du pion a cette position

    def est_case_vide(self, lig, col):
        """Verifie si la case specifiee est vide"""
        return self.plateau[lig][col] == ' ' # Verifier si la case est vide