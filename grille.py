# grille.py

class Grille:
    def __init__(self):
        """Initialisation du plateau de jeu pour Othello (Reversi)."""
        # Crée une grille vide de 8x8
        self.plateau = [[' ' for _ in range(8)] for _ in range(8)]
        # Positionne les quatre pions de départ
        self.plateau[3][3] = 'B' # Blanc
        self.plateau[3][4] = 'N' # Noir
        self.plateau[4][3] = 'N' # Noir
        self.plateau[4][4] = 'B' # Blanc

    def __str__(self):
        """Fournit une représentation textuelle du plateau, conviviale pour l'utilisateur."""
        # Ajoute les numéros de colonnes (1-8)
        sortie = "  1 2 3 4 5 6 7 8\n"
        for i, ligne in enumerate(self.plateau):
            # Ajoute le numéro de ligne (1-8) et le contenu de la ligne
            sortie += f"{i + 1} {' '.join(ligne)} {i + 1}\n"
        # Répète les numéros de colonnes en bas pour une meilleure lisibilité
        sortie += "  1 2 3 4 5 6 7 8"
        return sortie

    def placer_pion(self, lig, col, couleur):
        """Place un pion d'une couleur donnée sur la case spécifiée."""
        self.plateau[lig][col] = couleur

    def flipper_pion(self, lig, col):
        """Inverse la couleur du pion à la position spécifiée (de 'B' à 'N' ou vice-versa)."""
        if self.plateau[lig][col] == 'B':
            self.plateau[lig][col] = 'N'
        elif self.plateau[lig][col] == 'N':
            self.plateau[lig][col] = 'B'

    def couleur_pion(self, lig, col):
        """Retourne la couleur du pion ('B', 'N', ou ' ') à la position spécifiée."""
        return self.plateau[lig][col]

    def est_case_vide(self, lig, col):
        """Vérifie si la case aux coordonnées spécifiées est vide."""
        return self.plateau[lig][col] == ' '

    def retirer_pion(self, lig, col):
        """Retire un pion de la grille, en remettant la case à vide (' ').
        Utilisé par la fonction d'annulation de coup."""
        self.plateau[lig][col] = ' '