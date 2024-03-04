import random
import chess

class Engine:
    PIECE_VALUES = {
        chess.PAWN: 1,
        chess.KNIGHT: 3,
        chess.BISHOP: 3,
        chess.ROOK: 5,
        chess.QUEEN: 9,
        chess.KING: 100
    }
   
    def evaluate_material(self, board):
        score = 0
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece is not None:
                if piece.color == board.turn:
                    score += self.PIECE_VALUES[piece.piece_type]
                else:
                    score -= self.PIECE_VALUES[piece.piece_type]
        return score
    
    def play(self, board):
        legal_moves = list(board.legal_moves)
        random.shuffle(legal_moves)
        worst_move = None
        min_eval = float('-inf')
        for move in legal_moves:
            board.push(move)
            eval = self.evaluate_board(board)
            if eval > min_eval:
                min_eval = eval
                worst_move = move
            board.pop()
        return worst_move