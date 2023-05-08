class IA:
    def __init__(self, couleur, profondeur=3):
        self.couleur = couleur
        self.profondeur = profondeur

    def jouer_coup(self, jeu):
        meilleur_coup = self.alpha_beta(jeu, self.profondeur, float('-inf'), float('inf'), True)[1]
        print(meilleur_coup)
        jeu.jouer_coup_ia(meilleur_coup)

    def alpha_beta(self, jeu, profondeur, alpha, beta, is_maximizing):
        if profondeur == 0 or jeu.partie_terminee():
            return self.evaluer(jeu), None

        best_value = float('-inf') if is_maximizing else float('inf')
        best_move = None

        for coup in jeu.coups_possibles():
            new_game_state = jeu.result(*coup)
            value, _ = self.alpha_beta(new_game_state, profondeur - 1, alpha, beta, not is_maximizing)

            if is_maximizing:
                if value > best_value:
                    best_value = value
                    best_move = coup
                alpha = max(alpha, best_value)
            else:
                if value < best_value:
                    best_value = value
                    best_move = coup
                beta = min(beta, best_value)

            if beta <= alpha:
                break

        return best_value, best_move

    def evaluer(self, jeu):
        poids_positions = [
            [20, -3, 11,  8],
            [-3, -7, -4,  1],
            [11, -4,  2,  2],
            [ 8,  1,  2, -3]
        ]
        
        # Calculer la valeur des positions des pions
        valeur_positions = 0
        for i in range(8):
            for j in range(8):
                poids = poids_positions[min(i, 7 - i)][min(j, 7 - j)]
                if jeu.grille.plateau[i][j] == self.couleur:
                    valeur_positions += poids
                elif jeu.grille.plateau[i][j] != ' ':
                    valeur_positions -= poids

        # Calculer la mobilité
        coups_possibles_joueur = len(jeu.coups_possibles())
        jeu.changer_joueur()
        coups_possibles_adversaire = len(jeu.coups_possibles())
        jeu.changer_joueur()
        mobilité = coups_possibles_joueur - coups_possibles_adversaire

        # Calculer la différence de pions
        nb_pions_blancs = sum([ligne.count('B') for ligne in jeu.grille.plateau])
        nb_pions_noirs = sum([ligne.count('N') for ligne in jeu.grille.plateau])
        difference_pions = nb_pions_blancs - nb_pions_noirs if self.couleur == 'B' else nb_pions_noirs - nb_pions_blancs

        # Combinaison des facteurs
        valeur_heuristique = valeur_positions + 10 * mobilité + difference_pions

        return valeur_heuristique