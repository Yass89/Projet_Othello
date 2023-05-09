from ia import IA
from logique_jeu import LogiqueJeu

def afficher_grille(jeu):
    """ Affiche la grille de jeu """
    print("  1 2 3 4 5 6 7 8") # Affiche la numerotation des colonnes
    for i, ligne in enumerate(jeu.grille.plateau):
        print(i + 1, end=' ') # Affiche la numerotation des lignes
        for case in ligne:
            print(case, end=' ') # Affiche le contenu de chaque case
        print() # Passe a la ligne suivante

def afficher_score(jeu):
    """ Affiche le score du jeu """
    nb_pions_noirs = sum([ligne.count('N') for ligne in jeu.grille.plateau]) # compte le nombre de pions noirs sur la grille
    nb_pions_blancs = sum([ligne.count('B') for ligne in jeu.grille.plateau]) # compte le nombre de pions blancs sur la grille
    print(f"Score : Noirs {nb_pions_noirs} - Blancs {nb_pions_blancs}") # affiche le score 

def jouer_coup_humain(jeu):
    """ Permet à un joueur humain de jouer un coup """
    while True:
        try:
            # Demande au joueur les coordonnées du coup
            print(f"C'est à vous de jouer ({jeu.joueur_courant}). Entrez les coordonnées (ligne, colonne) :")
            lig, col = map(int, input().split())
            lig -= 1
            col -= 1
            # Vérifie si le coup est valide
            if jeu.coup_valide(lig, col):
                break
            else:
                print("Coup invalide, veuillez réessayer.")
        except ValueError:
            print("Coup invalide, veuillez réessayer.")
    # Joue le coup sur le plateau de jeu
    jeu.jouer_coup(lig, col)

def jouer_coup_ia(ia, jeu):
    """ Permet à l'IA de jouer un coup """
    print(f"C'est au tour de l'IA ({ia.couleur}).") # Affiche le message indiquant que c'est le tour de l'IA
    ia.jouer_coup(jeu) # Appelle la methode jouer_coup de l'objet IA en passant l'objet jeu en argument
    
def choisir_difficulte():
    """ Permet de choisir la difficulte de l'IA """
    try:
        # Affiche les options de difficulte et demande a l'utilisateur de saisir un choix
        print("Choisissez la difficulté de l'IA :")
        print("1. Facile")
        print("2. Moyen")
        print("3. Difficile")
        choix = int(input().strip())
        # Verifie si le choix est valide et redemande une saisie si ce n'est pas le cas
        while choix not in range(1, 4):
            print("Veuillez choisir une difficulté valide (1, 2, 3):")
            choix = int(input().strip())
        # Retourne la profondeur de recherche en fonction du choix de l'utilisateur
        if choix == 1:
            return 1
        elif choix == 2:
            return 5
        else:
            return 7
    except ValueError:
        # Redemande une saisie si une exception ValueError est levee
        print("Veuillez choisir une difficulté valide (1, 2, 3):")
        return choisir_difficulte()

def main():
    # Créer un objet LogiqueJeu pour gerer la partie
    jeu = LogiqueJeu()
    # Demander au joueur s'il veut commencer la partie
    print("Bienvenue dans Othello !")
    choix = ''
    while choix not in ('O', 'N', 'o', 'n'):
        print("Voulez-vous commencer la partie ? (O/N)")
        choix = input().strip().upper()
    
    joueur_commence = choix == 'O'
    
    # Choisir la difficulté de l'IA
    difficulte = choisir_difficulte()
    ia_noir = IA('N', difficulte)
    ia_blanc = IA('B', difficulte)
    
    # Jouer la partie
    while not jeu.partie_terminee():
        # Afficher la grille et le score à chaque tour
        afficher_grille(jeu)
        afficher_score(jeu)
    
        # Vérifier si un coup est possible, sinon passer son tour
        if not jeu.coups_possibles():
            print("le tour est passé car aucun coup legal n'est disponible")
            jeu.changer_joueur()
        else:
            # Si c'est le tour du joueur humain, lui demander de jouer, sinon l'IA joue
            if joueur_commence:
                if jeu.joueur_courant == 'N':
                    jouer_coup_humain(jeu)
                else:
                    jouer_coup_ia(ia_blanc, jeu)
            else:
                if jeu.joueur_courant == 'B':
                    jouer_coup_humain(jeu)
                else:
                    jouer_coup_ia(ia_noir, jeu)
    
    # Afficher le résultat de la partie
    afficher_grille(jeu)
    afficher_score(jeu)
    resultat = jeu.calculer_resultat()
    if resultat > 0:
        print("Le joueur Blanc a gagné.")
    elif resultat < 0:
        print("Le joueur Noir a gagné.")
    else:
        print("La partie est terminée. Match nul.")

if __name__ == "__main__":
    main() # Lancement du jeu