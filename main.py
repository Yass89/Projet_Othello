from ia import IA
from logique_jeu import LogiqueJeu

def afficher_grille(jeu):
    print("  1 2 3 4 5 6 7 8")
    for i, ligne in enumerate(jeu.grille.plateau):
        print(i + 1, end=' ')
        for case in ligne:
            print(case, end=' ')
        print()

def afficher_score(jeu):
    nb_pions_noirs = sum([ligne.count('N') for ligne in jeu.grille.plateau])
    nb_pions_blancs = sum([ligne.count('B') for ligne in jeu.grille.plateau])
    print(f"Score : Noirs {nb_pions_noirs} - Blancs {nb_pions_blancs}")

if __name__ == "__main__":
    jeu = LogiqueJeu()

    print("Bienvenue dans Othello !")
    print("Voulez-vous commencer la partie ? (O/N)")
    choix = input().strip().upper()

    joueur_commence = choix == 'O'

    ia_noir = IA('N', 3)
    ia_blanc = IA('B', 3)

    while not jeu.partie_terminee():
        afficher_grille(jeu)
        afficher_score(jeu)

        if joueur_commence:
            if jeu.joueur_courant == 'N':
                while True:
                        print("C'est à vous de jouer (Noir). Entrez les coordonnées (ligne, colonne) :")
                        lig, col = map(int, input().split())
                        lig -= 1
                        col -= 1
                        if jeu.coup_valide(lig, col):
                            break
                        else:
                            print("Coup invalide, veuillez réessayer.")
                jeu.jouer_coup(lig, col)
            else:
                print("C'est au tour de l'IA (Blanc).")
                ia_blanc.jouer_coup(jeu)
        else:
            if jeu.joueur_courant == 'B':
                while True:
                        print("C'est à vous de jouer (Blanc). Entrez les coordonnées (ligne, colonne) :")
                        lig, col = map(int, input().split())
                        lig -= 1
                        col -= 1
                        if jeu.coup_valide(lig, col):
                            break
                        else:
                            print("Coup invalide, veuillez réessayer.")
                jeu.jouer_coup(lig, col)
            else:
                print("C'est au tour de l'IA (Noir).")
                ia_noir.jouer_coup(jeu)

    afficher_grille(jeu)
    afficher_score(jeu)
    resultat = jeu.calculer_resultat()
    if resultat > 0:
        print("Le joueur Blanc a gagné.")
    elif resultat < 0:
        print("Le joueur Noir a gagné.")
    else:
        print("La partie est terminée. Match nul.")