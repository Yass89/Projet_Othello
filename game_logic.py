# game_logic.py
from board import Board

class GameLogic:
    def __init__(self):
        """Initialize the game logic."""
        self.board = Board()
        self.current_player = 'B'  # Black always starts
        self.directions = [(-1, -1), (-1, 0), (-1, 1),
                           (0, -1),          (0, 1),
                           (1, -1),  (1, 0), (1, 1)]

    def switch_player(self):
        """Switch to the next player."""
        self.current_player = 'W' if self.current_player == 'B' else 'B'

    def opponent_pieces_to_flip_in_direction(self, row, col, dx, dy):
        """
        Explore a direction from a starting square to find a line of opponent pieces
        bounded by a piece of the current player.
        Returns the list of positions of pieces to flip.
        """
        pieces_to_flip = []
        x, y = row + dx, col + dy

        while 0 <= x < 8 and 0 <= y < 8:
            square_color = self.board.piece_color(x, y)
            if square_color == ' ':
                return []  # Empty square means no capture in this direction
            if square_color == self.current_player:
                return pieces_to_flip  # Found own piece; valid capture
            
            # Opponent piece: add to temporary list
            pieces_to_flip.append((x, y))
            x += dx
            y += dy
        
        return []  # Reached edge without finding own piece

    def is_valid_move(self, row, col):
        """Check if a move is valid for the current player at the specified position."""
        if not (0 <= row < 8 and 0 <= col < 8) or not self.board.is_square_empty(row, col):
            return False

        for dx, dy in self.directions:
            if self.opponent_pieces_to_flip_in_direction(row, col, dx, dy):
                return True
        return False

    def get_possible_moves(self):
        """Return a list of all valid moves for the current player."""
        return [(i, j) for i in range(8) for j in range(8) if self.is_valid_move(i, j)]
    
    def play_move(self, row, col):
        """
        Play a move: place the piece, flip opponent pieces, and switch player.
        Returns the list of flipped pieces (useful for undo).
        """
        all_flipped_pieces = []
        for dx, dy in self.directions:
            flipped = self.opponent_pieces_to_flip_in_direction(row, col, dx, dy)
            all_flipped_pieces.extend(flipped)

        # Place the new piece
        self.board.place_piece(row, col, self.current_player)
        # Flip captured opponent pieces
        for pos in all_flipped_pieces:
            self.board.flip_piece(*pos)
        
        self.switch_player()
        return all_flipped_pieces

    def undo_move(self, row, col, flipped_pieces):
        """
        Undo a move to restore the previous game state.
        Essential for Minimax to explore the game tree without copies.
        """
        self.switch_player()
        self.board.remove_piece(row, col)
        for pos in flipped_pieces:
            self.board.flip_piece(*pos)

    def is_game_over(self):
        """Check if the game is over (neither player can move)."""
        if self.get_possible_moves():
            return False
        
        self.switch_player()
        if self.get_possible_moves():
            self.switch_player()
            return False
        
        self.switch_player()
        return True
    
    def get_score(self):
        """Compute and return the current score as a dictionary."""
        black_pieces = sum(row.count('B') for row in self.board.board)
        white_pieces = sum(row.count('W') for row in self.board.board)
        return {'B': black_pieces, 'W': white_pieces}
