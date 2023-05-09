import time
class IA:
    def __init__(self, couleur, profondeur):
        """Initialiser la classe IA avec une couleur et une profondeur de recherche donnee"""
        self.couleur = couleur
        self.profondeur = profondeur
        
    def couleur_opposee(self):
        """Retourne la couleur opposee"""
        return 'B' if self.couleur == 'N' else 'N'

    def jouer_coup(self, jeu):
        """ Joue un coup pour l'IA en utilisant l'algorithme alpha-beta """
        # Mesurer le temps de calcul
        start_time = time.time()
        meilleur_coup = self.alpha_beta(jeu, self.profondeur, float('-inf'), float('inf'), True)[1]
        end_time = time.time()
        temps_calcul = end_time - start_time
        # Obtenir les coordonnees du meilleur coup
        ligne, colonne = meilleur_coup
        # Afficher le coup de l'IA et le temps de calcul
        print("le coup de l'IA (",self.couleur,") est :",(ligne + 1, colonne + 1))
        print("Temps de calcul de l'IA : ({:.0f} ms, {:.2f} secondes)".format(temps_calcul * 1000, temps_calcul))
        
        # Jouer le coup sur le plateau de jeu
        jeu.jouer_coup(ligne,colonne)


    def alpha_beta(self, jeu, profondeur, alpha, beta, is_maximizing):
        """ Implemente l'algorithme alpha-beta pour choisir le meilleur coup a jouer """
        # Verifier si la profondeur est atteinte ou si la partie est terminee
        if profondeur == 0 or jeu.partie_terminee():
            evaluation = self.evaluer(jeu)
            return evaluation, None
        
        # Initialiser les variables pour le meilleur coup et sa valeur
        best_value = float('-inf') if is_maximizing else float('inf')
        best_move = None
        
        # Obtenir tous les coups possibles pour le joueur actuel
        coups_possibles = jeu.coups_possibles()
        
        # Si aucun coup n'est possible, changer de joueur et evaluer le coup suivant
        if not coups_possibles:
            jeu.changer_joueur()
            value, _ = self.alpha_beta(jeu, profondeur - 1, alpha, beta, not is_maximizing)
            jeu.changer_joueur()
            return value, None
        
        # Parcourir tous les coups possibles
        for coup in coups_possibles:
            # Obtenir l'etat du jeu apres avoir joue ce coup
            new_game_state = jeu.result(*coup)
            # Calculer la valeur pour cet etat de jeu en appelant recursivement alpha_beta()
            value, _ = self.alpha_beta(new_game_state, profondeur - 1, alpha, beta, not is_maximizing)
    
            # Mettre a jour la meilleure valeur et le meilleur coup selon si on maximise ou minimise la valeur
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
    
            # Couper la recherche si on atteint la limite inferieure ou superieure de l'intervalle
            if beta <= alpha:
                break
    
        return best_value, best_move # Retourner la meilleure valeure de l'evaluation ainsi que le meilleur coup

    def evaluer(self, jeu):
        """ Evalue la position actuelle du jeu pour l'IA """
        # Definition des poids pour chaque position du plateau
        poids_positions = [
            [50, -1, 11,  8],
            [-1, -7, -4,  1],
            [11, -4,  2,  2],
            [ 8,  1,  2, -3]
        ]
    
        # Calcul de la valeur des positions des pions
        valeur_positions = 0
        for i in range(8):
            for j in range(8):
                # Calcul du poids pour la position (i,j)
                poids = poids_positions[min(i, 7 - i)][min(j, 7 - j)]
                # Si la case (i,j) est occupee par l'IA, ajouter le poids a la valeur des positions
                if jeu.grille.plateau[i][j] == self.couleur:
                    valeur_positions += poids
                # Si la case (i,j) est occupee par l'adversaire, soustraire le poids de la valeur des positions
                elif jeu.grille.plateau[i][j] != ' ':
                    valeur_positions -= poids
    
        # Calcul de la mobilite
        coups_possibles_joueur = len(jeu.coups_possibles())
        jeu.changer_joueur()
        coups_possibles_adversaire = len(jeu.coups_possibles())
        jeu.changer_joueur()
        mobilite = coups_possibles_joueur - coups_possibles_adversaire
    
        # Calcul de la stabilite des pions
        stabilite = self.calculer_stabilite(jeu)
    
        # Calcul de la difference de pions
        nb_pions_blancs = sum([ligne.count('B') for ligne in jeu.grille.plateau])
        nb_pions_noirs = sum([ligne.count('N') for ligne in jeu.grille.plateau])
        difference_pions = nb_pions_blancs - nb_pions_noirs if self.couleur == 'B' else nb_pions_noirs - nb_pions_blancs
    
        # Calcul de la parite
        parite = (nb_pions_blancs + nb_pions_noirs) % 2
    
        # Combinaison des facteurs pour obtenir la valeur heuristique finale selon des criteres que l'on a juge pertinent
        valeur_heuristique = 2 * valeur_positions + 30 * mobilite + 15  * stabilite + parite + difference_pions
    
        return valeur_heuristique
    
    def calculer_stabilite(self, jeu):
        """ Calcule la stabilite des pions pour l'IA """
        stabilite = 0
    
        # Les coins sont toujours stables
        coins = [(0, 0), (0, 7), (7, 0), (7, 7)]
    
        for coin in coins:
            i, j = coin
            if jeu.grille.plateau[i][j] == self.couleur:
                # Si le coin est occupe par l'IA, ajouter 30 a la stabilite
                stabilite += 60
            elif jeu.grille.plateau[i][j] != ' ':
                # Si le coin est occupe par l'adversaire, soustraire 30 a la stabilite
                stabilite -= 60
    
        # Les bords sont consideres comme stables s'ils sont adjacents a des pions stables
        for i in range(8):
            for j in range(8):
                if i == 0 or i == 7 or j == 0 or j == 7:
                    if jeu.grille.plateau[i][j] == self.couleur:
                        # Si le bord est occupe par l'IA et qu'il est adjacent a des pions stables, ajouter 5 a la stabilite
                        stable = True
                        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                            x, y = i + dx, j + dy
                            if 0 <= x < 8 and 0 <= y < 8 and jeu.grille.plateau[x][y] == self.couleur_opposee():
                                stable = False
                                break
                        if stable:
                            stabilite += 5
                    elif jeu.grille.plateau[i][j] != ' ':
                        # Si le bord est occupe par l'adversaire et qu'il est adjacent a des pions stables, soustraire 5 a la stabilite
                        stable = True
                        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                            x, y = i + dx, j + dy
                            if 0 <= x < 8 and 0 <= y < 8 and jeu.grille.plateau[x][y] == self.couleur:
                                stable = False
                                break
                        if stable:
                            stabilite -= 5
    
        return stabilite