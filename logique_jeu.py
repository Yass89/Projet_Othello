from copy import deepcopy
from grille import Grille

class LogiqueJeu:
    def __init__(self):
        """Initialisation de la logique de jeu"""
        self.grille = Grille() # Initialiser une grille de jeu
        self.joueur_courant = 'N' # Definir le joueur courant (N pour noir, B pour blanc)
        self.directions = [
            (-1, -1), (-1, 0), (-1, 1), # Directions diagonales
            (0, -1),           (0, 1), # Directions horizontales
            (1, -1), (1, 0), (1, 1) # Directions diagonales
        ]

    def simuler_coup(self, lig, col):
        """Simuler un coup à la position spécifiée et retourner les pions qui seraient retournés"""
        # Créer une copie de l'état actuel du jeu
        etat_simule = deepcopy(self)
        
        # Jouer le coup sur la copie de l'état du jeu
        etat_simule.jouer_coup(lig, col)
        
        # Obtenir les pions qui ont été retournés
        pions_a_retourner = []
    
        # Trouver les pions à retourner dans toutes les directions
        for dx, dy in self.directions:
            pions_a_retourner.extend(etat_simule.pions_adverses(lig, col, dx, dy))
    
        # Retourner la liste des pions qui seraient retournés
        return pions_a_retourner
    
    def coup_valide(self, lig, col):
        """Verifie si un coup est valide a la position specifiee"""
        # Verifier si la case est vide ou si elle n'est pas dans la grille
        if not self.grille.est_dans_grille(lig, col) or not self.grille.est_case_vide(lig, col):
            return False

        # Verifier si un coup est valide dans l'une des directions
        for dx, dy in self.directions:
            if self.pions_adverses(lig, col, dx, dy):
                return True

        return False

    def result(self, lig, col):
        """Obtenir un nouvel etat de jeu resultant d'un coup"""
        new_game_state = deepcopy(self)
        new_game_state.jouer_coup(lig, col)
        new_game_state.changer_joueur()
        return new_game_state

    def retournement_pions(self, lig, col):
        """Retourne les pions adverses a la position specifiee"""
        pions_a_retourner = []

        # Trouver les pions a retourner dans toutes les directions
        for dx, dy in self.directions:
            pions_a_retourner.extend(self.pions_adverses(lig, col, dx, dy))

        # Retourner les pions trouves
        for pion in pions_a_retourner:
            self.grille.retourner_pion(*pion)

    def pions_adverses(self, lig, col, dx, dy):
        """Trouve les pions adverses dans la direction donnee"""
        pions_adverses = []
        x, y = lig + dx, col + dy

        # Parcourir la direction donnee et collecter les pions adverses
        while 0 <= x < 8 and 0 <= y < 8:
            couleur = self.grille.couleur_pion(x, y)

            if couleur == self.joueur_courant:
                return pions_adverses # Si on rencontre un pion de la meme couleur que le joueur courant, on arrete
            elif couleur == ' ':
                break # Si on rencontre une case vide, on arrete
            else:
                pions_adverses.append((x, y)) # Sinon, on ajoute la position du pion adverse a la liste

            x += dx
            y += dy

        return []
    

    def coups_possibles(self):
        """Obtenir la liste des coups possibles"""
        coups_possibles = []

        # Parcourir la grille et ajouter les coups valides a la liste des coups possibles
        for i in range(8):
            for j in range(8):
                if self.coup_valide(i, j):
                    coups_possibles.append((i, j))

        return coups_possibles

    def changer_joueur(self):
        """Changer le joueur courant"""
        self.joueur_courant = 'B' if self.joueur_courant == 'N' else 'N'

    def partie_terminee(self):
        """Verifie si la partie est terminee"""
        coups_possibles_joueur_courant = self.coups_possibles()
    
        # Si le joueur courant a des coups possibles, la partie n'est pas terminee
        if coups_possibles_joueur_courant:
            return False
    
        # Verifier si l'autre joueur a des coups possibles
        self.changer_joueur()
        coups_possibles_autre_joueur = self.coups_possibles()
        self.changer_joueur()
    
        return not coups_possibles_autre_joueur
    
    def calculer_resultat(self):
        """Calculer le resultat de la partie"""
        nb_pions_blancs = sum([ligne.count('B') for ligne in self.grille.plateau])
        nb_pions_noirs = sum([ligne.count('N') for ligne in self.grille.plateau])
        return nb_pions_blancs - nb_pions_noirs
    
    def jouer_coup(self, lig, col):
        """Jouer un coup a la position specifiee"""
        # Si le coup est valide, placer un pion, retourner les pions adverses et changer de joueur
        self.grille.placer_pion(lig, col, self.joueur_courant)
        self.retournement_pions(lig, col)
        self.changer_joueur()