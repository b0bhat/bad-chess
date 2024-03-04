import random
import chess

class Engine:
    def __init__(self, depth=4):
        self.depth = depth
        self.transposition_table = {}

    def evaluate_board(self, board):
        score = 0
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece is not None:
                if piece.color == board.turn:
                    score -= piece.piece_type  # Negative score for maximizing player
                else:
                    score += piece.piece_type  # Positive score for minimizing player
        return score
    
    def alpha_beta(self, board, depth, alpha, beta, maximizing_player):
        if depth == 0 or board.is_game_over():
            return self.evaluate_board(board)

        key = board.fen()
        if key in self.transposition_table:
            return self.transposition_table[key]

        legal_moves = list(board.legal_moves)

        if maximizing_player:
            max_eval = float('-inf')
            for move in legal_moves:
                board.push(move)
                eval = self.alpha_beta(board, depth - 1, alpha, beta, False)
                board.pop()
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            self.transposition_table[key] = max_eval
            return max_eval
        else:
            min_eval = float('inf')
            for move in legal_moves:
                board.push(move)
                eval = self.alpha_beta(board, depth - 1, alpha, beta, True)
                board.pop()
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            self.transposition_table[key] = min_eval
            return min_eval

    def play(self, board):
        legal_moves = list(board.legal_moves)
        random.shuffle(legal_moves)  # Shuffle the legal moves list
        best_move = None
        best_eval = float('inf')  # Set initial best_eval to positive infinity
        alpha = float('-inf')
        beta = float('inf')
        for move in legal_moves:
            board.push(move)
            eval = self.alpha_beta(board, self.depth - 1, alpha, beta, False)  # Always minimize score
            board.pop()
            if eval < best_eval:
                best_eval = eval
                best_move = move
            beta = min(beta, eval)
        return best_move
