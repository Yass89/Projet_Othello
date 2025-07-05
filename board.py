# board.py

class Board:
    def __init__(self):
        """Initialize the Othello (Reversi) game board."""
        # Create an empty 8x8 board
        self.board = [[' ' for _ in range(8)] for _ in range(8)]
        # Place the four starting pieces
        self.board[3][3] = 'W'  # White
        self.board[3][4] = 'B'  # Black
        self.board[4][3] = 'B'  # Black
        self.board[4][4] = 'W'  # White

    def __str__(self):
        """Return a user-friendly text representation of the board."""
        output = "  1 2 3 4 5 6 7 8\n"
        for i, row in enumerate(self.board):
            output += f"{i + 1} {' '.join(row)} {i + 1}\n"
        output += "  1 2 3 4 5 6 7 8"
        return output

    def place_piece(self, row, col, color):
        """Place a piece of the given color on the specified square."""
        self.board[row][col] = color

    def flip_piece(self, row, col):
        """Flip the piece at the specified position ('W' to 'B' or vice versa)."""
        if self.board[row][col] == 'W':
            self.board[row][col] = 'B'
        elif self.board[row][col] == 'B':
            self.board[row][col] = 'W'

    def piece_color(self, row, col):
        """Return the color of the piece ('W', 'B', or ' ') at the specified position."""
        return self.board[row][col]

    def is_square_empty(self, row, col):
        """Check if the square at the specified coordinates is empty."""
        return self.board[row][col] == ' '

    def remove_piece(self, row, col):
        """Remove a piece from the board, leaving the square empty.
        Used for undoing a move."""
        self.board[row][col] = ' '
