# ai.py
import time

class AI:
    def __init__(self, color, depth):
        """Initialize the AI with its color and search depth for the algorithm."""
        self.color = color
        self.depth = depth
        # Static weight matrix to evaluate the value of each square.
        # Corners are most valuable; adjacent squares are dangerous.
        self.position_weights = [
            [120, -20, 20,  5,  5, 20, -20, 120],
            [-20, -40, -5, -5, -5, -5, -40, -20],
            [ 20,  -5, 15,  3,  3, 15,  -5,  20],
            [  5,  -5,  3,  3,  3,  3,  -5,   5],
            [  5,  -5,  3,  3,  3,  3,  -5,   5],
            [ 20,  -5, 15,  3,  3, 15,  -5,  20],
            [-20, -40, -5, -5, -5, -5, -40, -20],
            [120, -20, 20,  5,  5, 20, -20, 120],
        ]

    def opposite_color(self):
        """Return the opponent's color."""
        return 'B' if self.color == 'W' else 'W'

    def sort_moves(self, possible_moves):
        """Sort possible moves to improve Alpha-Beta pruning efficiency.
        Best moves (corners, edges) are explored first."""
        def move_score(move):
            row, col = move
            if (row, col) in [(0, 0), (0, 7), (7, 0), (7, 7)]:
                return 100  # Highest priority for corners
            if row in [0, 7] or col in [0, 7]:
                return 50   # Medium priority for edges
            return 0        # Low priority otherwise

        return sorted(possible_moves, key=move_score, reverse=True)

    def play_move(self, game):
        """Determine and play the best move for the AI, without printing anything."""
        _, best_move = self.alpha_beta(game, self.depth, float('-inf'), float('inf'), True)

        if best_move:
            game.play_move(best_move[0], best_move[1])
        # If no move is possible, main logic will pass the turn.

    def alpha_beta(self, game, depth, alpha, beta, is_maximizing_player):
        """
        Implementation of the Minimax algorithm with Alpha-Beta pruning.

        This recursive function explores the game tree up to a given depth and returns
        the best score and corresponding move found for the current player.

        Parameters:
        - game: current state of the GameLogic instance.
        - depth: how many moves ahead to explore.
        - alpha: best value that the maximizer currently can guarantee.
        - beta: best value that the minimizer currently can guarantee.
        - is_maximizing_player: True if it's the AI's turn to maximize its score, False otherwise.

        Returns:
        - (best_score, best_move): tuple with the best score found and the move to achieve it.
        """

        # Base case: if maximum depth reached or game is over, evaluate and return the board state
        if depth == 0 or game.is_game_over():
            return self.evaluate(game), None

        # Get all valid moves and sort them (corners & edges prioritized to improve pruning)
        possible_moves = self.sort_moves(game.get_possible_moves())

        # If no moves available for this player, pass the turn and continue searching
        if not possible_moves:
            game.switch_player()
            val, _ = self.alpha_beta(game, depth - 1, alpha, beta, not is_maximizing_player)
            game.switch_player()
            return val, None

        # Initialize best move to None — will be updated below
        best_move = None

        if is_maximizing_player:
            # Maximizing player's turn (AI)
            max_eval = float('-inf')
            for move in possible_moves:
                # Simulate playing this move and flipping opponent pieces
                flipped_pieces = game.play_move(move[0], move[1])

                # Recursively evaluate resulting position
                evaluation, _ = self.alpha_beta(game, depth - 1, alpha, beta, False)

                # Undo the simulated move to restore board state
                game.undo_move(move[0], move[1], flipped_pieces)

                # Update best evaluation if we found a better move
                if evaluation > max_eval:
                    max_eval = evaluation
                    best_move = move

                # Update alpha (best score the maximizer can guarantee so far)
                alpha = max(alpha, evaluation)

                # Alpha-Beta pruning: if current branch can't improve beta, stop searching this branch
                if beta <= alpha:
                    break  # Prune this branch (alpha cut-off)

            return max_eval, best_move

        else:
            # Minimizing player's turn (opponent)
            min_eval = float('inf')
            for move in possible_moves:
                # Simulate playing this move and flipping opponent pieces
                flipped_pieces = game.play_move(move[0], move[1])

                # Recursively evaluate resulting position
                evaluation, _ = self.alpha_beta(game, depth - 1, alpha, beta, True)

                # Undo the simulated move to restore board state
                game.undo_move(move[0], move[1], flipped_pieces)

                # Update best evaluation if we found a worse move (for minimizer)
                if evaluation < min_eval:
                    min_eval = evaluation
                    best_move = move

                # Update beta (best score the minimizer can guarantee so far)
                beta = min(beta, evaluation)

                # Alpha-Beta pruning: if current branch can't improve alpha, stop searching this branch
                if beta <= alpha:
                    break  # Prune this branch (beta cut-off)

            return min_eval, best_move

    def evaluate(self, game):
        """Evaluate the current board position and return a score for the AI."""
        scores = game.get_score()
        if game.is_game_over():
            if scores[self.color] > scores[self.opposite_color()]:
                return 10000  # Win
            if scores[self.color] < scores[self.opposite_color()]:
                return -10000  # Loss
            return 0  # Draw

        # Heuristic combining positional value and mobility
        position_value = 0
        for i in range(8):
            for j in range(8):
                piece_color = game.board.piece_color(i, j)
                if piece_color == self.color:
                    position_value += self.position_weights[i][j]
                elif piece_color == self.opposite_color():
                    position_value -= self.position_weights[i][j]

        # Compute mobility (number of possible moves)
        ai_mobility = len(game.get_possible_moves())
        game.switch_player()
        opponent_mobility = len(game.get_possible_moves())
        game.switch_player()

        # Mobility factor is the difference in possible moves
        mobility = 15 * (ai_mobility - opponent_mobility)

        return position_value + mobility