# ui.py

import tkinter as tk
from tkinter import ttk, messagebox
from game_logic import GameLogic
from ai import AI

# --- Display constants ---
SQUARE_SIZE = 70
BOARD_COLOR = "#008000"      # Dark green
LINE_COLOR = "#000000"       # Black
POSSIBLE_MOVE_COLOR = "#A9A9A9"  # Grey for possible moves

class OthelloUI:
    def __init__(self, master):
        """Initialize the Othello game UI."""
        self.master = master
        self.master.title("Othello")
        self.master.resizable(False, False)

        # --- Create initial configuration menu ---
        self.create_config_menu()

    def create_config_menu(self):
        """Display configuration screen to start a game."""
        self.menu_frame = tk.Frame(self.master, padx=20, pady=20)
        self.menu_frame.pack()

        tk.Label(self.menu_frame, text="Game Configuration", font=("Arial", 16, "bold")).pack(pady=10)

        # Color choice
        tk.Label(self.menu_frame, text="Choose your color:", font=("Arial", 12)).pack()
        self.color_var = tk.StringVar(value='B')
        ttk.Radiobutton(self.menu_frame, text="Black (starts)", variable=self.color_var, value='B').pack()
        ttk.Radiobutton(self.menu_frame, text="White", variable=self.color_var, value='W').pack(pady=(0, 15))

        # Difficulty choice
        tk.Label(self.menu_frame, text="Choose AI difficulty:", font=("Arial", 12)).pack()
        self.difficulty_var = tk.StringVar(value="Medium")
        difficulty_options = ["Easy", "Medium", "Hard"]
        dropdown = ttk.Combobox(self.menu_frame, textvariable=self.difficulty_var, values=difficulty_options, state="readonly")
        dropdown.pack(pady=(0, 20))

        # Start button
        ttk.Button(self.menu_frame, text="Start Game", command=self.start_game).pack()

    def start_game(self):
        """Configure the game with chosen options and launch game UI."""
        self.human_color = self.color_var.get()
        self.ai_color = 'B' if self.human_color == 'W' else 'W'

        levels = {'Easy': 2, 'Medium': 4, 'Hard': 6}
        depth = levels[self.difficulty_var.get()]

        self.game = GameLogic()
        self.ai = AI(self.ai_color, depth)

        self.menu_frame.destroy()
        self.create_game_ui()

    def create_game_ui(self):
        """Create game board widgets."""
        info_frame = tk.Frame(self.master, pady=10)
        info_frame.pack(fill="x")

        self.turn_label = tk.Label(info_frame, text="", font=("Arial", 14))
        self.turn_label.pack()
        self.score_label = tk.Label(info_frame, text="", font=("Arial", 14))
        self.score_label.pack()

        self.canvas = tk.Canvas(self.master,
                                width=8 * SQUARE_SIZE,
                                height=8 * SQUARE_SIZE,
                                bg=BOARD_COLOR)
        self.canvas.pack(padx=10, pady=10)
        self.canvas.bind("<Button-1>", self.on_click)

        btn_frame = tk.Frame(self.master)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="New Game", command=self.restart_game).pack()

        self.game_active = True
        self.draw_board()
        self.update_display()
        self.game_flow()

    def restart_game(self):
        """Reset UI and show config menu."""
        for widget in self.master.winfo_children():
            widget.destroy()
        self.create_config_menu()

    def draw_board(self):
        """Draw grid and markers."""
        for i in range(9):
            self.canvas.create_line(i * SQUARE_SIZE, 0, i * SQUARE_SIZE, 8 * SQUARE_SIZE, fill=LINE_COLOR)
            self.canvas.create_line(0, i * SQUARE_SIZE, 8 * SQUARE_SIZE, i * SQUARE_SIZE, fill=LINE_COLOR)

        for r, c in [(2, 2), (2, 6), (6, 2), (6, 6)]:
            self.canvas.create_oval(c*SQUARE_SIZE-2, r*SQUARE_SIZE-2,
                                    c*SQUARE_SIZE+2, r*SQUARE_SIZE+2,
                                    fill=LINE_COLOR, outline="")

    def update_display(self):
        """Update board, scores, and status."""
        self.canvas.delete("pieces")
        for row in range(8):
            for col in range(8):
                piece = self.game.board.piece_color(row, col)
                if piece != ' ':
                    self.draw_piece(row, col, piece)

        if self.game_active and self.game.current_player == self.human_color:
            for row, col in self.game.get_possible_moves():
                self.draw_possible_move(row, col)

        scores = self.game.get_score()
        self.score_label.config(text=f"Score: Black {scores['B']} - White {scores['W']}")

        if self.game_active:
            player = "Black" if self.game.current_player == 'B' else "White"
            self.turn_label.config(text=f"{player}'s turn")

        self.master.update_idletasks()

    def draw_piece(self, row, col, color):
        """Draw a piece at the specified square."""
        x0, y0 = col * SQUARE_SIZE + 5, row * SQUARE_SIZE + 5
        x1, y1 = (col + 1) * SQUARE_SIZE - 5, (row + 1) * SQUARE_SIZE - 5
        fill_color = 'black' if color == 'B' else 'white'
        self.canvas.create_oval(x0, y0, x1, y1, fill=fill_color, outline="#1A1A1A", tags="pieces")

    def draw_possible_move(self, row, col):
        """Visually indicate a possible move."""
        x, y = col * SQUARE_SIZE + SQUARE_SIZE / 2, row * SQUARE_SIZE + SQUARE_SIZE / 2
        self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill=POSSIBLE_MOVE_COLOR, outline="", tags="pieces")

    def on_click(self, event):
        """Handle human player's mouse click."""
        if not self.game_active or self.game.current_player != self.human_color:
            return

        col, row = event.x // SQUARE_SIZE, event.y // SQUARE_SIZE
        if (row, col) in self.game.get_possible_moves():
            self.game.play_move(row, col)
            self.update_display()
            self.next_turn()

    def next_turn(self):
        """Determine next game state after a move."""
        if self.game.is_game_over():
            self.end_game()
            return

        if not self.game.get_possible_moves():
            self.pass_turn()
            return

        if self.game.current_player == self.ai_color:
            self.master.after(500, self.ai_turn)

    def ai_turn(self):
        """Handle AI's turn."""
        if not self.game_active or self.game.current_player != self.ai_color:
            return

        self.turn_label.config(text=f"AI ({self.ai_color}) is thinking...")
        self.master.update_idletasks()

        self.ai.play_move(self.game)
        self.update_display()
        self.next_turn()

    def pass_turn(self):
        """Announce a pass, switch player, and continue."""
        messagebox.showinfo("Pass",("White Player" if self.game.current_player == 'W' else "Black Player")+ " has no valid moves and passes their turn.")
        self.game.switch_player()
        self.update_display()
        self.next_turn()

    def game_flow(self):
        """Check initial state and start first turn, possibly AI if human is White."""
        self.next_turn()

    def end_game(self):
        """Show final result."""
        self.game_active = False
        scores = self.game.get_score()

        if scores['B'] > scores['W']:
            winner = "Black wins!"
        elif scores['W'] > scores['B']:
            winner = "White wins!"
        else:
            winner = "Draw!"

        self.turn_label.config(text="Game Over!")
        messagebox.showinfo("Game Over", f"{winner}\nFinal score: Black {scores['B']} - White {scores['W']}")
