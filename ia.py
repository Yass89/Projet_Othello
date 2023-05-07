
class IA:
    def __init__(self, couleur, profondeur=3):
        self.couleur = couleur
        self.profondeur = profondeur

    def jouer_coup(self, jeu):
        meilleur_coup = self.alpha_beta(jeu, self.profondeur, float('-inf'), float('inf'), True)[1]
        print(meilleur_coup)
        if meilleur_coup:
            jeu.jouer_coup(*meilleur_coup)

    def alpha_beta(self, jeu, profondeur, alpha, beta, is_maximizing):
        if profondeur == 0 or jeu.partie_terminee():
            return self.evaluer(jeu), None

        best_move = None
        if is_maximizing:
            best_value = float('-inf')
            for coup in jeu.coups_possibles():
                new_game_state = jeu.result(*coup)
                value = self.alpha_beta(new_game_state, profondeur - 1, alpha, beta, False)[0]
                if value > best_value:
                    best_value = value
                    best_move = coup
                alpha = max(alpha, best_value)
                if beta <= alpha:
                    break
        else:
            best_value = float('inf')
            for coup in jeu.coups_possibles():
                new_game_state = jeu.result(*coup)
                value = self.alpha_beta(new_game_state, profondeur - 1, alpha, beta, True)[0]
                if value < best_value:
                    best_value = value
                    best_move = coup
                beta = min(beta, best_value)
                if beta <= alpha:
                    break

        return best_value, best_move

    def evaluer(self, jeu):
        nb_pions_total = sum([ligne.count('B') + ligne.count('N') for ligne in jeu.grille.plateau])
        nb_pions_restants = 60 - nb_pions_total

        nb_pions_blancs = sum([ligne.count('B') for ligne in jeu.grille.plateau])
        nb_pions_noirs = sum([ligne.count('N') for ligne in jeu.grille.plateau])

        if self.couleur == 'N':
            score = nb_pions_noirs - nb_pions_blancs
        else:
            score = nb_pions_blancs - nb_pions_noirs

        if nb_pions_restants <= (60 - self.profondeur):
            return score
        else:
            return score * (1 - nb_pions_restants / 60)