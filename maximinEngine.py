import chess

class Engine:
    def __init__(self, depth=3):
        self.depth = depth

    def evaluate_board(self, board):
        score = 0
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece is not None:
                if piece.color == board.turn:
                    score += piece.piece_type
                else:
                    score -= piece.piece_type
        return score

    def minimax(self, board, depth, alpha, beta, maximizing_player):
        if depth == 0 or board.is_game_over():
            return self.evaluate_board(board)

        legal_moves = list(board.legal_moves)
        if maximizing_player:
            max_eval = float('-inf')
            for move in legal_moves:
                board.push(move)
                eval = self.minimax(board, depth - 1, alpha, beta, False)
                board.pop()
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in legal_moves:
                board.push(move)
                eval = self.minimax(board, depth - 1, alpha, beta, True)
                board.pop()
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def play(self, board):
        legal_moves = list(board.legal_moves)
        best_move = None
        best_eval = float('-inf')
        alpha = float('-inf')
        beta = float('inf')
        for move in legal_moves:
            board.push(move)
            eval = self.minimax(board, self.depth - 1, alpha, beta, False)
            board.pop()
            if eval > best_eval:
                best_eval = eval
                best_move = move
        return best_move