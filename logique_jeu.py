# logique_jeu.py
from grille import Grille

class LogiqueJeu:
    def __init__(self):
        """Initialisation de la logique de jeu."""
        self.grille = Grille()
        self.joueur_courant = 'N'  # Le joueur Noir commence toujours
        self.directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    def changer_joueur(self):
        """Passe le tour au joueur suivant."""
        self.joueur_courant = 'B' if self.joueur_courant == 'N' else 'N'

    def pions_adverses_a_retourner_dans_direction(self, lig, col, dx, dy):
        """
        Analyse une direction à partir d'une case de départ pour trouver une ligne de pions
        adversaires encadrée par un pion du joueur courant.
        Retourne la liste des positions des pions à retourner.
        """
        pions_a_retourner = []
        x, y = lig + dx, col + dy

        # Parcourt la ligne tant qu'on est dans la grille
        while 0 <= x < 8 and 0 <= y < 8:
            couleur_case = self.grille.couleur_pion(x, y)
            if couleur_case == ' ':
                return []  # Si on rencontre une case vide, la prise est invalide dans cette direction
            if couleur_case == self.joueur_courant:
                return pions_a_retourner  # Si on rencontre un pion allié, la prise est valide
            
            # Si c'est un pion adverse, on l'ajoute à la liste temporaire
            pions_a_retourner.append((x, y))
            x += dx
            y += dy
        
        return []  # Si on atteint le bord de la grille sans trouver de pion allié, la prise est invalide

    def coup_valide(self, lig, col):
        """Vérifie si un coup est valide pour le joueur courant à la position spécifiée."""
        # Le coup doit être sur une case vide et dans les limites de la grille
        if not (0 <= lig < 8 and 0 <= col < 8) or not self.grille.est_case_vide(lig, col):
            return False

        # Le coup doit retourner au moins un pion adverse
        for dx, dy in self.directions:
            if self.pions_adverses_a_retourner_dans_direction(lig, col, dx, dy):
                return True
        return False

    def coups_possibles(self):
        """Retourne une liste de tous les coups valides pour le joueur courant."""
        return [(i, j) for i in range(8) for j in range(8) if self.coup_valide(i, j)]
    
    def jouer_coup(self, lig, col):
        """
        Joue un coup : place le pion, retourne les pions adverses et change de joueur.
        Retourne la liste des pions qui ont été retournés, pour permettre l'annulation du coup.
        """
        pions_total_retournes = []
        for dx, dy in self.directions:
            pions_a_retourner = self.pions_adverses_a_retourner_dans_direction(lig, col, dx, dy)
            pions_total_retournes.extend(pions_a_retourner)

        # Place le nouveau pion
        self.grille.placer_pion(lig, col, self.joueur_courant)
        # Retourne les pions adverses capturés
        for pion_pos in pions_total_retournes:
            self.grille.flipper_pion(*pion_pos)
        
        self.changer_joueur()
        return pions_total_retournes

    def annuler_coup(self, lig, col, pions_retournes):
        """
        Annule un coup pour restaurer l'état précédent du jeu.
        Essentiel pour l'algorithme Minimax afin d'explorer l'arbre de jeu sans faire de copies.
        """
        # Revenir au joueur qui venait de jouer
        self.changer_joueur() 
        # Retirer le pion qui avait été posé
        self.grille.retirer_pion(lig, col) 
        # Re-flipper les pions pour les rendre à l'adversaire
        for pion_pos in pions_retournes:
            self.grille.flipper_pion(*pion_pos) 

    def partie_terminee(self):
        """Vérifie si la partie est terminée (aucun des deux joueurs ne peut jouer)."""
        if self.coups_possibles():
            return False
        
        # Vérifie si l'autre joueur peut jouer
        self.changer_joueur()
        if self.coups_possibles():
            self.changer_joueur()  # Rétablit le joueur original
            return False
        
        self.changer_joueur()  # Rétablit le joueur original
        return True
    
    def calculer_score(self):
        """Calcule et retourne le score sous forme de dictionnaire."""
        nb_pions_noirs = sum(ligne.count('N') for ligne in self.grille.plateau)
        nb_pions_blancs = sum(ligne.count('B') for ligne in self.grille.plateau)
        return {'N': nb_pions_noirs, 'B': nb_pions_blancs}