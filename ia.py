# ia.py
import time

class IA:
    def __init__(self, couleur, profondeur):
        """Initialise l'IA avec sa couleur et la profondeur de recherche pour l'algorithme."""
        self.couleur = couleur
        self.profondeur = profondeur
        # Matrice de poids statique pour évaluer la valeur de chaque case.
        # Les coins sont les plus précieux, les cases adjacentes aux coins sont dangereuses.
        self.poids_positions = [
            [120, -20, 20,  5,  5, 20, -20, 120],
            [-20, -40, -5, -5, -5, -5, -40, -20],
            [ 20,  -5, 15,  3,  3, 15,  -5,  20],
            [  5,  -5,  3,  3,  3,  3,  -5,   5],
            [  5,  -5,  3,  3,  3,  3,  -5,   5],
            [ 20,  -5, 15,  3,  3, 15,  -5,  20],
            [-20, -40, -5, -5, -5, -5, -40, -20],
            [120, -20, 20,  5,  5, 20, -20, 120],
        ]

    def couleur_opposee(self):
        """Retourne la couleur de l'adversaire."""
        return 'B' if self.couleur == 'N' else 'N'

    def trier_coups(self, coups_possibles):
        """Trie les coups possibles pour améliorer l'efficacité de l'élagage alpha-bêta.
        Les meilleurs coups (coins, bords) sont explorés en premier."""
        def score_coup(coup):
            lig, col = coup
            if (lig, col) in [(0,0), (0,7), (7,0), (7,7)]: return 100 # Priorité maximale pour les coins
            if lig in [0, 7] or col in [0, 7]: return 50 # Priorité moyenne pour les bords
            return 0 # Priorité faible pour les autres coups
        
        return sorted(coups_possibles, key=score_coup, reverse=True)

    def jouer_coup(self, jeu):
        """Détermine et joue le meilleur coup pour l'IA."""
        start_time = time.time()
        # L'algorithme retourne (score, meilleur_coup)
        _, meilleur_coup = self.alpha_beta(jeu, self.profondeur, float('-inf'), float('inf'), True)
        end_time = time.time()
        
        if meilleur_coup:
            ligne, colonne = meilleur_coup
            print(f"L'IA ({self.couleur}) joue en : ({ligne + 1}, {colonne + 1})")
            print(f"Temps de calcul de l'IA : {end_time - start_time:.3f} secondes")
            jeu.jouer_coup(ligne, colonne)

    def alpha_beta(self, jeu, profondeur, alpha, beta, est_joueur_maximisant):
        """Implémentation de l'algorithme Minimax avec élagage Alpha-Bêta."""
        if profondeur == 0 or jeu.partie_terminee():
            return self.evaluer(jeu), None

        coups_possibles = self.trier_coups(jeu.coups_possibles())

        # Si aucun coup n'est possible, on passe le tour et on continue la recherche
        if not coups_possibles:
            jeu.changer_joueur()
            val, _ = self.alpha_beta(jeu, profondeur - 1, alpha, beta, not est_joueur_maximisant)
            jeu.changer_joueur()
            return val, None

        meilleur_coup = None
        if est_joueur_maximisant:
            max_eval = float('-inf')
            for coup in coups_possibles:
                pions_retournes = jeu.jouer_coup(coup[0], coup[1])
                evaluation, _ = self.alpha_beta(jeu, profondeur - 1, alpha, beta, False)
                jeu.annuler_coup(coup[0], coup[1], pions_retournes) # Annuler le coup
                
                if evaluation > max_eval:
                    max_eval = evaluation
                    meilleur_coup = coup
                alpha = max(alpha, evaluation)
                if beta <= alpha:
                    break # Élagage Alpha
            return max_eval, meilleur_coup
        else: # Joueur minimisant
            min_eval = float('inf')
            for coup in coups_possibles:
                pions_retournes = jeu.jouer_coup(coup[0], coup[1])
                evaluation, _ = self.alpha_beta(jeu, profondeur - 1, alpha, beta, True)
                jeu.annuler_coup(coup[0], coup[1], pions_retournes) # Annuler le coup
                
                if evaluation < min_eval:
                    min_eval = evaluation
                    meilleur_coup = coup
                beta = min(beta, evaluation)
                if beta <= alpha:
                    break # Élagage Bêta
            return min_eval, meilleur_coup

    def evaluer(self, jeu):
        """Évalue la position actuelle du jeu et retourne un score pour l'IA."""
        scores = jeu.calculer_score()
        if jeu.partie_terminee():
            if scores[self.couleur] > scores[self.couleur_opposee()]: return 10000  # Victoire
            if scores[self.couleur] < scores[self.couleur_opposee()]: return -10000 # Défaite
            return 0 # Match nul

        # Heuristique combinant la valeur positionnelle et la mobilité
        valeur_positions = 0
        for i in range(8):
            for j in range(8):
                couleur_pion = jeu.grille.couleur_pion(i, j)
                if couleur_pion == self.couleur:
                    valeur_positions += self.poids_positions[i][j]
                elif couleur_pion == self.couleur_opposee():
                    valeur_positions -= self.poids_positions[i][j]
        
        # Calcul de la mobilité (nombre de coups possibles)
        mobilite_ia = len(jeu.coups_possibles())
        jeu.changer_joueur()
        mobilite_adversaire = len(jeu.coups_possibles())
        jeu.changer_joueur()
        
        # Le facteur de mobilité est la différence de coups possibles
        mobilite = 15 * (mobilite_ia - mobilite_adversaire)

        return valeur_positions + mobilite