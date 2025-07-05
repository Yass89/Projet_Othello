# 📄 Othello — Code Documentation

This document explains the structure and functionality of the Othello codebase.  
It is intended for developers who wish to understand, modify, or contribute to the project.

---

## 📁 File Structure

```
.
├── ai.py              # AI logic: Minimax + Alpha-Beta pruning
├── board.py           # Board representation & manipulation
├── game_logic.py      # Game rules & move validation
├── ui.py              # Graphical user interface (Tkinter)
├── main.py            # Entry point
└── README.md          # Project overview & usage 
└── DOCUMENTATION.md  # Code-specific documentation
(not covered here)
```

---

## 🧠 Module Overviews

### `main.py`
- Main entry point of the application.
- Creates the Tkinter root window.
- Instantiates the `OthelloUI` class.
- Starts the Tkinter main event loop.
- Includes minimal error handling for missing `tkinter` or unexpected exceptions.

---

### `board.py`
- Defines the `Board` class.
- Represents the 8×8 Othello board as a 2D list (`self.board`).
- Initializes with the 4 starting pieces in the center.
- Methods:
  - `__str__()` — Returns a printable text representation of the board.
  - `place_piece(row, col, color)` — Places a piece (`B` or `W`) at a given square.
  - `flip_piece(row, col)` — Flips a piece from `B` to `W` or vice versa.
  - `piece_color(row, col)` — Returns the piece color at a given square.
  - `is_square_empty(row, col)` — Checks if a square is empty.
  - `remove_piece(row, col)` — Removes a piece from the board (for undo).

---

### `game_logic.py`
- Defines the `GameLogic` class.
- Implements the rules of Othello:
  - Valid move detection.
  - Capturing opponent pieces.
  - Switching turns.
  - Undoing moves (for AI search).
  - Determining game end & score.
- Holds an instance of `Board` as `self.board`.
- Tracks current player (`B` or `W`).
- Key methods:
  - `switch_player()` — Changes turn to the other player.
  - `opponent_pieces_to_flip_in_direction(row, col, dx, dy)` — Returns a list of opponent pieces to flip in a given direction.
  - `is_valid_move(row, col)` — Checks if a move is legal for the current player.
  - `get_possible_moves()` — Lists all legal moves.
  - `play_move(row, col)` — Executes a move, flips pieces, and switches turn.
  - `undo_move(row, col, flipped_pieces)` — Reverts a move and restores board state.
  - `is_game_over()` — Checks if no valid moves remain for either player.
  - `get_score()` — Returns the current piece counts as `{ 'B': int, 'W': int }`.

---

### `ai.py`
- Defines the `AI` class.
- Implements the AI player using the **Minimax algorithm with Alpha-Beta pruning**.
- Initialized with:
  - `color` — AI’s piece color (`B` or `W`).
  - `depth` — Search depth (higher = stronger).
- Includes a position weight matrix to favor corners & edges.
- Key methods:
  - `play_move(game)` — Finds and plays the best move on the given `GameLogic` instance.
  - `alpha_beta(game, depth, alpha, beta, is_maximizing)` — Recursive minimax search.
  - `evaluate(game)` — Heuristic evaluation of the board:
    - Positional weights.
    - Mobility (number of possible moves).
    - Winning/drawing states.
  - `sort_moves(moves)` — Orders moves to improve pruning efficiency.

---

### `ui.py`
- Defines the `OthelloUI` class.
- Implements the **graphical user interface (GUI)** using **Tkinter**.
- Starts with a configuration menu where player chooses:
  - Color (`B` or `W`).
  - AI difficulty (search depth).
- Creates a canvas to display the board & pieces.
- Handles:
  - Drawing the board & pieces.
  - Updating scores & turn labels.
  - Detecting and processing human moves.
  - Triggering AI turns.
  - Handling end-of-game.
  - Restarting a new game.
- Key methods:
  - `create_config_menu()` — Show initial config menu.
  - `start_game()` — Initialize `GameLogic` & `AI`, launch game UI.
  - `create_game_ui()` — Draws board, canvas, labels, buttons.
  - `update_display()` — Redraws board & updates labels.
  - `on_click(event)` — Handles human player’s mouse click.
  - `next_turn()` — Determines next state after a move.
  - `ai_turn()` — Performs the AI’s move.
  - `end_game()` — Shows final scores & winner.

---

## 🔄 Game Flow

1️⃣ **Startup**
- `main.py` → starts Tkinter → `OthelloUI`.

2️⃣ **Configuration**
- User selects color & difficulty → `start_game()`.

3️⃣ **Gameplay**
- `GameLogic` tracks board state & current player.
- Human clicks → validated via `GameLogic` → pieces flipped.
- AI plays using `AI.play_move()` → updates board.

4️⃣ **End of Game**
- When no players can move → `end_game()` shows results.

---

##  Notes

- Board state lives in `Board.board` (2D list of `'B'`, `'W'`, `' '`).
- Current player: `GameLogic.current_player`.
- AI uses positional weights & mobility for heuristic evaluation.
- Undo is implemented (`undo_move`) to allow Minimax to simulate moves.

---
