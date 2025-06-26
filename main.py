# main.py

import tkinter as tk
from ui_graphique import OthelloUI

def main():
    """
    Point d'entrée principal de l'application.
    Crée la fenêtre racine Tkinter et lance l'interface graphique du jeu Othello.
    """
    try:
        # Crée la fenêtre principale
        root = tk.Tk()
        # Initialise la classe de l'interface graphique
        OthelloUI(root)
        # Lance la boucle d'événements de Tkinter
        root.mainloop()
    except ImportError:
        print("Erreur critique : Le module 'tkinter' est requis pour lancer ce jeu.")
        print("Veuillez vous assurer que Tkinter est installé avec votre version de Python.")
    except Exception as e:
        print(f"Une erreur inattendue est survenue : {e}")

if __name__ == "__main__":
    main()