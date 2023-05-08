from copy import deepcopy
from grille import Grille

class LogiqueJeu:
    def __init__(self):
        self.grille = Grille()
        self.joueur_courant = 'N'
        self.directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),           (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]

    def coup_valide(self, lig, col):
        # Vérifier si la case est vide
        if not self.grille.est_dans_grille(lig, col) or not self.grille.est_case_vide(lig, col):
            return False
        
        
        # Vérifier si un coup est valide dans l'une des directions
        for dx, dy in self.directions:
            if self.pions_adverses(lig, col, dx, dy):
                return True
        
        return False
    
    def result(self, lig, col):
        new_game_state = deepcopy(self)
        new_game_state.jouer_coup(lig, col)
        new_game_state.changer_joueur()
        return new_game_state

    def retournement_pions(self, lig, col):
        pions_a_retourner = []
        
        # Trouver les pions à retourner dans toutes les directions
        for dx, dy in self.directions:
            pions_a_retourner.extend(self.pions_adverses(lig, col, dx, dy))
        
        # Retourner les pions trouvés
        for pion in pions_a_retourner:
            self.grille.retourner_pion(*pion)

    def pions_adverses(self, lig, col, dx, dy):
        pions_adverses = []
        x, y = lig + dx, col + dy

        # Parcourir la direction donnée et collecter les pions adverses
        while 0 <= x < 8 and 0 <= y < 8:
            couleur = self.grille.couleur_pion(x, y)

            if couleur == self.joueur_courant:
                return pions_adverses
            elif couleur == ' ':
                break
            else:
                pions_adverses.append((x, y))

            x += dx
            y += dy

        return []
    

    def coups_possibles(self):
        coups_possibles = []
        
        # Parcourir la grille et ajouter les coups valides à la liste des coups possibles
        for i in range(8):
            for j in range(8):
                if self.coup_valide(i, j):
                    coups_possibles.append((i, j))
        print(coups_possibles)
        return coups_possibles

    def changer_joueur(self):
        self.joueur_courant = 'B' if self.joueur_courant == 'N' else 'N'

    def partie_terminee(self):
        coups_possibles_joueur_courant = self.coups_possibles()
        
        # Si le joueur courant a des coups possibles, la partie n'est pas terminée
        if coups_possibles_joueur_courant:
            return False
        
        # Vérifier si l'autre joueur a des coups possibles
        self.changer_joueur()
        coups_possibles_autre_joueur = self.coups_possibles()
        self.changer_joueur()

        return not coups_possibles_autre_joueur
    
    def calculer_resultat(self):
        nb_pions_blancs = sum([ligne.count('B') for ligne in self.grille.plateau])
        nb_pions_noirs = sum([ligne.count('N') for ligne in self.grille.plateau])
        return nb_pions_blancs - nb_pions_noirs
    
    def jouer_coup(self, lig, col):
            # Si le coup n'est pas valide et qu'il reste des coups possibles pour l'autre joueur, passe son tour
            if not self.coups_possibles():
                print("le tour est passé car aucun coup légal n'est disponible")
                self.changer_joueur()
                return False
            # Si le coup est valide, Placer un pion, retourner les pions adverses et changer de joueur
            self.grille.placer_pion(lig, col, self.joueur_courant)
            self.retournement_pions(lig, col)
            self.changer_joueur()
            return True
    
    def jouer_coup_ia(self, coup):
         # Si le coup est valide, Placer un pion, retourner les pions adverses et changer de joueur
        if coup is not None:
            lig, col = coup
            self.grille.placer_pion(lig, col, self.joueur_courant)
            self.retournement_pions(lig, col)
            self.changer_joueur()
            return True
        else: # sinon on passe le tour 
            print("Le tour est passé car aucun coup légal n'est disponible")
            self.changer_joueur()
            return False