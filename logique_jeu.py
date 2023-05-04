from grille import Grille

class LogiqueJeu:
    def __init__(self):
        self.grille = Grille()
        self.joueur_courant = 'N'

    def coup_valide(self, lig, col):
        # Vérifier si la case est vide
        if self.grille.est_case_vide(lig, col):
            # Nord, Sud, Est, Ouest, Nord-Est, Nord-Ouest, Sud-Est, Sud-Ouest
            directions = [
                (-1, -1), (-1, 0), (-1, 1),
                (0, -1),           (0, 1),
                (1, -1), (1, 0), (1, 1)
            ]
    
            for dx, dy in directions:
                x, y = lig + dx, col + dy
                pions_adverses = []
    
                # Parcourir la direction jusqu'a trouver un pion de la meme couleur
                while 0 <= x < 8 and 0 <= y < 8:
                    couleur = self.grille.couleur_pion(x, y)
    
                    if couleur == self.joueur_courant:
                        break
                    elif couleur == ' ':
                        pions_adverses = []
                        break
                    else:
                        pions_adverses.append((x, y))
    
                    x += dx
                    y += dy
    
                # Si on a trouve des pions adverses entre les pions de la meme couleur, le coup est valide
                if pions_adverses:
                    return True
    
        return False
        
            

    def retournement_pions(self, lig, col):
        # Implémentez la logique pour retourner les pions
        return 
    
    def coups_possibles(self):
        # Initialisation d'une liste vide de coups possibles
        coups_possibles = []
        # Parcours de la grille
        for i in range(len(self.grille.plateau)):
            for j in range(len(self.grille.plateau)): 
                if self.coup_valide(i, j): # Verification du coup valide
                    coups_possibles.append((i, j))
        return coups_possibles # Retourner les tuples possibles
                

    def changer_joueur(self):
        self.joueur_courant = 'B' if self.joueur_courant == 'N' else 'N'

    def partie_terminee(self):
        # Verifier si le joueur courant n'a pas de coups possibles
        if not self.coups_possibles():
            # Changer de joueur 
            self.changer_joueur()
            # Verifier si l'autre joueur n'a pas de coups possibles 
            aucun_coup_autre_joueur = not self.coups_possibles()é
            # Rechanger de joueur pour revenir au joueur initial
            self.changer_joueur()
            return aucun_coup_autre_joueur # retour du booleen determinant
                                           # si l'adversaire a un coup possible ou non
        return False # si le joueur courant a un coup possible la partie n'est pas finie

    def jouer_coup(self, lig, col):
        if self.coup_valide(lig, col):
            self.grille.placer_pion(lig, col, self.joueur_courant)
            self.retournement_pions(lig, col)
            self.joueur_suivant()
            return True
        return False