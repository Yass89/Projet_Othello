class Grille:
    def __init__(self):
        # Initialisation du plateau de jeu
        self.plateau = [[' ' for _ in range(8)] for _ in range(8)]
        self.plateau[3][3] = 'B'
        self.plateau[3][4] = 'N'
        self.plateau[4][3] = 'N'
        self.plateau[4][4] = 'B'

    def __str__(self):
        # Affichage du plateau de jeu en mode texte
        sortie = "  0 1 2 3 4 5 6 7\n"
        for i, ligne in enumerate(self.plateau):
            sortie += f"{i} {' '.join(ligne)} {i}\n"
        sortie += "  0 1 2 3 4 5 6 7"
        return sortie

    def placer_pion(self, lig, col, couleur):
        # Place un pion de la couleur donnée a la position specifiee
        if self.plateau[lig][col] == ' ':
            self.plateau[lig][col] = couleur
            return True
        return False
    
    def retourner_pion(self, lig, col):
        # Retourne le pion a la position specifiee
        if self.plateau[lig][col] == 'B':
            self.plateau[lig][col] = 'N'
        elif self.plateau[lig][col] == 'N':
            self.plateau[lig][col] = 'B'

    def couleur_pion(self, lig, col):
        # Retourne la couleur du pion à la position specifiee
        return self.plateau[lig][col]

    def est_case_vide(self, lig, col):
        # Verifie si la case spécifiee est vide
        return self.plateau[lig][col] == ' '