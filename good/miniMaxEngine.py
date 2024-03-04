import chess

class Engine:
    def __init__(self, depth=4):
        self.depth = depth
        self.transposition_table = {}
        self.visited_positions = set()

    def evaluate_board(self, board):
        # Simple evaluation function: material advantage
        score = sum(piece.piece_type * (1 if piece.color == board.turn else -1)
                    for piece in board.piece_map().values())
        return score
    
    def alpha_beta(self, board, depth, alpha, beta, maximizing):
        if depth == 0 or board.is_game_over():
            return self.evaluate_board(board)

        key = board.fen()
        if key in self.transposition_table:
            return self.transposition_table[key]

        legal_moves = list(board.legal_moves)
        if maximizing:
            min_eval = float('-inf')  # Change this line
            for move in legal_moves:
                board.push(move)
                eval = self.alpha_beta(board, depth - 1, alpha, beta, False)
                board.pop()
                min_eval = min(min_eval, eval)  # Change this line
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            self.transposition_table[key] = min_eval
            return min_eval
        else:
            max_eval = float('-inf')
            for move in legal_moves:
                board.push(move)
                eval = self.alpha_beta(board, depth - 1, alpha, beta, True)
                board.pop()
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            self.transposition_table[key] = max_eval
            return max_eval


    def play(self, board):
        legal_moves = list(board.legal_moves)
        best_move = None
        best_eval = float('inf')
        alpha = float('inf')
        beta = float('-inf')
        for move in legal_moves:
            board.push(move)
            if board.fen() not in self.visited_positions:  # Check for repetition
                eval = self.alpha_beta(board, self.depth - 1, alpha, beta, True)
                if eval < best_eval:
                    best_eval = eval
                    best_move = move
                alpha = max(alpha, eval)
            board.pop()
        self.visited_positions.add(board.fen())  # Add current position to visited positions
        return best_move
