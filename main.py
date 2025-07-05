# main.py

import tkinter as tk
from ui import OthelloUI

def main():
    """
    Main entry point of the application.
    Creates the Tkinter root window and launches the Othello game UI.
    """
    try:
        # Create the main window
        root = tk.Tk()
        # Set custom window icon
        root.iconbitmap("assets/othello_icon.ico")
        # Initialize the UI class
        OthelloUI(root)
        # Start the Tkinter event loop
        root.mainloop()
    except ImportError:
        print("Critical error: The 'tkinter' module is required to run this game.")
        print("Please make sure Tkinter is installed with your Python version.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
