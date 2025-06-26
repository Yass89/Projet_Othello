# main.py      
from ia import IA
from logique_jeu import LogiqueJeu

def afficher_score(jeu):
    """Affiche le score actuel en se basant sur la logique du jeu."""
    scores = jeu.calculer_score()
    print(f"Score : Noirs (N) {scores['N']} - Blancs (B) {scores['B']}")

def jouer_coup_humain(jeu):
    """Gère la saisie et la validation du coup d'un joueur humain."""
    coups_valides = jeu.coups_possibles()
    # Affiche les coups possibles pour aider le joueur
    print("Coups possibles :", [(l + 1, c + 1) for l, c in coups_valides])

    while True:
        try:
            # Demande au joueur de saisir les coordonnées au format "ligne colonne" (ex: 3 4)
            saisie = input(f"C'est à vous de jouer ({jeu.joueur_courant}). Entrez les coordonnées (ligne colonne) : ").split()
            if len(saisie) != 2:
                print("Entrée invalide. Veuillez entrer deux nombres séparés par un espace.")
                continue
            
            lig, col = map(int, saisie)
            # Conversion des coordonnées 1-8 en index 0-7
            lig -= 1
            col -= 1
            
            if (lig, col) in coups_valides:
                jeu.jouer_coup(lig, col)
                break  # Sort de la boucle si le coup est valide
            else:
                print("Coup invalide. Veuillez choisir parmi les coups possibles.")
        except ValueError:
            print("Entrée invalide. Veuillez entrer uniquement des nombres.")

def choisir_difficulte():
    """Permet au joueur de choisir le niveau de difficulté de l'IA."""
    while True:
        try:
            print("\nChoisissez la difficulté de l'IA :")
            print("1. Facile   (Profondeur de recherche : 2)")
            print("2. Moyen    (Profondeur de recherche : 4)")
            print("3. Difficile(Profondeur de recherche : 6)")
            choix = int(input("Votre choix (1-3) : ").strip())
            if choix == 1: return 2
            if choix == 2: return 4
            if choix == 3: return 6
            print("Choix invalide. Veuillez entrer 1, 2 ou 3.")
        except ValueError:
            print("Veuillez entrer un nombre valide.")

def main():
    """Fonction principale qui orchestre le déroulement de la partie."""
    jeu = LogiqueJeu()
    print("--- Bienvenue dans Othello ! ---")

    couleur_humain = ''
    while couleur_humain not in ('N', 'B'):
        couleur_humain = input("Choisissez votre couleur (N pour Noir, B pour Blanc) : ").strip().upper()
    
    couleur_ia = 'B' if couleur_humain == 'N' else 'N'
    difficulte = choisir_difficulte()
    ia = IA(couleur_ia, difficulte)
    
    # Boucle de jeu principale
    while not jeu.partie_terminee():
        print("\n" + "="*25)
        print(jeu.grille)  # Affiche le plateau de jeu
        afficher_score(jeu)
    
        # Si le joueur courant n'a pas de coup possible, il passe son tour
        if not jeu.coups_possibles():
            print(f"\nLe joueur {jeu.joueur_courant} ne peut pas jouer. Son tour est passé.")
            jeu.changer_joueur()
            continue

        if jeu.joueur_courant == couleur_humain:
            jouer_coup_humain(jeu)
        else:
            print(f"\nC'est au tour de l'IA ({ia.couleur})...")
            ia.jouer_coup(jeu)
    
    # Affichage du résultat final
    print("\n" + "="*25)
    print("Partie terminée !")
    print(jeu.grille)
    scores = jeu.calculer_score()
    afficher_score(jeu)

    if scores['N'] > scores['B']:
        gagnant = "Noir (N)"
    elif scores['B'] > scores['N']:
        gagnant = "Blanc (B)"
    else:
        print("Match nul !")
        return
        
    print(f"Le joueur {gagnant} a gagné !")

if __name__ == "__main__":
    main()